"""美国区域判定、白名单与解析链（CF 头 -> MaxMind -> HTTP）。"""
from __future__ import annotations

import asyncio
import ipaddress
import json
import time
from typing import Optional
from urllib.parse import quote

import aiohttp
from sanic import Request

from genaipf.conf import region_restrict_conf as conf
from genaipf.utils.log_utils import logger

# 简单进程内缓存: ip -> (iso_code_upper_or_empty, expire_monotonic)
_geo_cache: dict[str, tuple[str, float]] = {}
_geo_cache_lock = asyncio.Lock()
_MAX_CACHE_ENTRIES = 8192

_maxmind_reader = None
_maxmind_tried = False


def _trim_cache_unlocked() -> None:
    if len(_geo_cache) > _MAX_CACHE_ENTRIES:
        # 删掉约 1/4 最旧条目（按插入顺序近似 FIFO）
        for _ in range(_MAX_CACHE_ENTRIES // 4):
            if not _geo_cache:
                break
            _geo_cache.pop(next(iter(_geo_cache)))


def _strip_ip_token(raw: str) -> str:
    return raw.strip().split("%")[0].strip()


def get_client_ip(request: Request) -> str:
    """
    解析真实客户端公网 IP，供地区判断使用。

    仅取 X-Forwarded-For 首段在「前置为内网/保留地址」时会误判（常见于网关追加
    内网 hop），此时地区中间件会误判为内网而直接放行，而 remote_addr 仍为公网。
    因此从左到右取第一个非公网地址；若无则尝试 X-Real-IP / True-Client-IP，
    再回退 request.ip / request.remote_addr。
    """
    hdr = getattr(request.app.config, "REAL_IP_HEADER", None) or "X-Forwarded-For"
    raw = request.headers.get(hdr) or request.headers.get(hdr.upper())
    if raw:
        for part in raw.split(","):
            ip_str = _strip_ip_token(part)
            if ip_str and not _is_private_or_reserved(ip_str):
                return ip_str

    for alt in ("X-Real-IP", "x-real-ip", "True-Client-IP", "true-client-ip"):
        alt_raw = request.headers.get(alt)
        if alt_raw:
            ip_str = _strip_ip_token(alt_raw)
            if ip_str and not _is_private_or_reserved(ip_str):
                return ip_str

    fallback = request.ip or request.remote_addr or ""
    fb = _strip_ip_token(fallback)
    if fb and not _is_private_or_reserved(fb):
        return fb
    return ""


def _is_private_or_reserved(ip_str: str) -> bool:
    try:
        ip_obj = ipaddress.ip_address(ip_str)
    except ValueError:
        return True
    return bool(
        ip_obj.is_private
        or ip_obj.is_loopback
        or ip_obj.is_link_local
        or ip_obj.is_reserved
        or ip_obj.is_multicast
    )


def _parse_ip_networks(raw: str) -> list:
    nets: list[ipaddress._BaseNetwork] = []
    for part in raw.split(","):
        part = part.strip()
        if not part:
            continue
        try:
            if "/" in part:
                nets.append(ipaddress.ip_network(part, strict=False))
            else:
                nets.append(ipaddress.ip_network(f"{part}/32", strict=False))
        except ValueError:
            try:
                nets.append(ipaddress.ip_network(f"{part}/128", strict=False))
            except ValueError:
                logger.warning(f"region_restrict: skip invalid whitelist CIDR/IP: {part}")
    return nets


_IP_NETWORKS: list = []


def _ensure_ip_networks_loaded() -> None:
    global _IP_NETWORKS
    if _IP_NETWORKS:
        return
    if conf.REGION_WHITELIST_IPS:
        _IP_NETWORKS = _parse_ip_networks(conf.REGION_WHITELIST_IPS)


def ip_in_whitelist_networks(ip_str: str) -> bool:
    _ensure_ip_networks_loaded()
    if not _IP_NETWORKS:
        return False
    try:
        ip_obj = ipaddress.ip_address(ip_str)
    except ValueError:
        return False
    return any(ip_obj in net for net in _IP_NETWORKS)


def _get_maxmind_reader():
    global _maxmind_reader, _maxmind_tried
    if _maxmind_tried:
        return _maxmind_reader
    _maxmind_tried = True
    path = conf.GEOIP2_COUNTRY_MMDB
    if not path:
        return None
    import os

    if not os.path.isfile(path):
        logger.warning(f"region_restrict: GEOIP2_COUNTRY_MMDB not a file: {path}")
        return None
    try:
        import geoip2.database
    except ImportError:
        logger.warning(
            "region_restrict: geoip2 not installed; pip install geoip2 for MaxMind support"
        )
        return None
    try:
        _maxmind_reader = geoip2.database.Reader(path)
        logger.info(f"region_restrict: MaxMind Reader opened: {path}")
    except Exception as e:
        logger.error(f"region_restrict: failed to open MaxMind db: {e}")
        _maxmind_reader = None
    return _maxmind_reader


def country_from_maxmind(ip_str: str) -> Optional[str]:
    reader = _get_maxmind_reader()
    if reader is None:
        return None
    try:
        rec = reader.country(ip_str)
        code = rec.country.iso_code
        return code.upper() if code else None
    except Exception as e:
        if e.__class__.__name__ == "AddressNotFoundError":
            return None
        logger.warning(f"region_restrict: maxmind lookup error for {ip_str}: {e}")
        return None


def country_from_cf(request: Request) -> Optional[str]:
    if not conf.REGION_TRUST_CF_IP_COUNTRY:
        return None
    cc = request.headers.get("CF-IPCountry") or request.headers.get("cf-ipcountry")
    if not cc:
        return None
    cc = cc.strip().upper()
    if cc in ("XX", "T1", ""):
        return None
    return cc


async def _http_country_code(ip_str: str) -> Optional[str]:
    if not conf.REGION_GEO_HTTP_FALLBACK_ENABLED:
        return None
    tpl = conf.REGION_GEO_HTTP_URL_TEMPLATE
    if "{ip}" not in tpl:
        logger.error("region_restrict: REGION_GEO_HTTP_URL_TEMPLATE must contain {ip}")
        return None
    url = tpl.format(ip=quote(ip_str, safe=":"))
    timeout = aiohttp.ClientTimeout(total=2.5)
    try:
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.get(url, headers={"User-Agent": "GenAI-Platform/region-restrict"}) as resp:
                if resp.status != 200:
                    return None
                text = await resp.text()
    except Exception as e:
        logger.warning(f"region_restrict: http geo failed for {ip_str}: {e}")
        return None
    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        return None
    # ipwho.is
    if isinstance(data, dict) and "country_code" in data:
        if not data.get("success", True):
            return None
        c = data.get("country_code")
        return str(c).upper() if c else None
    # ip-api.com style
    if isinstance(data, dict) and data.get("status") == "success":
        c = data.get("countryCode")
        return str(c).upper() if c else None
    return None


async def resolve_country_iso(request: Request, ip_str: str) -> Optional[str]:
    """返回 ISO 3166-1 alpha-2 大写国家码；无法判定返回 None。"""
    if not ip_str or _is_private_or_reserved(ip_str):
        return None

    now = time.monotonic()
    ttl = max(60, conf.REGION_GEO_CACHE_TTL_SEC)

    async with _geo_cache_lock:
        hit = _geo_cache.get(ip_str)
        if hit and hit[1] > now:
            return hit[0] or None

    cc = country_from_cf(request)
    if cc is None:
        cc = country_from_maxmind(ip_str)
    if cc is None:
        cc = await _http_country_code(ip_str)

    async with _geo_cache_lock:
        _trim_cache_unlocked()
        _geo_cache[ip_str] = (cc or "", now + ttl)

    return cc


def is_united_states(iso_code: Optional[str]) -> bool:
    if not iso_code:
        return False
    return iso_code.strip().upper() == "US"


async def redis_whitelist_user_ids() -> frozenset[str]:
    if not conf.REGION_REDIS_WHITELIST_ENABLED:
        return frozenset()
    key = conf.REGION_REDIS_WHITELIST_USER_KEY
    if not key:
        return frozenset()

    def _load():
        from genaipf.utils.redis_utils import RedisConnectionPool

        r = RedisConnectionPool().get_connection()
        members = r.smembers(key)
        out = set()
        for m in members or ():
            out.add(str(m).strip())
        return frozenset(out)

    try:
        return await asyncio.to_thread(_load)
    except Exception as e:
        logger.warning(f"region_restrict: redis user whitelist unreadable: {e}")
        return frozenset()


async def redis_whitelist_ips_raw() -> frozenset[str]:
    if not conf.REGION_REDIS_WHITELIST_ENABLED:
        return frozenset()
    key = conf.REGION_REDIS_WHITELIST_IP_KEY
    if not key:
        return frozenset()

    def _load():
        from genaipf.utils.redis_utils import RedisConnectionPool

        r = RedisConnectionPool().get_connection()
        members = r.smembers(key)
        return frozenset(str(x).strip() for x in (members or ()) if str(x).strip())

    try:
        return await asyncio.to_thread(_load)
    except Exception as e:
        logger.warning(f"region_restrict: redis ip whitelist unreadable: {e}")
        return frozenset()


def _ip_in_redis_literal_sets(ip_str: str, literals: frozenset[str]) -> bool:
    if ip_str in literals:
        return True
    try:
        ip_obj = ipaddress.ip_address(ip_str)
    except ValueError:
        return False
    for lit in literals:
        if "/" in lit:
            try:
                if ip_obj in ipaddress.ip_network(lit, strict=False):
                    return True
            except ValueError:
                continue
    return False


async def evaluate_us_region_block(
    request: Request,
    *,
    redis_users: Optional[frozenset[str]] = None,
    redis_ips: Optional[frozenset[str]] = None,
) -> dict:
    """
    返回是否按美国区策略拦截、原因码、国家码等，供中间件与探测接口共用。
    block_reason 仅在 would_block 为 True 时有值。
    """
    ip_str = get_client_ip(request)
    base = {
        "would_block": False,
        "block_reason": None,
        "country_iso": None,
        "client_ip": ip_str or "",
        "is_private_or_reserved_ip": bool(
            not ip_str or _is_private_or_reserved(ip_str)
        ),
        "restrict_us_enabled": bool(conf.REGION_RESTRICT_US_ENABLED),
    }
    if not conf.REGION_RESTRICT_US_ENABLED:
        return base

    if not ip_str or _is_private_or_reserved(ip_str):
        return base

    user = getattr(request.ctx, "user", None)
    uid = None
    if user and isinstance(user, dict):
        uid = user.get("id")
    uid_str = str(uid).strip() if uid is not None else ""

    if redis_users is None:
        redis_users = await redis_whitelist_user_ids()
    if uid_str and (uid_str in conf.REGION_WHITELIST_USER_IDS or uid_str in redis_users):
        return base

    if ip_in_whitelist_networks(ip_str):
        return base

    if redis_ips is None:
        redis_ips = await redis_whitelist_ips_raw()
    if redis_ips and _ip_in_redis_literal_sets(ip_str, redis_ips):
        return base

    iso = await resolve_country_iso(request, ip_str)
    out = {**base, "country_iso": iso}
    if iso is None:
        if not conf.REGION_GEO_UNKNOWN_ALLOW:
            out["would_block"] = True
            out["block_reason"] = "geo_unknown_blocked"
        return out

    if is_united_states(iso):
        out["would_block"] = True
        out["block_reason"] = "united_states_geo_blocked"
    return out


async def should_block_us_request(request: Request) -> bool:
    """
    True = 应拦截（美国且未命中白名单）。
    私有/内网 IP 不拦截。
    """
    ev = await evaluate_us_region_block(request)
    return bool(ev["would_block"])


def user_whitelist_hits(uid_str: str, redis_users: frozenset[str]) -> list[str]:
    """当前用户 ID 命中的白名单来源：env / redis；未登录或空 ID 返回空列表。"""
    if not uid_str:
        return []
    hits: list[str] = []
    if uid_str in conf.REGION_WHITELIST_USER_IDS:
        hits.append("env")
    if uid_str in redis_users:
        hits.append("redis")
    return hits


def ip_whitelist_hits(ip_str: str, redis_ips: frozenset[str]) -> list[str]:
    """当前客户端 IP 命中的白名单来源。"""
    if not ip_str:
        return []
    hits: list[str] = []
    if ip_in_whitelist_networks(ip_str):
        hits.append("env")
    if redis_ips and _ip_in_redis_literal_sets(ip_str, redis_ips):
        hits.append("redis")
    return hits


async def build_region_support_probe(request: Request) -> dict:
    """未登录可调的探测数据（与中间件判定一致）。"""
    ip_str = get_client_ip(request)
    user = getattr(request.ctx, "user", None)
    uid = None
    if user and isinstance(user, dict):
        uid = user.get("id")
    uid_str = str(uid).strip() if uid is not None else ""

    redis_users = await redis_whitelist_user_ids()
    redis_ips = await redis_whitelist_ips_raw()

    ev = await evaluate_us_region_block(
        request, redis_users=redis_users, redis_ips=redis_ips
    )
    would_block = bool(ev["would_block"])
    restrict_on = bool(ev["restrict_us_enabled"])
    service_supported = True
    if restrict_on:
        service_supported = not would_block

    return {
        "supported": service_supported,
        "restrict_on": restrict_on,
        "ip": ev["client_ip"],
        "uid": uid_str or None,
        "country": ev["country_iso"],
        "in_user_wl": user_whitelist_hits(uid_str, redis_users),
        "in_ip_wl": ip_whitelist_hits(ip_str, redis_ips),
        "reason": ev["block_reason"],
    }


async def merged_whitelist_view() -> dict[str, list[str]]:
    """合并 .env 静态白名单与 Redis SET（仅值，不含管理逻辑）。"""
    redis_users = await redis_whitelist_user_ids()
    redis_ips = await redis_whitelist_ips_raw()
    env_users = sorted(conf.REGION_WHITELIST_USER_IDS)
    env_ips: list[str] = []
    if conf.REGION_WHITELIST_IPS:
        env_ips = [
            p.strip()
            for p in conf.REGION_WHITELIST_IPS.split(",")
            if p.strip()
        ]
    user_ids = sorted(set(env_users) | set(redis_users))
    ips = sorted(set(env_ips) | set(redis_ips))
    return {"user_ids": user_ids, "ips": ips}


def path_matches_restrict_prefix(path: str) -> bool:
    for prefix in conf.REGION_RESTRICT_PATH_PREFIXES:
        if path == prefix or path.startswith(prefix + "/"):
            return True
    return False


# 登录与注册前置接口：不因美国 IP 拦截，便于用户登录后命中账号白名单
_REGION_AUTH_EXEMPT_PATHS: frozenset[str] = frozenset(
    {
        "/v1/api/userLogin",
        "/v1/api/userLoginOther",
        "/v1/api/plugin/login",
        "/v1/api/register",
        "/v1/api/sendVerifyCode",
        "/v1/api/sendEmailCode",
        "/v1/api/getCaptcha",
        "/v1/api/testVerifyCode",
        "/v1/api/modifyPassword",
        "/v1/api/userCheckExist",
        "/v2/api/userLogin",
        "/v2/api/userLoginOther",
        "/v2/api/plugin/login",
        "/v2/api/register",
        "/v2/api/sendVerifyCode",
        "/v2/api/sendEmailCode",
        "/v2/api/sendAppEmailCode",
        "/v2/api/getCaptcha",
        "/v2/api/testVerifyCode",
        "/v2/api/modifyPassword",
        "/v2/api/userCheckExist",
        "/v2/api/ios/vip/config",
        "/v2/api/region/supportStatus",
        "/v2/api/region/whitelist",
    }
)


def path_exempt_from_region_check(path: str) -> bool:
    if path in _REGION_AUTH_EXEMPT_PATHS:
        return True
    if path in conf.REGION_RESTRICT_AUTH_EXEMPT_PATHS:
        return True
    return False
