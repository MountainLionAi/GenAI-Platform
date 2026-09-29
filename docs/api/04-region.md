# 区域访问

本模块 3 个已挂载接口。通用约定见 [README](README.md)。

## 索引

| 方法 | 路径 | 鉴权 |
| --- | --- | --- |
| GET | [`/v2/api/region/supportStatus`](#get-v2-api-region-supportstatus-1) | 需要 x-api-key，免登录 |
| GET | [`/v2/api/region/whitelist`](#get-v2-api-region-whitelist-2) | 需要 x-api-key，免登录 |
| POST | [`/v2/api/region/whitelist`](#post-v2-api-region-whitelist-3) | 需要 x-api-key，免登录 |

## 详情

### GET `/v2/api/region/supportStatus`

<a id="get-v2-api-region-supportstatus-1"></a>

GET：未登录可查，返回是否支持当前区域及白名单命中情况。

- 路由键：`region_support_status`
- 鉴权：需要 x-api-key，免登录
- 实现：`GenAI/genaipf/controller/region_whitelist_api.py:31` `genaipf.controller.region_whitelist_api.region_support_status`
- 响应：JSON 信封 `{code,message,status,data}`

无额外 query/body 字段（或参数在更下游动态拼装）。

### GET `/v2/api/region/whitelist`

<a id="get-v2-api-region-whitelist-2"></a>

GET：分别返回 .env 与 Redis 白名单；需管理密钥与操作者。

不走用户 JWT。`X-Region-Wl-Admin-Key` 必填；操作者优先用登录用户，否则用 `X-Region-Wl-Operator-Id`，并且必须在 `REGION_WHITELIST_ADMIN_OPERATOR_IDS` 里。同一 IP 每分钟最多 5 次。

- 路由键：`region_whitelist_get`
- 鉴权：需要 x-api-key，免登录
- 实现：`GenAI/genaipf/controller/region_whitelist_api.py:37` `genaipf.controller.region_whitelist_api.region_whitelist_get`
- 响应：JSON 信封 `{code,message,status,data}`

**额外请求头**

| 字段 | 读取方式 | 默认值 |
| --- | --- | --- |
| `X-Region-Wl-Admin-Key` | `.get` | 无 |
| `X-Region-Wl-Operator-Id` | `.get` | 无 |

无额外 query/body 字段（或参数在更下游动态拼装）。

### POST `/v2/api/region/whitelist`

<a id="post-v2-api-region-whitelist-3"></a>

POST：变更 Redis 白名单（append/replace/delete/clear）。

不走用户 JWT。`X-Region-Wl-Admin-Key` 必填；操作者优先用登录用户，否则用 `X-Region-Wl-Operator-Id`，并且必须在 `REGION_WHITELIST_ADMIN_OPERATOR_IDS` 里。同一 IP 每分钟最多 5 次。 `mode` 为 append、replace、delete、clear。append/delete 时 `user_ids` 或 `ips` 至少一个非空数组；clear 时对要清空的一侧传 `[]`。

- 路由键：`region_whitelist_post`
- 鉴权：需要 x-api-key，免登录
- 实现：`GenAI/genaipf/controller/region_whitelist_api.py:45` `genaipf.controller.region_whitelist_api.region_whitelist_post`
- 响应：JSON 信封 `{code,message,status,data}`
- 显式错误码：`PARAMS_ERROR`

**JSON Body**

| 字段 | 读取方式 | 默认值 |
| --- | --- | --- |
| `mode` | `.get` | `append` |
| `user_ids` | `.get` | 无 |
| `ips` | `.get` | 无 |

**额外请求头**

| 字段 | 读取方式 | 默认值 |
| --- | --- | --- |
| `X-Region-Wl-Admin-Key` | `.get` | 无 |
| `X-Region-Wl-Operator-Id` | `.get` | 无 |
