from sanic import Request

from genaipf.conf import region_restrict_conf as conf
from genaipf.constant.error_code import ERROR_CODE
from genaipf.interfaces.common_response import fail
from genaipf.utils.log_utils import logger
from genaipf.utils import region_restrict


async def region_restriction_middleware(request: Request):
    """
    在 check_user 之后执行：先账号白名单，再 IP 白名单，再美国区域拦截。
    仅作用于 REGION_RESTRICT_PATH_PREFIXES 配置的前缀（默认 /v1/api、/v2/api、/mpcbot）。
    """
    if not conf.REGION_RESTRICT_US_ENABLED:
        return

    if request.method == "OPTIONS":
        return

    path = request.path or ""
    if path.startswith("/static"):
        return

    if not region_restrict.path_matches_restrict_prefix(path):
        return

    try:
        if await region_restrict.should_block_us_request(request):
            return fail(
                ERROR_CODE["REGION_NOT_SUPPORTED"],
                message="",
            )
    except Exception as e:
        logger.error(f"region_restriction_middleware: {e}")
        if not conf.REGION_GEO_UNKNOWN_ALLOW:
            return fail(ERROR_CODE["REGION_NOT_SUPPORTED"], message="")
