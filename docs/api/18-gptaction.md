# GPT Action

本模块 14 个已挂载接口。通用约定见 [README](README.md)。

## 索引

| 方法 | 路径 | 鉴权 |
| --- | --- | --- |
| GET | [`/v2/api/gptactionGetCoinKline`](#get-v2-api-gptactiongetcoinkline-1) | 需要 x-api-key，免登录 |
| GET | [`/v2/api/gptactionGetCoinTrading`](#get-v2-api-gptactiongetcointrading-2) | 需要 x-api-key，免登录 |
| GET | [`/v2/api/gptactionGetCoinInfo`](#get-v2-api-gptactiongetcoininfo-3) | 需要 x-api-key，免登录 |
| GET | [`/v2/api/gptactionGetGoodNews`](#get-v2-api-gptactiongetgoodnews-4) | 需要 x-api-key，免登录 |
| GET | [`/v2/api/gptactionGetCoinPredict`](#get-v2-api-gptactiongetcoinpredict-5) | 需要 x-api-key，免登录 |
| GET | [`/v2/api/gptactionGetMultiCoinPrice`](#get-v2-api-gptactiongetmulticoinprice-6) | 需要 x-api-key，免登录 |
| GET | [`/v2/api/gptactionGetMultiCoinPredict`](#get-v2-api-gptactiongetmulticoinpredict-7) | 需要 x-api-key，免登录 |
| GET | [`/v2/api/gptactionGetNftList`](#get-v2-api-gptactiongetnftlist-8) | 需要 x-api-key，免登录 |
| GET | [`/v2/api/gptactionGetNftInfo`](#get-v2-api-gptactiongetnftinfo-9) | 需要 x-api-key，免登录 |
| GET | [`/v2/api/gptactionGetPurchaseRecommendation`](#get-v2-api-gptactiongetpurchaserecommendation-10) | 需要 x-api-key，免登录 |
| GET | [`/v2/api/gptactionGetCurrencyComparison`](#get-v2-api-gptactiongetcurrencycomparison-11) | 需要 x-api-key，免登录 |
| GET | [`/v2/api/gptactionGetNftComparison`](#get-v2-api-gptactiongetnftcomparison-12) | 需要 x-api-key，免登录 |
| GET | [`/v2/api/gptactionGetHashDataForSwap`](#get-v2-api-gptactiongethashdataforswap-13) | 需要 x-api-key，免登录 |
| GET | [`/v2/api/gptactionBroadcastSwap`](#get-v2-api-gptactionbroadcastswap-14) | 需要 x-api-key，免登录 |

## 详情

### GET `/v2/api/gptactionGetCoinKline`

<a id="get-v2-api-gptactiongetcoinkline-1"></a>

- 路由键：`gptactionGetCoinKline`
- 鉴权：需要 x-api-key，免登录
- v1 镜像：`GET /v1/api/gptactionGetCoinKline`（同一 handler；v1 不校验 `x-api-key`）
- 实现：`ml4gp/ml4gp/controller/gptaction_api.py:48` `ml4gp.controller.gptaction_api.gptaction_get_coin_kline`
- 响应：JSON 信封 `{code,message,status,data}`
- `data` 字面量键：`content`

**Query**

| 字段 | 读取方式 | 默认值 |
| --- | --- | --- |
| `symbol` | `.get` | 无 |

### GET `/v2/api/gptactionGetCoinTrading`

<a id="get-v2-api-gptactiongetcointrading-2"></a>

- 路由键：`gptactionGetCoinTrading`
- 鉴权：需要 x-api-key，免登录
- v1 镜像：`GET /v1/api/gptactionGetCoinTrading`（同一 handler；v1 不校验 `x-api-key`）
- 实现：`ml4gp/ml4gp/controller/gptaction_api.py:61` `ml4gp.controller.gptaction_api.gptaction_get_coin_trading`
- 响应：JSON 信封 `{code,message,status,data}`
- `data` 字面量键：`content`

**Query**

| 字段 | 读取方式 | 默认值 |
| --- | --- | --- |
| `symbol` | `.get` | 无 |

### GET `/v2/api/gptactionGetCoinInfo`

<a id="get-v2-api-gptactiongetcoininfo-3"></a>

- 路由键：`gptactionGetCoinInfo`
- 鉴权：需要 x-api-key，免登录
- v1 镜像：`GET /v1/api/gptactionGetCoinInfo`（同一 handler；v1 不校验 `x-api-key`）
- 实现：`ml4gp/ml4gp/controller/gptaction_api.py:71` `ml4gp.controller.gptaction_api.gptaction_get_coin_info`
- 响应：JSON 信封 `{code,message,status,data}`
- `data` 字面量键：`content`

**Query**

| 字段 | 读取方式 | 默认值 |
| --- | --- | --- |
| `symbol` | `.get` | 无 |

### GET `/v2/api/gptactionGetGoodNews`

<a id="get-v2-api-gptactiongetgoodnews-4"></a>

- 路由键：`gptactionGetGoodNews`
- 鉴权：需要 x-api-key，免登录
- v1 镜像：`GET /v1/api/gptactionGetGoodNews`（同一 handler；v1 不校验 `x-api-key`）
- 实现：`ml4gp/ml4gp/controller/gptaction_api.py:84` `ml4gp.controller.gptaction_api.gptaction_get_good_news`
- 响应：JSON 信封 `{code,message,status,data}`
- `data` 字面量键：`content`

**Query**

| 字段 | 读取方式 | 默认值 |
| --- | --- | --- |
| `symbol` | `.get` | 无 |

### GET `/v2/api/gptactionGetCoinPredict`

<a id="get-v2-api-gptactiongetcoinpredict-5"></a>

- 路由键：`gptactionGetCoinPredict`
- 鉴权：需要 x-api-key，免登录
- v1 镜像：`GET /v1/api/gptactionGetCoinPredict`（同一 handler；v1 不校验 `x-api-key`）
- 实现：`ml4gp/ml4gp/controller/gptaction_api.py:95` `ml4gp.controller.gptaction_api.gptaction_get_coin_predict`
- 响应：JSON 信封 `{code,message,status,data}`
- `data` 字面量键：`content`

**Query**

| 字段 | 读取方式 | 默认值 |
| --- | --- | --- |
| `symbol` | `.get` | 无 |

### GET `/v2/api/gptactionGetMultiCoinPrice`

<a id="get-v2-api-gptactiongetmulticoinprice-6"></a>

- 路由键：`gptactionGetMultiCoinPrice`
- 鉴权：需要 x-api-key，免登录
- v1 镜像：`GET /v1/api/gptactionGetMultiCoinPrice`（同一 handler；v1 不校验 `x-api-key`）
- 实现：`ml4gp/ml4gp/controller/gptaction_api.py:107` `ml4gp.controller.gptaction_api.gptaction_get_multi_coin_price`
- 响应：JSON 信封 `{code,message,status,data}`
- `data` 字面量键：`content`

**Query**

| 字段 | 读取方式 | 默认值 |
| --- | --- | --- |
| `symbols` | `.get` | 无 |

### GET `/v2/api/gptactionGetMultiCoinPredict`

<a id="get-v2-api-gptactiongetmulticoinpredict-7"></a>

- 路由键：`gptactionGetMultiCoinPredict`
- 鉴权：需要 x-api-key，免登录
- v1 镜像：`GET /v1/api/gptactionGetMultiCoinPredict`（同一 handler；v1 不校验 `x-api-key`）
- 实现：`ml4gp/ml4gp/controller/gptaction_api.py:122` `ml4gp.controller.gptaction_api.gptaction_get_multi_coin_predict`
- 响应：JSON 信封 `{code,message,status,data}`
- `data` 字面量键：`content`

**Query**

| 字段 | 读取方式 | 默认值 |
| --- | --- | --- |
| `symbols` | `.get` | 无 |

### GET `/v2/api/gptactionGetNftList`

<a id="get-v2-api-gptactiongetnftlist-8"></a>

- 路由键：`gptactionGetNftList`
- 鉴权：需要 x-api-key，免登录
- v1 镜像：`GET /v1/api/gptactionGetNftList`（同一 handler；v1 不校验 `x-api-key`）
- 实现：`ml4gp/ml4gp/controller/gptaction_api.py:138` `ml4gp.controller.gptaction_api.gptaction_get_nft_list`
- 响应：JSON 信封 `{code,message,status,data}`
- `data` 字面量键：`content`

**Query**

| 字段 | 读取方式 | 默认值 |
| --- | --- | --- |
| `collection` | `.get` | 无 |

### GET `/v2/api/gptactionGetNftInfo`

<a id="get-v2-api-gptactiongetnftinfo-9"></a>

- 路由键：`gptactionGetNftInfo`
- 鉴权：需要 x-api-key，免登录
- v1 镜像：`GET /v1/api/gptactionGetNftInfo`（同一 handler；v1 不校验 `x-api-key`）
- 实现：`ml4gp/ml4gp/controller/gptaction_api.py:156` `ml4gp.controller.gptaction_api.gptaction_get_nft_info`
- 响应：JSON 信封 `{code,message,status,data}`
- `data` 字面量键：`content`

**Query**

| 字段 | 读取方式 | 默认值 |
| --- | --- | --- |
| `collection` | `.get` | 无 |
| `tokenid` | `.get` | 无 |

### GET `/v2/api/gptactionGetPurchaseRecommendation`

<a id="get-v2-api-gptactiongetpurchaserecommendation-10"></a>

- 路由键：`gptactionGetPurchaseRecommendation`
- 鉴权：需要 x-api-key，免登录
- v1 镜像：`GET /v1/api/gptactionGetPurchaseRecommendation`（同一 handler；v1 不校验 `x-api-key`）
- 实现：`ml4gp/ml4gp/controller/gptaction_api.py:165` `ml4gp.controller.gptaction_api.gptaction_get_purchase_recommendation`
- 响应：JSON 信封 `{code,message,status,data}`
- `data` 字面量键：`content`

**Query**

| 字段 | 读取方式 | 默认值 |
| --- | --- | --- |
| `collection` | `.get` | 无 |
| `features` | `.get` | 无 |
| `price` | `.get` | 无 |

### GET `/v2/api/gptactionGetCurrencyComparison`

<a id="get-v2-api-gptactiongetcurrencycomparison-11"></a>

- 路由键：`gptactionGetCurrencyComparison`
- 鉴权：需要 x-api-key，免登录
- v1 镜像：`GET /v1/api/gptactionGetCurrencyComparison`（同一 handler；v1 不校验 `x-api-key`）
- 实现：`ml4gp/ml4gp/controller/gptaction_api.py:175` `ml4gp.controller.gptaction_api.gptaction_get_currency_comparison`
- 响应：JSON 信封 `{code,message,status,data}`
- `data` 字面量键：`content`

**Query**

| 字段 | 读取方式 | 默认值 |
| --- | --- | --- |
| `coin1` | `.get` | 无 |
| `coin2` | `.get` | 无 |

### GET `/v2/api/gptactionGetNftComparison`

<a id="get-v2-api-gptactiongetnftcomparison-12"></a>

- 路由键：`gptactionGetNftComparison`
- 鉴权：需要 x-api-key，免登录
- v1 镜像：`GET /v1/api/gptactionGetNftComparison`（同一 handler；v1 不校验 `x-api-key`）
- 实现：`ml4gp/ml4gp/controller/gptaction_api.py:184` `ml4gp.controller.gptaction_api.gptaction_get_nft_comparison`
- 响应：JSON 信封 `{code,message,status,data}`
- `data` 字面量键：`content`

**Query**

| 字段 | 读取方式 | 默认值 |
| --- | --- | --- |
| `collection_1` | `.get` | 无 |
| `collection_2` | `.get` | 无 |

### GET `/v2/api/gptactionGetHashDataForSwap`

<a id="get-v2-api-gptactiongethashdataforswap-13"></a>

- 路由键：`gptactionGetHashDataForSwap`
- 鉴权：需要 x-api-key，免登录
- v1 镜像：`GET /v1/api/gptactionGetHashDataForSwap`（同一 handler；v1 不校验 `x-api-key`）
- 实现：`ml4gp/ml4gp/controller/gptaction_api.py:194` `ml4gp.controller.gptaction_api.gptaction_get_hash_data_for_swap`
- 响应：JSON 信封 `{code,message,status,data}`
- `data` 字面量键：`to_be_signed_data`

**Query**

| 字段 | 读取方式 | 默认值 |
| --- | --- | --- |
| `from_token` | `.get` | 无 |
| `from_token_amount` | `.get` | 无 |
| `to_token` | `.get` | 无 |
| `to_token_amount` | `.get` | 无 |

### GET `/v2/api/gptactionBroadcastSwap`

<a id="get-v2-api-gptactionbroadcastswap-14"></a>

- 路由键：`gptactionBroadcastSwap`
- 鉴权：需要 x-api-key，免登录
- v1 镜像：`GET /v1/api/gptactionBroadcastSwap`（同一 handler；v1 不校验 `x-api-key`）
- 实现：`ml4gp/ml4gp/controller/gptaction_api.py:211` `ml4gp.controller.gptaction_api.gptaction_broadcast_swap`
- 响应：JSON 信封 `{code,message,status,data}`
- `data` 字面量键：`msg`

**Query**

| 字段 | 读取方式 | 默认值 |
| --- | --- | --- |
| `signed_data` | `.get` | 无 |
