"""区域限制探测与白名单管理接口。"""
from __future__ import annotations

from sanic import Request

from genaipf.constant.error_code import ERROR_CODE
from genaipf.interfaces.common_response import fail, success
from genaipf.services import region_whitelist_admin_service as rw_admin
from genaipf.utils import region_restrict


def _map_admin_error_message(message: str) -> int:
    if "过于频繁" in message:
        return ERROR_CODE["REQUEST_FREQUENCY_TOO_HIGH"]
    if "必须配置 REGION_WHITELIST_ADMIN_OPERATOR_IDS" in message:
        return ERROR_CODE["PARAMS_ERROR"]
    if "不在 REGION_WHITELIST_ADMIN_OPERATOR_IDS 允许列表" in message:
        return ERROR_CODE["REGION_WHITELIST_ADMIN_FORBIDDEN"]
    if (
        "管理密钥" in message
        or rw_admin.HEADER_ADMIN_KEY in message
        or "REGION_WHITELIST_ADMIN_KEY" in message
    ):
        return ERROR_CODE["REGION_WHITELIST_ADMIN_INVALID"]
    return ERROR_CODE["PARAMS_ERROR"]


async def region_support_status(request: Request):
    """GET：未登录可查，返回是否支持当前区域及白名单命中情况。"""
    data = await region_restrict.build_region_support_probe(request)
    return success(data)


async def region_whitelist_get(request: Request):
    """GET：分别返回 .env 与 Redis 白名单；需管理密钥与操作者。"""
    ok, msg, data = await rw_admin.query_whitelist(request)
    if not ok:
        return fail(_map_admin_error_message(msg), message=msg)
    return success(data)


async def region_whitelist_post(request: Request):
    """POST：变更 Redis 白名单（append/replace/delete/clear）。"""
    body = request.json
    if body is None:
        return fail(ERROR_CODE["PARAMS_ERROR"], message="请求体须为 JSON 对象")
    ok, msg, summary = await rw_admin.apply_mutate(request, body)
    if not ok:
        return fail(_map_admin_error_message(msg), message=msg)
    return success(summary)
