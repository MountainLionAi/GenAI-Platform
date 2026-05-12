"""美国等区域限制相关环境变量（独立文件，避免与 server 循环依赖）。"""
import os


def _truthy(raw: str | None, default: bool = False) -> bool:
    if raw is None or raw == "":
        return default
    return raw.strip().lower() in ("1", "true", "yes", "y", "on")


# 总开关：开启后对美国 IP 拦截（经白名单与解析链）
REGION_RESTRICT_US_ENABLED = _truthy(os.getenv("REGION_RESTRICT_US_ENABLED"), False)

# 仅对这些 URL 前缀做检查（全站 API + chatbot）
REGION_RESTRICT_PATH_PREFIXES = tuple(
    p.strip()
    for p in os.getenv(
        "REGION_RESTRICT_PATH_PREFIXES",
        "/v1/api,/v2/api,/mpcbot",
    ).split(",")
    if p.strip()
)

# 信任 Cloudflare 注入的国家码（仅在前面有 CF 且不可伪造时开启）
REGION_TRUST_CF_IP_COUNTRY = _truthy(os.getenv("REGION_TRUST_CF_IP_COUNTRY"), False)

# MaxMind GeoLite2 / GeoIP2 Country 数据库路径（.mmdb）；存在且可加载则优先于 HTTP
GEOIP2_COUNTRY_MMDB = os.getenv("GEOIP2_COUNTRY_MMDB", "").strip()

# 无本地库时是否允许 HTTP 解析（默认开）；关则仅 CF + MaxMind
REGION_GEO_HTTP_FALLBACK_ENABLED = _truthy(
    os.getenv("REGION_GEO_HTTP_FALLBACK_ENABLED"), True
)

# HTTP 解析使用的模板 URL，{ip} 占位；默认 ipwho.is（无需 key，有频率限制，务必配合缓存）
REGION_GEO_HTTP_URL_TEMPLATE = os.getenv(
    "REGION_GEO_HTTP_URL_TEMPLATE",
    "https://ipwho.is/{ip}",
).strip()

# IP -> 国家码 正缓存 TTL（秒）
REGION_GEO_CACHE_TTL_SEC = int(os.getenv("REGION_GEO_CACHE_TTL_SEC", "3600"))

# 解析失败或无法判定国家时是否视为「非美国」（放行）。True=放行，False=按美国拦截（更严）
REGION_GEO_UNKNOWN_ALLOW = _truthy(os.getenv("REGION_GEO_UNKNOWN_ALLOW"), True)

# 账号白名单：用户 id，逗号分隔（与 JWT / request.ctx.user['id'] 一致）
REGION_WHITELIST_USER_IDS = frozenset(
    x.strip()
    for x in os.getenv("REGION_WHITELIST_USER_IDS", "").split(",")
    if x.strip()
)

# IP 白名单：支持单 IP 与 CIDR，逗号分隔
REGION_WHITELIST_IPS = os.getenv("REGION_WHITELIST_IPS", "").strip()

# Redis 中额外白名单（与 ENV 并集）；为空 key 则忽略
REGION_REDIS_WHITELIST_USER_KEY = os.getenv(
    "REGION_REDIS_WHITELIST_USER_KEY", "geo:region:whitelist:user"
).strip()
REGION_REDIS_WHITELIST_IP_KEY = os.getenv(
    "REGION_REDIS_WHITELIST_IP_KEY", "geo:region:whitelist:ip"
).strip()

# 是否合并 Redis 白名单（需要 Redis 已配置）
REGION_REDIS_WHITELIST_ENABLED = _truthy(
    os.getenv("REGION_REDIS_WHITELIST_ENABLED"), True
)
