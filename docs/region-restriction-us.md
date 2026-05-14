# GenAI-Platform 美国区域访问限制说明

本文描述对「美国来源流量」的拦截策略、白名单、地理解析链、如何确认是否已有 MaxMind 库，以及与动态 HTTP 检测的关系。实现代码位于：

- 配置：`genaipf/conf/region_restrict_conf.py`（环境变量）
- 解析与白名单：`genaipf/utils/region_restrict.py`
- 中间件：`genaipf/middlewares/region_restriction_middleware.py`
- 入口注册：`app.py`（在 `check_user` 之后、`save_user_log` 之前）
- 错误码：`ERROR_CODE["REGION_NOT_SUPPORTED"]` = **5021**；白名单管理鉴权失败 **5022**、操作者不允许 **5023**

## 1. 功能概述

在开启 `REGION_RESTRICT_US_ENABLED=true` 后，对 **默认** 前缀下的 HTTP 请求进行校验：

- 路径前缀（可配置，默认）：`/v1/api`、`/v2/api`、`/mpcbot`
- 跳过：`OPTIONS`（CORS 预检）、`/static` 开头路径
- **登录与注册前置接口**（`userLogin`、`register`、`sendVerifyCode` 等，见 `genaipf/utils/region_restrict.py` 中 `_REGION_AUTH_EXEMPT_PATHS`）不做美国 IP 拦截，便于美国 IP 用户完成登录后命中**账号白名单**。另可通过环境变量 `REGION_RESTRICT_AUTH_EXEMPT_PATHS`（逗号分隔的完整 path）追加豁免。

**判定顺序（与产品逻辑一致）：**

1. **账号白名单**：若 `request.ctx.user` 存在（由前置 `check_user` 写入），且用户 `id` 在环境变量 `REGION_WHITELIST_USER_IDS` 或 Redis Set `REGION_REDIS_WHITELIST_USER_KEY` 中 → **直接放行**，不做 IP/地区判断。
2. **IP 白名单（CIDR）**：客户端 IP 命中 `REGION_WHITELIST_IPS` 中的网段 → **放行**。
3. **Redis IP 白名单**：若启用 Redis 白名单，IP 出现在 `REGION_REDIS_WHITELIST_IP_KEY` 集合中（支持纯 IP 或带 `/` 的 CIDR 字符串）→ **放行**。
4. **美国判定**：经解析链得到国家码为 `US` → 返回 JSON 错误，**code = 5021**，文案见 `ERROR_MESSAGE[5021]`。
5. **其它国家** → 正常进入业务。

**内网/保留地址**（如 `127.0.0.1`、`10.x`、`192.168.x`）不做公网地理解析，**一律放行**（便于本地与内网调试）。

## 2. 如何确认是否已有 MaxMind（.mmdb）

MaxMind **不会**随本仓库自动安装；若未配置路径或文件不存在，逻辑会自动跳过本地库。

可按下面方式自查（任选）：

1. **环境变量**：在运行服务的 `.env` 或部署配置里搜 `GEOIP2_COUNTRY_MMDB`、`MMDB`、`GeoLite2`、`GeoIP2`。
2. **机器文件**：在服务器或镜像构建脚本中查找 `.mmdb` 文件，例如：
   - `find /usr /opt /var /home -name "*.mmdb" 2>/dev/null | head`
3. **依赖**：本地库需要 Python 包 `geoip2`（见下文）；仅安装包而没有 `.mmdb` 文件仍无法使用本地解析。

若 **没有** mmdb：无需强制补齐即可运行——系统会按配置使用 **Cloudflare 国家头**（若开启信任）或 **HTTP 兜底**（见下一节）。

## 3. 地理解析链（动态检测是否可行）

**可行。** 解析顺序为：

| 优先级 | 来源 | 条件 |
|--------|------|------|
| 1 | `CF-IPCountry` 请求头 | `REGION_TRUST_CF_IP_COUNTRY=true`，且仅在你确认请求 **必定经过 Cloudflare**、该头不可被客户端伪造时开启。 |
| 2 | MaxMind GeoIP2 / GeoLite2 Country | `GEOIP2_COUNTRY_MMDB` 指向存在的 `.mmdb` 文件，且已 `pip install geoip2`。 |
| 3 | HTTP 公网接口 | `REGION_GEO_HTTP_FALLBACK_ENABLED=true`（默认），使用 `REGION_GEO_HTTP_URL_TEMPLATE`（默认 `https://ipwho.is/{ip}`）。 |

说明：

- HTTP 方案 **无需** mmdb，适合快速上线；但有 **频率与可用性** 限制，因此实现里对「IP → 国家码」做了 **进程内缓存**（TTL 默认 3600 秒，可配 `REGION_GEO_CACHE_TTL_SEC`）。
- 若解析失败或无法得到国家码：由 `REGION_GEO_UNKNOWN_ALLOW` 控制。**默认 `true` = 放行**（避免第三方故障导致全站不可用）；若合规要求「未知一律按美国处理」，设为 `false`，此时未知会被 **拦截**（与解析失败时中间件异常分支行为一致，见代码注释）。

## 4. 环境变量一览

| 变量 | 默认 | 说明 |
|------|------|------|
| `REGION_RESTRICT_US_ENABLED` | `false` | 总开关 |
| `REGION_RESTRICT_PATH_PREFIXES` | `/v1/api,/v2/api,/mpcbot` | 逗号分隔路径前缀 |
| `REGION_WHITELIST_USER_IDS` | 空 | 用户 id 白名单，逗号分隔 |
| `REGION_WHITELIST_IPS` | 空 | IP/CIDR 白名单，逗号分割 |
| `REGION_TRUST_CF_IP_COUNTRY` | `false` | 是否信任 `CF-IPCountry` |
| `GEOIP2_COUNTRY_MMDB` | 空 | MaxMind Country `.mmdb` 绝对路径 |
| `REGION_GEO_HTTP_FALLBACK_ENABLED` | `true` | 是否允许 HTTP 兜底 |
| `REGION_GEO_HTTP_URL_TEMPLATE` | `https://ipwho.is/{ip}` | 必须含 `{ip}`；可换为自建或带 key 的兼容 JSON 接口 |
| `REGION_GEO_CACHE_TTL_SEC` | `3600` | 解析结果缓存秒数 |
| `REGION_GEO_UNKNOWN_ALLOW` | `true` | 无法解析国家时是否放行 |
| `REGION_REDIS_WHITELIST_ENABLED` | `true` | 是否与 Redis Set 并集白名单 |
| `REGION_REDIS_WHITELIST_USER_KEY` | `geo:region:whitelist:user` | Redis 用户 id Set |
| `REGION_REDIS_WHITELIST_IP_KEY` | `geo:region:whitelist:ip` | Redis IP/CIDR Set |
| `REGION_WHITELIST_ADMIN_KEY` | 空 | 使用白名单 **查询/变更** HTTP 接口时**必填**：与请求头 `X-Region-Wl-Admin-Key` 一致 |
| `REGION_WHITELIST_ADMIN_OPERATOR_IDS` | 空 | 使用上述接口时**必填且非空**（逗号分隔用户 ID）；仅允许列表中的用户作为操作者（来自登录态或 `X-Region-Wl-Operator-Id`） |

客户端 IP 取自与 `app.config.REAL_IP_HEADER` 一致的 `X-Forwarded-For` **第一段**（与现有 Sanic 配置一致）；请保证 **网关只追加可信链**，避免伪造。

白名单 **查询与变更** 接口对同一客户端 IP 固定为每分钟最多 **5** 次（查询与变更合计），在代码中写死，不设环境变量。

## 4.1 区域探测与白名单 HTTP 接口

### 探测（免登录）

- **GET** `/v2/api/region/supportStatus`（已列入 `_REGION_AUTH_EXEMPT_PATHS`，美国区中间件不拦截）
- 成功时 `data` 字段含义如下：

| 字段 | 含义 |
|------|------|
| `supported` | 当前是否视为可服务区域（与中间件一致；开启限制且会被拦时为 `false`） |
| `restrict_on` | `REGION_RESTRICT_US_ENABLED` 是否开启 |
| `ip` | 服务端解析到的客户端公网 IP |
| `uid` | 当前用户 ID（未登录为 `null`） |
| `country` | 国家码 ISO；内网/未解析可为 `null` |
| `in_user_wl` | 用户 ID 命中的白名单来源：`env` / `redis`，无则为 `[]` |
| `in_ip_wl` | 客户端 IP 命中的白名单来源：`env` / `redis`，无则为 `[]` |
| `reason` | 被拦截时的原因：`united_states_geo_blocked` / `geo_unknown_blocked`，否则 `null` |

```bash
curl -sS "https://<HOST>/v2/api/region/supportStatus"
```

### 白名单查询与变更（需管理密钥 + 允许的操作者）

**环境变量前置条件**

1. `REGION_REDIS_WHITELIST_ENABLED=true`，且已配置 `REGION_REDIS_WHITELIST_USER_KEY`、`REGION_REDIS_WHITELIST_IP_KEY`。
2. `REGION_WHITELIST_ADMIN_KEY` 已设置为足够长的随机串。
3. `REGION_WHITELIST_ADMIN_OPERATOR_IDS` 已设置为**非空**逗号列表（例如运维在业务系统中的用户 ID）。
4. 数据库已执行 `docs/sql/region_whitelist_admin_audit.sql` 建表（审计）。

**请求头**

- `X-Region-Wl-Admin-Key`：与 `REGION_WHITELIST_ADMIN_KEY` 一致。
- `X-Region-Wl-Operator-Id`：无有效登录 Token 时**必填**，且该 ID 必须在 `REGION_WHITELIST_ADMIN_OPERATOR_IDS` 中；若带有效登录 Token，则以 Token 内用户 ID 为操作者（与 Header 并存时以登录态为准）。

**查询（合并 .env 静态名单 + Redis）**

```bash
curl -sS "https://<HOST>/v2/api/region/whitelist" \
  -H "X-Region-Wl-Admin-Key: <YOUR_ADMIN_KEY>" \
  -H "X-Region-Wl-Operator-Id: <OPERATOR_USER_ID>"
```

成功时 `data` 含 `user_ids`、`ips` 两个数组（可为 `[]`）。

**变更 Redis 白名单（POST，JSON）**

```bash
curl -sS -X POST "https://<HOST>/v2/api/region/whitelist" \
  -H "Content-Type: application/json" \
  -H "X-Region-Wl-Admin-Key: <YOUR_ADMIN_KEY>" \
  -H "X-Region-Wl-Operator-Id: <OPERATOR_USER_ID>" \
  -d '{"mode":"append","user_ids":["10001"],"ips":["203.0.113.10"]}'
```

```bash
# clear：仅清空显式传入空数组 [] 的一侧（此处只清空 Redis 用户白名单 Set）
curl -sS -X POST "https://<HOST>/v2/api/region/whitelist" \
  -H "Content-Type: application/json" \
  -H "X-Region-Wl-Admin-Key: <YOUR_ADMIN_KEY>" \
  -H "X-Region-Wl-Operator-Id: <OPERATOR_USER_ID>" \
  -d '{"mode":"clear","user_ids":[]}'
```

`mode`：`append` | `replace` | `delete` | `clear`；`user_ids`、`ips` 校验与语义见 `genaipf/services/region_whitelist_admin_service.py`。

## 5. 可选依赖

本地 MaxMind 解析需要：

```bash
pip install geoip2
```

并在环境变量中设置 `GEOIP2_COUNTRY_MMDB`。`requirements.txt` 中可保留为可选注释行，由运维按需安装。

## 6. Redis 白名单运维示例

```bash
redis-cli SADD geo:region:whitelist:user "10001"
redis-cli SADD geo:region:whitelist:ip "203.0.113.10"
redis-cli SADD geo:region:whitelist:ip "198.51.100.0/24"
```

与 `.env` 中的名单为 **并集**。

## 7. 错误响应格式

与现有 `fail()` 一致，例如：

```json
{
  "code": 5021,
  "message": "Service is not available in your region ",
  "status": "false"
}
```

（`message` 前半段为 `ERROR_MESSAGE[5021]`，后半可为附加说明；当前实现附加为空字符串。）

## 8. 中间件顺序说明

当前顺序：`check_user` → `region_restriction_middleware` → `save_user_log`。

这样已登录用户可命中 **账号白名单**；未登录或免登录接口仍可进行 **IP 白名单 / 美国拦截**。

若 `check_user` 已对某请求返回 401，Sanic 将中止后续中间件，则不会再做地区判断（与「未通过鉴权」一致）。

## 9. 合规与性能建议

- 生产优先：**CF 可信头** 或 **本地 mmdb + 缓存**；HTTP 仅作兜底或低 QPS 场景。
- 定期更新 MaxMind 数据库文件；注意许可协议（GeoLite2 需 MaxMind 账号与许可链接）。
- 监控 5021 比例与 HTTP 解析错误日志，必要时缩短 TTL 或扩容缓存层（后续可演进为 Redis 缓存）。
