# 支付

本模块 5 个已挂载接口。通用约定见 [README](README.md)。

## 索引

| 方法 | 路径 | 鉴权 |
| --- | --- | --- |
| GET | [`/v2/api/pay/summary`](#get-v2-api-pay-summary-1) | 需要 x-api-key，v2 免登录；v1 需登录 |
| GET | [`/v2/api/pay/cardInfo`](#get-v2-api-pay-cardinfo-2) | 需要 x-api-key，免登录 |
| GET | [`/v2/api/pay/orderCheck`](#get-v2-api-pay-ordercheck-3) | 需要 x-api-key，需登录 |
| GET | [`/v2/api/pay/account`](#get-v2-api-pay-account-4) | 需要 x-api-key，免登录 |
| POST | [`/v2/api/pay/callback`](#post-v2-api-pay-callback-5) | 需要 x-api-key，免登录 |

## 详情

### GET `/v2/api/pay/summary`

<a id="get-v2-api-pay-summary-1"></a>

- 路由键：`paySummary`
- 鉴权：需要 x-api-key，v2 免登录；v1 需登录
- v1 镜像：`GET /v1/api/pay/summary`（同一 handler；v1 不校验 `x-api-key`）
- 实现：`ml4gp/ml4gp/controller/pay_summary.py:7` `ml4gp.controller.pay_summary.pay_summary`
- 响应：JSON 信封 `{code,message,status,data}`
- `data` 字面量键：`summary`, `summary_tg`

**Query**

| 字段 | 读取方式 | 默认值 |
| --- | --- | --- |
| `query_date` | `.get` | 无 |
| `is_email` | `.get` | 无 |
| `is_tg` | `.get` | 无 |
| `debug` | `.get` | 无 |

### GET `/v2/api/pay/cardInfo`

<a id="get-v2-api-pay-cardinfo-2"></a>

- 路由键：`query_pay_card`
- 鉴权：需要 x-api-key，免登录
- 实现：`GenAI/genaipf/controller/pay.py:11` `genaipf.controller.pay.query_pay_card`
- 响应：JSON 信封 `{code,message,status,data}`
- 显式错误码：`SYSTEM_ERROR`

无额外 query/body 字段（或参数在更下游动态拼装）。

### GET `/v2/api/pay/orderCheck`

<a id="get-v2-api-pay-ordercheck-3"></a>

- 路由键：`check_order`
- 鉴权：需要 x-api-key，需登录
- 实现：`GenAI/genaipf/controller/pay.py:24` `genaipf.controller.pay.check_order`
- 响应：JSON 信封 `{code,message,status,data}`
- 显式错误码：`ORDER_NOT_EXIST`, `PARAMS_ERROR`

**Query**

| 字段 | 读取方式 | 默认值 |
| --- | --- | --- |
| `order_no` | `.get` | 无 |

### GET `/v2/api/pay/account`

<a id="get-v2-api-pay-account-4"></a>

- 路由键：`query_user_account`
- 鉴权：需要 x-api-key，免登录
- 实现：`GenAI/genaipf/controller/pay.py:36` `genaipf.controller.pay.query_user_account`
- 响应：JSON 信封 `{code,message,status,data}`

**Query**

| 字段 | 读取方式 | 默认值 |
| --- | --- | --- |
| `visitorId` | `.get` | `` |

### POST `/v2/api/pay/callback`

<a id="post-v2-api-pay-callback-5"></a>

支付回调

- 路由键：`pay_success_callback`
- 鉴权：需要 x-api-key，免登录
- 实现：`GenAI/genaipf/controller/pay.py:53` `genaipf.controller.pay.pay_success_callback`
- 响应：JSON 信封 `{code,message,status,data}`

**JSON Body**

| 字段 | 读取方式 | 默认值 |
| --- | --- | --- |
| `userid` | `.get` | 无 |
| `email` | `.get` | 无 |
| `order_no` | `.get` | 无 |
| `card_type` | `.get` | 无 |
| `amount` | `.get` | 无 |
| `pay_type` | `.get` | 无 |
| `status` | `.get` | 无 |
