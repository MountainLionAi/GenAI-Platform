# 兑换 Swap

本模块 17 个已挂载接口。通用约定见 [README](README.md)。

## 索引

| 方法 | 路径 | 鉴权 |
| --- | --- | --- |
| GET | [`/v2/api/swap/getQuoteData`](#get-v2-api-swap-getquotedata-1) | 需要 x-api-key，免登录 |
| POST | [`/v2/api/swap/getSwapData`](#post-v2-api-swap-getswapdata-2) | 需要 x-api-key，免登录 |
| POST | [`/v2/api/swap/addTransData`](#post-v2-api-swap-addtransdata-3) | 需要 x-api-key，免登录 |
| GET | [`/v2/api/getSwapInfoBySymbol`](#get-v2-api-getswapinfobysymbol-4) | 需要 x-api-key，免登录 |
| GET | [`/v2/api/getWalletAssets`](#get-v2-api-getwalletassets-5) | 需要 x-api-key，免登录 |
| POST | [`/v2/api/getTransferData`](#post-v2-api-gettransferdata-6) | 需要 x-api-key，免登录 |
| GET | [`/v2/api/swap/getCoinList`](#get-v2-api-swap-getcoinlist-7) | 需要 x-api-key，免登录 |
| POST | [`/v2/api/getBaseInfo`](#post-v2-api-getbaseinfo-8) | 需要 x-api-key，免登录 |
| POST | [`/v2/api/multiQuote`](#post-v2-api-multiquote-9) | 需要 x-api-key，免登录 |
| POST | [`/v2/api/commonSwap`](#post-v2-api-commonswap-10) | 需要 x-api-key，v2 免登录；v1 需登录 |
| POST | [`/v2/api/queryBlackList`](#post-v2-api-queryblacklist-11) | 需要 x-api-key，需登录 |
| POST | [`/v2/api/exchangeRecord/addTransData`](#post-v2-api-exchangerecord-addtransdata-12) | 需要 x-api-key，v2 免登录；v1 需登录 |
| POST | [`/v2/api/exchangeRecord/getTransData`](#post-v2-api-exchangerecord-gettransdata-13) | 需要 x-api-key，v2 免登录；v1 需登录 |
| POST | [`/v2/api/exchangeRecord/getTransDetail`](#post-v2-api-exchangerecord-gettransdetail-14) | 需要 x-api-key，v2 免登录；v1 需登录 |
| GET | [`/v2/api/recommendSwapQuestion`](#get-v2-api-recommendswapquestion-15) | 需要 x-api-key，免登录 |
| POST | [`/v2/api/summaryForSwap`](#post-v2-api-summaryforswap-16) | 需要 x-api-key，免登录 |
| GET | [`/v2/api/hotTokenForSwap`](#get-v2-api-hottokenforswap-17) | 需要 x-api-key，免登录 |

## 详情

### GET `/v2/api/swap/getQuoteData`

<a id="get-v2-api-swap-getquotedata-1"></a>

- 路由键：`getQuoteData`
- 鉴权：需要 x-api-key，免登录
- v1 镜像：`GET /v1/api/swap/getQuoteData`（同一 handler；v1 不校验 `x-api-key`）
- 实现：`ml4gp/ml4gp/controller/swap.py:24` `ml4gp.controller.swap.get_quote_data`
- 响应：JSON 信封 `{code,message,status,data}`

**Query**

| 字段 | 读取方式 | 默认值 |
| --- | --- | --- |
| `fromTokenAddress` | `.get` | 无 |
| `toTokenAddress` | `.get` | 无 |
| `fromTokenAmount` | `.get` | 无 |
| `fromChain` | `.get` | 无 |
| `toChain` | `.get` | 无 |
| `walletAddress` | `.get` | `0x4d9dd69be09Ba79fC1cDFD27E579F7c622Bd072c` |
| `walletType` | `.get` | `WEB3` |

### POST `/v2/api/swap/getSwapData`

<a id="post-v2-api-swap-getswapdata-2"></a>

- 路由键：`getSwapData`
- 鉴权：需要 x-api-key，免登录
- v1 镜像：`POST /v1/api/swap/getSwapData`（同一 handler；v1 不校验 `x-api-key`）
- 实现：`ml4gp/ml4gp/controller/swap.py:51` `ml4gp.controller.swap.get_swap_data`
- 响应：JSON 信封 `{code,message,status,data}`

**JSON Body**

| 字段 | 读取方式 | 默认值 |
| --- | --- | --- |
| `quoteInfo` | `.get` | 无 |
| `walletAddress` | `.get` | 无 |
| `toAddress` | `.get` | 无 |

### POST `/v2/api/swap/addTransData`

<a id="post-v2-api-swap-addtransdata-3"></a>

- 路由键：`addTransData`
- 鉴权：需要 x-api-key，免登录
- v1 镜像：`POST /v1/api/swap/addTransData`（同一 handler；v1 不校验 `x-api-key`）
- 实现：`ml4gp/ml4gp/controller/swap.py:76` `ml4gp.controller.swap.add_trans_data`
- 响应：JSON 信封 `{code,message,status,data}`

**JSON Body**

| 字段 | 读取方式 | 默认值 |
| --- | --- | --- |
| `language` | `.get` | 无 |
| `hash` | `.get` | 无 |
| `from_chain_id` | `.get` | 无 |
| `from_token_amount` | `.get` | 无 |
| `to_chain_id` | `.get` | 无 |
| `from_address` | `.get` | 无 |
| `from_token_address` | `.get` | 无 |
| `timestamp` | `.get` | 无 |
| `to_token_address` | `.get` | 无 |
| `to_token_amount` | `.get` | 无 |
| `estimated_time` | `.get` | 无 |
| `equipment_no` | `.get` | 无 |
| `from_chain` | `.get` | 无 |
| `to_chain` | `.get` | 无 |
| `source` | `.get` | 无 |
| `slippage` | `.get` | 无 |
| `dex_name` | `.get` | 无 |
| `order_id` | `.get` | 无 |
| `order_type` | `.get` | 无 |
| `transfer_data` | `.get` | 无 |
| `to_address` | `.get` | 无 |
| `to_token_amount_wd` | `.get` | 无 |
| `is_no_gas` | `.get` | 无 |
| `utm_source` | `.get` | 无 |
| `device_no` | `.get` | 无 |

### GET `/v2/api/getSwapInfoBySymbol`

<a id="get-v2-api-getswapinfobysymbol-4"></a>

- 路由键：`getSwapInfoBySymbol`
- 鉴权：需要 x-api-key，免登录
- v1 镜像：`GET /v1/api/getSwapInfoBySymbol`（同一 handler；v1 不校验 `x-api-key`）
- 实现：`ml4gp/ml4gp/controller/swap.py:96` `ml4gp.controller.swap.get_swap_info_by_coin`
- 响应：JSON 信封 `{code,message,status,data}`

**Query**

| 字段 | 读取方式 | 默认值 |
| --- | --- | --- |
| `coinCode` | `.get` | 无 |
| `token` | `.get` | 无 |
| `language` | `.get` | 无 |

### GET `/v2/api/getWalletAssets`

<a id="get-v2-api-getwalletassets-5"></a>

- 路由键：`getWalletAssets`
- 鉴权：需要 x-api-key，免登录
- v1 镜像：`GET /v1/api/getWalletAssets`（同一 handler；v1 不校验 `x-api-key`）
- 实现：`ml4gp/ml4gp/controller/swap.py:106` `ml4gp.controller.swap.get_wallet_assets`
- 响应：JSON 信封 `{code,message,status,data}`

**Query**

| 字段 | 读取方式 | 默认值 |
| --- | --- | --- |
| `address` | `.get` | `` |
| `chain_id` | `.get` | `` |

### POST `/v2/api/getTransferData`

<a id="post-v2-api-gettransferdata-6"></a>

- 路由键：`getTransferData`
- 鉴权：需要 x-api-key，免登录
- v1 镜像：`POST /v1/api/getTransferData`（同一 handler；v1 不校验 `x-api-key`）
- 实现：`ml4gp/ml4gp/controller/swap.py:115` `ml4gp.controller.swap.get_transfer_data`
- 响应：JSON 信封 `{code,message,status,data}`

**JSON Body**

| 字段 | 读取方式 | 默认值 |
| --- | --- | --- |
| `fromAddress` | `.get` | `` |
| `toAddress` | `.get` | `` |
| `fromAmount` | `.get` | `` |
| `chainId` | `.get` | `` |
| `tokenAddress` | `.get` | `` |

### GET `/v2/api/swap/getCoinList`

<a id="get-v2-api-swap-getcoinlist-7"></a>

- 路由键：`getSwapCoinList`
- 鉴权：需要 x-api-key，免登录
- v1 镜像：`GET /v1/api/swap/getCoinList`（同一 handler；v1 不校验 `x-api-key`）
- 实现：`ml4gp/ml4gp/controller/swap.py:128` `ml4gp.controller.swap.get_coin_list_v2`
- 响应：JSON 信封 `{code,message,status,data}`

无额外 query/body 字段（或参数在更下游动态拼装）。

### POST `/v2/api/getBaseInfo`

<a id="post-v2-api-getbaseinfo-8"></a>

- 路由键：`pathGetBaseInfo`
- 鉴权：需要 x-api-key，免登录
- v1 镜像：`POST /v1/api/getBaseInfo`（同一 handler；v1 不校验 `x-api-key`）
- 实现：`ml4gp/ml4gp/controller/path_swap.py:14` `ml4gp.controller.path_swap.get_base_info`
- 响应：JSON 信封 `{code,message,status,data}`

**JSON Body**

| 字段 | 读取方式 | 默认值 |
| --- | --- | --- |
| `chain` | `.get` | `` |

### POST `/v2/api/multiQuote`

<a id="post-v2-api-multiquote-9"></a>

- 路由键：`pathMultiQuote`
- 鉴权：需要 x-api-key，免登录
- v1 镜像：`POST /v1/api/multiQuote`（同一 handler；v1 不校验 `x-api-key`）
- 实现：`ml4gp/ml4gp/controller/path_swap.py:23` `ml4gp.controller.path_swap.multi_quote`
- 响应：JSON 信封 `{code,message,status,data}`

**JSON Body**

| 字段 | 读取方式 | 默认值 |
| --- | --- | --- |
| `fromTokenAddress` | 下标，缺失会抛错 | 必有 |
| `fromTokenChain` | 下标，缺失会抛错 | 必有 |
| `fromTokenAmount` | 下标，缺失会抛错 | 必有 |

### POST `/v2/api/commonSwap`

<a id="post-v2-api-commonswap-10"></a>

- 路由键：`pathCommonSwap`
- 鉴权：需要 x-api-key，v2 免登录；v1 需登录
- v1 镜像：`POST /v1/api/commonSwap`（同一 handler；v1 不校验 `x-api-key`）
- 实现：`ml4gp/ml4gp/controller/path_swap.py:69` `ml4gp.controller.path_swap.common_swap`
- 响应：JSON 信封 `{code,message,status,data}`

**JSON Body**

| 字段 | 读取方式 | 默认值 |
| --- | --- | --- |
| `needMarkdown` | `.get` | `0` |
| `language` | `.get` | `en` |

### POST `/v2/api/queryBlackList`

<a id="post-v2-api-queryblacklist-11"></a>

- 路由键：`pathQueryBlackList`
- 鉴权：需要 x-api-key，需登录
- v1 镜像：`POST /v1/api/queryBlackList`（同一 handler；v1 不校验 `x-api-key`）
- 实现：`ml4gp/ml4gp/controller/path_swap.py:86` `ml4gp.controller.path_swap.query_black_list`
- 响应：JSON 信封 `{code,message,status,data}`

**JSON Body**

读取整包 `request.json`，字段在下游服务里拆，调用时按业务传 JSON 对象。

### POST `/v2/api/exchangeRecord/addTransData`

<a id="post-v2-api-exchangerecord-addtransdata-12"></a>

- 路由键：`pathAddTransData`
- 鉴权：需要 x-api-key，v2 免登录；v1 需登录
- v1 镜像：`POST /v1/api/exchangeRecord/addTransData`（同一 handler；v1 不校验 `x-api-key`）
- 实现：`ml4gp/ml4gp/controller/path_swap.py:97` `ml4gp.controller.path_swap.add_trans_data`
- 响应：JSON 信封 `{code,message,status,data}`

**JSON Body**

读取整包 `request.json`，字段在下游服务里拆，调用时按业务传 JSON 对象。

### POST `/v2/api/exchangeRecord/getTransData`

<a id="post-v2-api-exchangerecord-gettransdata-13"></a>

- 路由键：`pathGetTransData`
- 鉴权：需要 x-api-key，v2 免登录；v1 需登录
- v1 镜像：`POST /v1/api/exchangeRecord/getTransData`（同一 handler；v1 不校验 `x-api-key`）
- 实现：`ml4gp/ml4gp/controller/path_swap.py:114` `ml4gp.controller.path_swap.get_trans_data`
- 响应：JSON 信封 `{code,message,status,data}`

**JSON Body**

读取整包 `request.json`，字段在下游服务里拆，调用时按业务传 JSON 对象。

### POST `/v2/api/exchangeRecord/getTransDetail`

<a id="post-v2-api-exchangerecord-gettransdetail-14"></a>

- 路由键：`pathGetTransDetail`
- 鉴权：需要 x-api-key，v2 免登录；v1 需登录
- v1 镜像：`POST /v1/api/exchangeRecord/getTransDetail`（同一 handler；v1 不校验 `x-api-key`）
- 实现：`ml4gp/ml4gp/controller/path_swap.py:126` `ml4gp.controller.path_swap.get_trans_detail`
- 响应：JSON 信封 `{code,message,status,data}`

**JSON Body**

读取整包 `request.json`，字段在下游服务里拆，调用时按业务传 JSON 对象。

### GET `/v2/api/recommendSwapQuestion`

<a id="get-v2-api-recommendswapquestion-15"></a>

- 路由键：`recommendQuestion`
- 鉴权：需要 x-api-key，免登录
- v1 镜像：`GET /v1/api/recommendSwapQuestion`（同一 handler；v1 不校验 `x-api-key`）
- 实现：`ml4gp/ml4gp/controller/recommend_token_question.py:22` `ml4gp.controller.recommend_token_question.question_for_recommend_swap`
- 响应：JSON 信封 `{code,message,status,data}`

**Query**

| 字段 | 读取方式 | 默认值 |
| --- | --- | --- |
| `language` | `.get` | `en` |
| `scene` | `.get` | `default` |

### POST `/v2/api/summaryForSwap`

<a id="post-v2-api-summaryforswap-16"></a>

- 路由键：`summaryForSwap`
- 鉴权：需要 x-api-key，免登录
- v1 镜像：`POST /v1/api/summaryForSwap`（同一 handler；v1 不校验 `x-api-key`）
- 实现：`ml4gp/ml4gp/controller/recommend_token_question.py:146` `ml4gp.controller.recommend_token_question.summary_for_recommend_swap_stream`
- 响应：流式（SSE / chunk）
- 显式错误码：`PARAMS_ERROR`

**JSON Body**

| 字段 | 读取方式 | 默认值 |
| --- | --- | --- |
| `symbol` | `.get` | `` |
| `language` | `.get` | `en` |
| `tokenInfo` | `.get` | `` |
| `user_query` | `.get` | `哪个币种当前有比较大的上涨潜力？` |

### GET `/v2/api/hotTokenForSwap`

<a id="get-v2-api-hottokenforswap-17"></a>

- 路由键：`hotTokenForSwap`
- 鉴权：需要 x-api-key，免登录
- v1 镜像：`GET /v1/api/hotTokenForSwap`（同一 handler；v1 不校验 `x-api-key`）
- 实现：`ml4gp/ml4gp/controller/recommend_token_question.py:175` `ml4gp.controller.recommend_token_question.hot_token_for_recommend_swap`
- 响应：JSON 信封 `{code,message,status,data}`

**Query**

| 字段 | 读取方式 | 默认值 |
| --- | --- | --- |
| `language` | `.get` | `en` |
