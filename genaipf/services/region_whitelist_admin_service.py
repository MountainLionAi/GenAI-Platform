"""区域白名单 Redis 管理：鉴权、校验、限流与变更。"""
from __future__ import annotations

import asyncio
import hashlib
import hmac
import ipaddress
import re
import time
from collections import deque
from typing import Any, Optional

from sanic import Request

from genaipf.conf import region_restrict_conf as conf
from genaipf.services import region_whitelist_audit_service as audit_svc
from genaipf.utils import region_restrict
from genaipf.utils.log_utils import logger
from genaipf.utils.redis_utils import RedisConnectionPool

_ADMIN_RATE_BUCKETS: dict[str, deque[float]] = {}
_ADMIN_RATE_LOCK = asyncio.Lock()

USER_ID_RE = re.compile(r"^[^\s,]{1,128}$")

HEADER_ADMIN_KEY = "X-Region-Wl-Admin-Key"
HEADER_OPERATOR_UID = "X-Region-Wl-Operator-Id"


def admin_key_sha256(raw_key: str) -> str:
    return hashlib.sha256(raw_key.encode("utf-8")).hexdigest()


def _redis():
    return RedisConnectionPool().get_connection()


def _sync_redis_delete(key: str) -> None:
    if not key:
        return
    _redis().delete(key)


def _sync_redis_sadd(key: str, members: list[str]) -> None:
    if not key or not members:
        return
    _redis().sadd(key, *members)


def _sync_redis_srem(key: str, members: list[str]) -> None:
    if not key or not members:
        return
    _redis().srem(key, *members)


def _sync_redis_replace_set(key: str, members: list[str]) -> None:
    r = _redis()
    pipe = r.pipeline(transaction=True)
    pipe.delete(key)
    if members:
        pipe.sadd(key, *members)
    pipe.execute()


async def _to_thread(fn, *args, **kwargs):
    return await asyncio.to_thread(fn, *args, **kwargs)


def verify_admin_key(request: Request) -> tuple[bool, str, str]:
    """
    校验管理密钥。
    返回 (ok, message, admin_key_sha256_hex)。
    """
    if not conf.REGION_WHITELIST_ADMIN_KEY:
        return False, "服务端未配置 REGION_WHITELIST_ADMIN_KEY", ""
    raw = (request.headers.get(HEADER_ADMIN_KEY) or "").strip()
    if not raw:
        return False, f"请求头缺少 {HEADER_ADMIN_KEY}", ""
    try:
        if not hmac.compare_digest(raw, conf.REGION_WHITELIST_ADMIN_KEY):
            return False, "管理密钥不正确", ""
    except (ValueError, TypeError):
        return False, "管理密钥不正确", ""
    return True, "", admin_key_sha256(raw)


def resolve_operator_user_id(request: Request) -> tuple[Optional[str], str]:
    ctx_user = getattr(request.ctx, "user", None)
    if ctx_user and isinstance(ctx_user, dict) and ctx_user.get("id") is not None:
        return str(ctx_user["id"]).strip(), ""
    h = (request.headers.get(HEADER_OPERATOR_UID) or "").strip()
    if h:
        return h, ""
    return None, f"缺少登录态且未提供 {HEADER_OPERATOR_UID}"


def admin_operator_acl_precheck() -> tuple[bool, str]:
    if not conf.REGION_WHITELIST_ADMIN_OPERATOR_IDS:
        return (
            False,
            "服务端必须配置 REGION_WHITELIST_ADMIN_OPERATOR_IDS 且为非空逗号分隔列表",
        )
    return True, ""


def operator_allowed(operator_id: str) -> bool:
    return operator_id in conf.REGION_WHITELIST_ADMIN_OPERATOR_IDS


_ADMIN_RATE_PER_MINUTE = 5


async def consume_admin_rate_limit(request: Request) -> tuple[bool, str]:
    lim = _ADMIN_RATE_PER_MINUTE
    ip = region_restrict.get_client_ip(request) or getattr(request, "ip", None) or "unknown"
    now = time.time()
    async with _ADMIN_RATE_LOCK:
        dq = _ADMIN_RATE_BUCKETS.setdefault(str(ip), deque())
        while dq and now - dq[0] > 60.0:
            dq.popleft()
        if len(dq) >= lim:
            return False, "管理接口请求过于频繁，请稍后再试"
        dq.append(now)
    return True, ""


def redis_whitelist_precheck() -> tuple[bool, str]:
    if not conf.REGION_REDIS_WHITELIST_ENABLED:
        return False, "REGION_REDIS_WHITELIST_ENABLED 未开启，无法操作 Redis 白名单"
    if not conf.REGION_REDIS_WHITELIST_USER_KEY or not conf.REGION_REDIS_WHITELIST_IP_KEY:
        return False, "未配置 REGION_REDIS_WHITELIST_USER_KEY 或 REGION_REDIS_WHITELIST_IP_KEY"
    return True, ""


def validate_user_id_entry(x: Any, index: int) -> tuple[Optional[str], str]:
    if x is None:
        return None, f"user_ids[{index}] 不能为 null"
    if isinstance(x, bool) or not isinstance(x, (str, int)):
        return None, f"user_ids[{index}] 须为字符串或整数"
    s = str(x).strip()
    if not s:
        return None, f"user_ids[{index}] 不能为空字符串"
    if str(x) != str(x).strip():
        return None, f"user_ids[{index}] 含首尾空白，非法"
    if not USER_ID_RE.match(s):
        return None, f"user_ids[{index}] 格式非法: {s!r}"
    return s, ""


def validate_ip_entry(x: Any, index: int) -> tuple[Optional[str], str]:
    if x is None:
        return None, f"ips[{index}] 不能为 null"
    if not isinstance(x, str):
        return None, f"ips[{index}] 须为字符串"
    s = x.strip()
    if not s:
        return None, f"ips[{index}] 不能为空字符串"
    try:
        if "/" in s:
            ipaddress.ip_network(s, strict=False)
        else:
            ipaddress.ip_address(s)
    except ValueError:
        return None, f"ips[{index}] 不是合法 IP 或 CIDR: {s!r}"
    return s, ""


def _normalize_id_list(raw: Any, field: str) -> tuple[Optional[list[str]], str]:
    """
    将 JSON 字段规范为字符串列表。
    若 raw 为 None 表示调用方判定为「键缺失」；若为其他类型则报错。
    """
    if raw is None:
        return None, ""
    if not isinstance(raw, list):
        return None, f"{field} 须为 JSON 数组"
    out: list[str] = []
    for i, x in enumerate(raw):
        if field == "user_ids":
            v, err = validate_user_id_entry(x, i)
        else:
            v, err = validate_ip_entry(x, i)
        if err:
            return None, err
        assert v is not None
        out.append(v)
    return out, ""


async def apply_mutate(
    request: Request,
    body: dict[str, Any],
) -> tuple[bool, str, Optional[dict[str, Any]]]:
    """
    执行白名单变更。成功时返回 (True, "", summary_dict)。
    """
    ok_r, msg_r = redis_whitelist_precheck()
    if not ok_r:
        return False, msg_r, None

    ok_acl, msg_acl = admin_operator_acl_precheck()
    if not ok_acl:
        return False, msg_acl, None

    ok_k, msg_k, key_hash = verify_admin_key(request)
    if not ok_k:
        return False, msg_k, None

    ok_l, msg_l = await consume_admin_rate_limit(request)
    if not ok_l:
        return False, msg_l, None

    op_id, msg_op = resolve_operator_user_id(request)
    if not op_id:
        return False, msg_op, None
    if not operator_allowed(op_id):
        return False, "当前操作者不在 REGION_WHITELIST_ADMIN_OPERATOR_IDS 允许列表中", None

    if not isinstance(body, dict):
        return False, "请求体须为 JSON 对象", None

    mode = str(body.get("mode", "append")).strip().lower()
    if mode not in ("append", "replace", "delete", "clear"):
        return False, "mode 须为 append、replace、delete 或 clear", None

    user_key = conf.REGION_REDIS_WHITELIST_USER_KEY
    ip_key = conf.REGION_REDIS_WHITELIST_IP_KEY

    has_user_key = "user_ids" in body
    has_ip_key = "ips" in body

    user_raw = body["user_ids"] if has_user_key else None
    ip_raw = body["ips"] if has_ip_key else None

    if mode == "clear":
        if has_user_key and user_raw is None:
            return False, "clear 模式下 user_ids 不能为 null，须省略或设为 []", None
        if has_ip_key and ip_raw is None:
            return False, "clear 模式下 ips 不能为 null，须省略或设为 []", None
        cleared_user = False
        cleared_ip = False
        if has_user_key:
            if not isinstance(user_raw, list):
                return False, "clear 模式下 user_ids 须为 JSON 数组", None
            if len(user_raw) != 0:
                return False, "clear 模式下 user_ids 仅允许为空数组 []", None
            cleared_user = True
        if has_ip_key:
            if not isinstance(ip_raw, list):
                return False, "clear 模式下 ips 须为 JSON 数组", None
            if len(ip_raw) != 0:
                return False, "clear 模式下 ips 仅允许为空数组 []", None
            cleared_ip = True
        if not cleared_user and not cleared_ip:
            return False, "clear 模式须至少对 user_ids 或 ips 之一传入空数组 [] 以指定清空对象", None
        try:
            if cleared_user:
                await _to_thread(_sync_redis_delete, user_key)
            if cleared_ip:
                await _to_thread(_sync_redis_delete, ip_key)
        except Exception as e:
            logger.error(f"region_whitelist_admin clear redis: {e}")
            return False, f"Redis 操作失败: {e}", None

        summary = {"mode": "clear", "cleared_user_redis": cleared_user, "cleared_ip_redis": cleared_ip}
        client_ip = region_restrict.get_client_ip(request) or ""
        audit_payload = {"mode": "clear"}
        if has_user_key:
            audit_payload["user_ids"] = []
        if has_ip_key:
            audit_payload["ips"] = []
        await audit_svc.insert_region_whitelist_audit(
            action_type="mutate_clear",
            operator_user_id=op_id,
            admin_key_sha256=key_hash,
            payload=audit_payload,
            client_ip=client_ip,
        )
        return True, "", summary

    # append / replace / delete
    u_list: Optional[list[str]] = None
    i_list: Optional[list[str]] = None
    u_err = ""
    i_err = ""

    if has_user_key:
        u_list, u_err = _normalize_id_list(user_raw, "user_ids")
        if u_err:
            return False, u_err, None
    if has_ip_key:
        i_list, i_err = _normalize_id_list(ip_raw, "ips")
        if i_err:
            return False, i_err, None

    if mode in ("append", "delete"):
        u_nonempty = bool(u_list and len(u_list) > 0)
        i_nonempty = bool(i_list and len(i_list) > 0)
        if not u_nonempty and not i_nonempty:
            return False, f"{mode} 模式须至少提供一项非空的 user_ids 或 ips", None

    if mode == "replace":
        u_nonempty = bool(u_list and len(u_list) > 0)
        i_nonempty = bool(i_list and len(i_list) > 0)
        if not u_nonempty and not i_nonempty:
            return False, "replace 模式须至少包含一个非空的 user_ids 或 ips 列表以执行替换", None

    try:
        if mode == "append":
            if u_list and len(u_list) > 0:
                await _to_thread(_sync_redis_sadd, user_key, u_list)
            if i_list and len(i_list) > 0:
                await _to_thread(_sync_redis_sadd, ip_key, i_list)
        elif mode == "delete":
            if u_list and len(u_list) > 0:
                await _to_thread(_sync_redis_srem, user_key, u_list)
            if i_list and len(i_list) > 0:
                await _to_thread(_sync_redis_srem, ip_key, i_list)
        elif mode == "replace":
            if u_list is not None and len(u_list) > 0:
                await _to_thread(_sync_redis_replace_set, user_key, u_list)
            if i_list is not None and len(i_list) > 0:
                await _to_thread(_sync_redis_replace_set, ip_key, i_list)
    except Exception as e:
        logger.error(f"region_whitelist_admin mutate redis: {e}")
        return False, f"Redis 操作失败: {e}", None

    summary = {
        "mode": mode,
        "user_ids_affected": bool(u_list and len(u_list) > 0),
        "ips_affected": bool(i_list and len(i_list) > 0),
    }
    client_ip = region_restrict.get_client_ip(request) or ""
    audit_payload = {k: v for k, v in body.items() if k in ("mode", "user_ids", "ips")}
    await audit_svc.insert_region_whitelist_audit(
        action_type=f"mutate_{mode}",
        operator_user_id=op_id,
        admin_key_sha256=key_hash,
        payload=audit_payload,
        client_ip=client_ip,
    )
    return True, "", summary


async def query_whitelist(request: Request) -> tuple[bool, str, Optional[dict[str, Any]]]:
    ok_r, msg_r = redis_whitelist_precheck()
    if not ok_r:
        return False, msg_r, None

    ok_acl, msg_acl = admin_operator_acl_precheck()
    if not ok_acl:
        return False, msg_acl, None

    ok_k, msg_k, key_hash = verify_admin_key(request)
    if not ok_k:
        return False, msg_k, None

    ok_l, msg_l = await consume_admin_rate_limit(request)
    if not ok_l:
        return False, msg_l, None

    op_id, msg_op = resolve_operator_user_id(request)
    if not op_id:
        return False, msg_op, None
    if not operator_allowed(op_id):
        return False, "当前操作者不在 REGION_WHITELIST_ADMIN_OPERATOR_IDS 允许列表中", None

    data = await region_restrict.split_whitelist_view()
    client_ip = region_restrict.get_client_ip(request) or ""
    await audit_svc.insert_region_whitelist_audit(
        action_type="query",
        operator_user_id=op_id,
        admin_key_sha256=key_hash,
        payload={"action": "query"},
        client_ip=client_ip,
    )
    return True, "", data
