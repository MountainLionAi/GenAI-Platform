# 数据看板

本模块 31 个已挂载接口。通用约定见 [README](README.md)。

## 索引

| 方法 | 路径 | 鉴权 |
| --- | --- | --- |
| GET | [`/v2/api/getAirdropLists`](#get-v2-api-getairdroplists-1) | 需要 x-api-key，免登录 |
| GET | [`/v2/api/getAirdropDetail`](#get-v2-api-getairdropdetail-2) | 需要 x-api-key，免登录 |
| GET | [`/v2/api/getListInfo`](#get-v2-api-getlistinfo-3) | 需要 x-api-key，免登录 |
| POST | [`/v2/api/getAIScoreInfo`](#post-v2-api-getaiscoreinfo-4) | 需要 x-api-key，免登录 |
| POST | [`/v2/api/getTopGainerInfo`](#post-v2-api-gettopgainerinfo-5) | 需要 x-api-key，免登录 |
| GET | [`/v2/api/getPopThemeInfo`](#get-v2-api-getpopthemeinfo-6) | 需要 x-api-key，免登录 |
| POST | [`/v2/api/getSmartTopBuyInfo`](#post-v2-api-getsmarttopbuyinfo-7) | 需要 x-api-key，免登录 |
| POST | [`/v2/api/getTopKOLCallInfo`](#post-v2-api-gettopkolcallinfo-8) | 需要 x-api-key，免登录 |
| POST | [`/v2/api/getTopVCHoldInfo`](#post-v2-api-gettopvcholdinfo-9) | 需要 x-api-key，免登录 |
| GET | [`/v2/api/getDashboardSupCategory`](#get-v2-api-getdashboardsupcategory-10) | 需要 x-api-key，免登录 |
| GET | [`/v2/api/getDashboardSupChain`](#get-v2-api-getdashboardsupchain-11) | 需要 x-api-key，免登录 |
| GET | [`/v2/api/getDashboardSupExchange`](#get-v2-api-getdashboardsupexchange-12) | 需要 x-api-key，免登录 |
| GET | [`/v2/api/getTotalTokens`](#get-v2-api-gettotaltokens-13) | 需要 x-api-key，免登录 |
| GET | [`/v2/api/meme/list`](#get-v2-api-meme-list-14) | 需要 x-api-key，免登录 |
| GET | [`/v2/api/symbolSearch`](#get-v2-api-symbolsearch-15) | 需要 x-api-key，免登录 |
| GET | [`/v2/api/getTweetInfo`](#get-v2-api-gettweetinfo-16) | 需要 x-api-key，免登录 |
| GET | [`/v2/api/getTweetConclusion`](#get-v2-api-gettweetconclusion-17) | 需要 x-api-key，需登录 |
| GET | [`/v2/api/getDashboardKline`](#get-v2-api-getdashboardkline-18) | 需要 x-api-key，免登录 |
| GET | [`/v2/api/getSupportChainList`](#get-v2-api-getsupportchainlist-19) | 需要 x-api-key，免登录 |
| GET | [`/v2/api/getDataByType`](#get-v2-api-getdatabytype-20) | 需要 x-api-key，免登录 |
| GET | [`/v2/api/getTokenUnlock`](#get-v2-api-gettokenunlock-21) | 需要 x-api-key，免登录 |
| GET | [`/v2/api/getOnChainSum`](#get-v2-api-getonchainsum-22) | 需要 x-api-key，免登录 |
| GET | [`/v2/api/getTWList`](#get-v2-api-gettwlist-23) | 需要 x-api-key，免登录 |
| GET | [`/v2/api/searchTWList`](#get-v2-api-searchtwlist-24) | 需要 x-api-key，免登录 |
| GET | [`/v2/api/dashboardAnalysis`](#get-v2-api-dashboardanalysis-25) | 需要 x-api-key，免登录 |
| GET | [`/v2/api/getOnChainModule`](#get-v2-api-getonchainmodule-26) | 需要 x-api-key，免登录 |
| GET | [`/v2/api/getTradeAnalysis`](#get-v2-api-gettradeanalysis-27) | 需要 x-api-key，免登录 |
| GET | [`/v2/api/dashboard/token/info`](#get-v2-api-dashboard-token-info-28) | 需要 x-api-key，免登录 |
| GET | [`/v2/api/getBtcDataByType`](#get-v2-api-getbtcdatabytype-29) | 需要 x-api-key，免登录 |
| GET | [`/v2/api/dashboard/token/search`](#get-v2-api-dashboard-token-search-30) | 需要 x-api-key，v2 需登录；v1 免登录 |
| POST | [`/v2/api/dashboard/detail/qrcode/generate`](#post-v2-api-dashboard-detail-qrcode-generate-31) | 需要 x-api-key，v2 免登录；v1 需登录 |

## 详情

### GET `/v2/api/getAirdropLists`

<a id="get-v2-api-getairdroplists-1"></a>

- 路由键：`getAirdropList`
- 鉴权：需要 x-api-key，免登录
- v1 镜像：`GET /v1/api/getAirdropLists`（同一 handler；v1 不校验 `x-api-key`）
- 实现：`ml4gp/ml4gp/controller/airdrop.py:9` `ml4gp.controller.airdrop.get_airdrop_lists`
- 响应：JSON 信封 `{code,message,status,data}`

**Query**

| 字段 | 读取方式 | 默认值 |
| --- | --- | --- |
| `language` | `.get` | `en` |
| `status` | `.get` | `Latest` |
| `category` | `.get` | `` |
| `name` | `.get` | `` |
| `pageSize` | `.get` | `100` |
| `pageNum` | `.get` | `1` |

### GET `/v2/api/getAirdropDetail`

<a id="get-v2-api-getairdropdetail-2"></a>

- 路由键：`getAirdropDetail`
- 鉴权：需要 x-api-key，免登录
- v1 镜像：`GET /v1/api/getAirdropDetail`（同一 handler；v1 不校验 `x-api-key`）
- 实现：`ml4gp/ml4gp/controller/airdrop.py:21` `ml4gp.controller.airdrop.get_airdrop_detail`
- 响应：JSON 信封 `{code,message,status,data}`
- 显式错误码：`PARAMS_ERROR`

**Query**

| 字段 | 读取方式 | 默认值 |
| --- | --- | --- |
| `language` | `.get` | `en` |
| `airdropId` | `.get` | `` |

### GET `/v2/api/getListInfo`

<a id="get-v2-api-getlistinfo-3"></a>

- 路由键：`getListInfo`
- 鉴权：需要 x-api-key，免登录
- v1 镜像：`GET /v1/api/getListInfo`（同一 handler；v1 不校验 `x-api-key`）
- 实现：`ml4gp/ml4gp/controller/dashboard.py:30` `ml4gp.controller.dashboard.mulit_list_info`
- 响应：JSON 信封 `{code,message,status,data}`

**Query**

| 字段 | 读取方式 | 默认值 |
| --- | --- | --- |
| `type` | `.get` | `old` |
| `page` | `.get` | 无 |
| `limit` | `.get` | 无 |

### POST `/v2/api/getAIScoreInfo`

<a id="post-v2-api-getaiscoreinfo-4"></a>

- 路由键：`getAIScoreInfo`
- 鉴权：需要 x-api-key，免登录
- v1 镜像：`POST /v1/api/getAIScoreInfo`（同一 handler；v1 不校验 `x-api-key`）
- 实现：`ml4gp/ml4gp/controller/dashboard.py:145` `ml4gp.controller.dashboard.get_ai_score`
- 响应：JSON 信封 `{code,message,status,data}`

**JSON Body**

| 字段 | 读取方式 | 默认值 |
| --- | --- | --- |
| `filter` | `.get` | `` |
| `keyword` | `.get` | `` |
| `limit` | `.get` | `100` |
| `page` | `.get` | `1` |

### POST `/v2/api/getTopGainerInfo`

<a id="post-v2-api-gettopgainerinfo-5"></a>

- 路由键：`getTopGainerInfo`
- 鉴权：需要 x-api-key，免登录
- v1 镜像：`POST /v1/api/getTopGainerInfo`（同一 handler；v1 不校验 `x-api-key`）
- 实现：`ml4gp/ml4gp/controller/dashboard.py:161` `ml4gp.controller.dashboard.get_top_gainer`
- 响应：JSON 信封 `{code,message,status,data}`

**JSON Body**

| 字段 | 读取方式 | 默认值 |
| --- | --- | --- |
| `filter` | `.get` | `` |
| `keyword` | `.get` | `` |
| `limit` | `.get` | `100` |
| `page` | `.get` | `1` |

### GET `/v2/api/getPopThemeInfo`

<a id="get-v2-api-getpopthemeinfo-6"></a>

- 路由键：`getPopThemeInfo`
- 鉴权：需要 x-api-key，免登录
- v1 镜像：`GET /v1/api/getPopThemeInfo`（同一 handler；v1 不校验 `x-api-key`）
- 实现：`ml4gp/ml4gp/controller/dashboard.py:177` `ml4gp.controller.dashboard.get_popular_theme`
- 响应：JSON 信封 `{code,message,status,data}`

**Query**

| 字段 | 读取方式 | 默认值 |
| --- | --- | --- |
| `keyword` | `.get` | `` |

### POST `/v2/api/getSmartTopBuyInfo`

<a id="post-v2-api-getsmarttopbuyinfo-7"></a>

- 路由键：`getSmartTopBuyInfo`
- 鉴权：需要 x-api-key，免登录
- v1 镜像：`POST /v1/api/getSmartTopBuyInfo`（同一 handler；v1 不校验 `x-api-key`）
- 实现：`ml4gp/ml4gp/controller/dashboard.py:186` `ml4gp.controller.dashboard.get_smart_top_buy`
- 响应：JSON 信封 `{code,message,status,data}`

**JSON Body**

| 字段 | 读取方式 | 默认值 |
| --- | --- | --- |
| `filter` | `.get` | `` |
| `keyword` | `.get` | `` |
| `limit` | `.get` | `100` |
| `page` | `.get` | `1` |

### POST `/v2/api/getTopKOLCallInfo`

<a id="post-v2-api-gettopkolcallinfo-8"></a>

- 路由键：`getTopKOLCallInfo`
- 鉴权：需要 x-api-key，免登录
- v1 镜像：`POST /v1/api/getTopKOLCallInfo`（同一 handler；v1 不校验 `x-api-key`）
- 实现：`ml4gp/ml4gp/controller/dashboard.py:202` `ml4gp.controller.dashboard.get_tw_kol`
- 响应：JSON 信封 `{code,message,status,data}`

**JSON Body**

| 字段 | 读取方式 | 默认值 |
| --- | --- | --- |
| `filter` | `.get` | `` |
| `keyword` | `.get` | `` |
| `limit` | `.get` | `100` |
| `page` | `.get` | `1` |

### POST `/v2/api/getTopVCHoldInfo`

<a id="post-v2-api-gettopvcholdinfo-9"></a>

- 路由键：`getTopVCHoldInfo`
- 鉴权：需要 x-api-key，免登录
- v1 镜像：`POST /v1/api/getTopVCHoldInfo`（同一 handler；v1 不校验 `x-api-key`）
- 实现：`ml4gp/ml4gp/controller/dashboard.py:218` `ml4gp.controller.dashboard.get_vc_top_hold`
- 响应：JSON 信封 `{code,message,status,data}`

**JSON Body**

| 字段 | 读取方式 | 默认值 |
| --- | --- | --- |
| `filter` | `.get` | `` |
| `keyword` | `.get` | `` |
| `limit` | `.get` | `100` |
| `page` | `.get` | `1` |

### GET `/v2/api/getDashboardSupCategory`

<a id="get-v2-api-getdashboardsupcategory-10"></a>

- 路由键：`getDashboardSupCategory`
- 鉴权：需要 x-api-key，免登录
- v1 镜像：`GET /v1/api/getDashboardSupCategory`（同一 handler；v1 不校验 `x-api-key`）
- 实现：`ml4gp/ml4gp/controller/dashboard.py:234` `ml4gp.controller.dashboard.get_dashboard_support_category`
- 响应：JSON 信封 `{code,message,status,data}`

无额外 query/body 字段（或参数在更下游动态拼装）。

### GET `/v2/api/getDashboardSupChain`

<a id="get-v2-api-getdashboardsupchain-11"></a>

- 路由键：`getDashboardSupChain`
- 鉴权：需要 x-api-key，免登录
- v1 镜像：`GET /v1/api/getDashboardSupChain`（同一 handler；v1 不校验 `x-api-key`）
- 实现：`ml4gp/ml4gp/controller/dashboard.py:241` `ml4gp.controller.dashboard.get_dashboard_support_chain`
- 响应：JSON 信封 `{code,message,status,data}`

无额外 query/body 字段（或参数在更下游动态拼装）。

### GET `/v2/api/getDashboardSupExchange`

<a id="get-v2-api-getdashboardsupexchange-12"></a>

- 路由键：`getDashboardSupExchange`
- 鉴权：需要 x-api-key，免登录
- v1 镜像：`GET /v1/api/getDashboardSupExchange`（同一 handler；v1 不校验 `x-api-key`）
- 实现：`ml4gp/ml4gp/controller/dashboard.py:248` `ml4gp.controller.dashboard.get_dashboard_support_exchange`
- 响应：JSON 信封 `{code,message,status,data}`

无额外 query/body 字段（或参数在更下游动态拼装）。

### GET `/v2/api/getTotalTokens`

<a id="get-v2-api-gettotaltokens-13"></a>

- 路由键：`getTotalTokens`
- 鉴权：需要 x-api-key，免登录
- v1 镜像：`GET /v1/api/getTotalTokens`（同一 handler；v1 不校验 `x-api-key`）
- 实现：`ml4gp/ml4gp/controller/dashboard.py:255` `ml4gp.controller.dashboard.get_total_tokens`
- 响应：JSON 信封 `{code,message,status,data}`

**Query**

| 字段 | 读取方式 | 默认值 |
| --- | --- | --- |
| `page` | `.get` | `1` |
| `limit` | `.get` | `15` |
| `keyword` | `.get` | `null` |

### GET `/v2/api/meme/list`

<a id="get-v2-api-meme-list-14"></a>

- 路由键：`getMemeList`
- 鉴权：需要 x-api-key，免登录
- v1 镜像：`GET /v1/api/meme/list`（同一 handler；v1 不校验 `x-api-key`）
- 实现：`ml4gp/ml4gp/controller/meme.py:8` `ml4gp.controller.meme.get_meme_list`
- 响应：JSON 信封 `{code,message,status,data}`

无额外 query/body 字段（或参数在更下游动态拼装）。

### GET `/v2/api/symbolSearch`

<a id="get-v2-api-symbolsearch-15"></a>

- 路由键：`symbolSearch`
- 鉴权：需要 x-api-key，免登录
- v1 镜像：`GET /v1/api/symbolSearch`（同一 handler；v1 不校验 `x-api-key`）
- 实现：`ml4gp/ml4gp/controller/dashboard.py:294` `ml4gp.controller.dashboard.symbol_search`
- 响应：JSON 信封 `{code,message,status,data}`

**Query**

| 字段 | 读取方式 | 默认值 |
| --- | --- | --- |
| `symbol` | `.get` | 无 |

### GET `/v2/api/getTweetInfo`

<a id="get-v2-api-gettweetinfo-16"></a>

- 路由键：`getTweetInfo`
- 鉴权：需要 x-api-key，免登录
- v1 镜像：`GET /v1/api/getTweetInfo`（同一 handler；v1 不校验 `x-api-key`）
- 实现：`ml4gp/ml4gp/controller/dashboard.py:303` `ml4gp.controller.dashboard.get_tweet_info`
- 响应：JSON 信封 `{code,message,status,data}`

**Query**

| 字段 | 读取方式 | 默认值 |
| --- | --- | --- |
| `coinId` | `.get` | 无 |
| `sortField` | `.get` | `` |
| `page` | `.get` | `1` |
| `lan` | `.get` | 无 |
| `cache` | `.get` | `null` |
| `symbol` | `.get` | `` |
| `visitor_id` | `.get` | `` |

### GET `/v2/api/getTweetConclusion`

<a id="get-v2-api-gettweetconclusion-17"></a>

- 路由键：`getTweetConclusion`
- 鉴权：需要 x-api-key，需登录
- v1 镜像：`GET /v1/api/getTweetConclusion`（同一 handler；v1 不校验 `x-api-key`）
- 实现：`ml4gp/ml4gp/controller/dashboard.py:322` `ml4gp.controller.dashboard.get_tweet_conclusion`
- 响应：JSON 信封 `{code,message,status,data}`

**Query**

| 字段 | 读取方式 | 默认值 |
| --- | --- | --- |
| `coinId` | `.get` | 无 |
| `page` | `.get` | `1` |
| `lan` | `.get` | 无 |
| `cache` | `.get` | `null` |

### GET `/v2/api/getDashboardKline`

<a id="get-v2-api-getdashboardkline-18"></a>

- 路由键：`getDashboardKline`
- 鉴权：需要 x-api-key，免登录
- v1 镜像：`GET /v1/api/getDashboardKline`（同一 handler；v1 不校验 `x-api-key`）
- 实现：`ml4gp/ml4gp/controller/dashboard.py:335` `ml4gp.controller.dashboard.get_dashboard_kline`
- 响应：JSON 信封 `{code,message,status,data}`

**Query**

| 字段 | 读取方式 | 默认值 |
| --- | --- | --- |
| `coinId` | `.get` | 无 |
| `dateType` | `.get` | 无 |
| `chain` | `.get` | 无 |
| `tokenAddress` | `.get` | 无 |

### GET `/v2/api/getSupportChainList`

<a id="get-v2-api-getsupportchainlist-19"></a>

- 路由键：`getSupportChainList`
- 鉴权：需要 x-api-key，免登录
- v1 镜像：`GET /v1/api/getSupportChainList`（同一 handler；v1 不校验 `x-api-key`）
- 实现：`ml4gp/ml4gp/controller/dashboard.py:347` `ml4gp.controller.dashboard.get_support_chainlist_by_token`
- 响应：JSON 信封 `{code,message,status,data}`

**Query**

| 字段 | 读取方式 | 默认值 |
| --- | --- | --- |
| `coinId` | `.get` | 无 |

### GET `/v2/api/getDataByType`

<a id="get-v2-api-getdatabytype-20"></a>

- 路由键：`getDataByType`
- 鉴权：需要 x-api-key，免登录
- v1 镜像：`GET /v1/api/getDataByType`（同一 handler；v1 不校验 `x-api-key`）
- 实现：`ml4gp/ml4gp/controller/dashboard.py:358` `ml4gp.controller.dashboard.get_multi_data_flow_by_type`
- 响应：JSON 信封 `{code,message,status,data}`

**Query**

| 字段 | 读取方式 | 默认值 |
| --- | --- | --- |
| `coinId` | `.get` | 无 |
| `dateType` | `.get` | 无 |
| `chain` | `.get` | 无 |
| `tokenAddress` | `.get` | 无 |
| `eventType` | `.get` | 无 |

### GET `/v2/api/getTokenUnlock`

<a id="get-v2-api-gettokenunlock-21"></a>

- 路由键：`getTokenUnlock`
- 鉴权：需要 x-api-key，免登录
- v1 镜像：`GET /v1/api/getTokenUnlock`（同一 handler；v1 不校验 `x-api-key`）
- 实现：`ml4gp/ml4gp/controller/dashboard.py:371` `ml4gp.controller.dashboard.get_unlock_token_info`
- 响应：JSON 信封 `{code,message,status,data}`

**Query**

| 字段 | 读取方式 | 默认值 |
| --- | --- | --- |
| `coinId` | `.get` | 无 |
| `dateType` | `.get` | 无 |
| `chain` | `.get` | 无 |
| `tokenAddress` | `.get` | 无 |
| `eventType` | `.get` | 无 |

### GET `/v2/api/getOnChainSum`

<a id="get-v2-api-getonchainsum-22"></a>

- 路由键：`getOnChainSum`
- 鉴权：需要 x-api-key，免登录
- v1 镜像：`GET /v1/api/getOnChainSum`（同一 handler；v1 不校验 `x-api-key`）
- 实现：`ml4gp/ml4gp/controller/dashboard.py:409` `ml4gp.controller.dashboard.get_onchain_summary`
- 响应：JSON 信封 `{code,message,status,data}`

**Query**

| 字段 | 读取方式 | 默认值 |
| --- | --- | --- |
| `coinId` | `.get` | 无 |
| `lan` | `.get` | 无 |
| `tokenAddress` | `.get` | `null` |
| `chain` | `.get` | `null` |
| `cache` | `.get` | `null` |

### GET `/v2/api/getTWList`

<a id="get-v2-api-gettwlist-23"></a>

- 路由键：`getTWList`
- 鉴权：需要 x-api-key，免登录
- v1 镜像：`GET /v1/api/getTWList`（同一 handler；v1 不校验 `x-api-key`）
- 实现：`ml4gp/ml4gp/controller/dashboard.py:384` `ml4gp.controller.dashboard.get_tw_list`
- 响应：JSON 信封 `{code,message,status,data}`

**Query**

| 字段 | 读取方式 | 默认值 |
| --- | --- | --- |
| `coinId` | `.get` | 无 |
| `sortField` | `.get` | 无 |
| `page` | `.get` | `1` |

### GET `/v2/api/searchTWList`

<a id="get-v2-api-searchtwlist-24"></a>

- 路由键：`searchTWList`
- 鉴权：需要 x-api-key，免登录
- v1 镜像：`GET /v1/api/searchTWList`（同一 handler；v1 不校验 `x-api-key`）
- 实现：`ml4gp/ml4gp/controller/dashboard.py:425` `ml4gp.controller.dashboard.search_twitter`
- 响应：JSON 信封 `{code,message,status,data}`

**Query**

| 字段 | 读取方式 | 默认值 |
| --- | --- | --- |
| `keyword` | `.get` | 无 |
| `order` | `.get` | 无 |

### GET `/v2/api/dashboardAnalysis`

<a id="get-v2-api-dashboardanalysis-25"></a>

- 路由键：`dashboardAnalysis`
- 鉴权：需要 x-api-key，免登录
- v1 镜像：`GET /v1/api/dashboardAnalysis`（同一 handler；v1 不校验 `x-api-key`）
- 实现：`ml4gp/ml4gp/controller/dashboard_analysis.py:8` `ml4gp.controller.dashboard_analysis.dashboard_analysis`
- 响应：JSON 信封 `{code,message,status,data}`
- `data` 字面量键：`summary`, `isUnlock`

**Query**

| 字段 | 读取方式 | 默认值 |
| --- | --- | --- |
| `queryDate` | `.get` | `null` |
| `symbol` | `.get` | `null` |
| `language` | `.get` | `en` |
| `timezone` | `.get` | `Asia/Shanghai` |
| `coinId` | `.get` | `null` |
| `needRefresh` | `.get` | `0` |
| `fixedSource` | `.get` | `` |
| `visitor_id` | `.get` | `` |

### GET `/v2/api/getOnChainModule`

<a id="get-v2-api-getonchainmodule-26"></a>

- 路由键：`getOnChainModule`
- 鉴权：需要 x-api-key，免登录
- v1 镜像：`GET /v1/api/getOnChainModule`（同一 handler；v1 不校验 `x-api-key`）
- 实现：`ml4gp/ml4gp/controller/dashboard.py:442` `ml4gp.controller.dashboard.get_onchain_module`
- 响应：JSON 信封 `{code,message,status,data}`

**Query**

| 字段 | 读取方式 | 默认值 |
| --- | --- | --- |
| `coinId` | `.get` | 无 |
| `tokenAddress` | `.get` | `null` |
| `chain` | `.get` | `null` |

### GET `/v2/api/getTradeAnalysis`

<a id="get-v2-api-gettradeanalysis-27"></a>

- 路由键：`getTradeAnalysis`
- 鉴权：需要 x-api-key，免登录
- v1 镜像：`GET /v1/api/getTradeAnalysis`（同一 handler；v1 不校验 `x-api-key`）
- 实现：`ml4gp/ml4gp/controller/dashboard.py:487` `ml4gp.controller.dashboard.get_trade_analysis`
- 响应：JSON 信封 `{code,message,status,data}`

**Query**

| 字段 | 读取方式 | 默认值 |
| --- | --- | --- |
| `coinId` | `.get` | 无 |
| `lan` | `.get` | 无 |

### GET `/v2/api/dashboard/token/info`

<a id="get-v2-api-dashboard-token-info-28"></a>

symbol: 币种 例如BTC

- 路由键：`queryTokenCurrentPriceInfo`
- 鉴权：需要 x-api-key，免登录
- v1 镜像：`GET /v1/api/dashboard/token/info`（同一 handler；v1 不校验 `x-api-key`）
- 实现：`ml4gp/ml4gp/controller/dashboard.py:464` `ml4gp.controller.dashboard.query_token_current_price_info`
- 响应：JSON 信封 `{code,message,status,data}`

**Query**

| 字段 | 读取方式 | 默认值 |
| --- | --- | --- |
| `code` | `.get` | 无 |

### GET `/v2/api/getBtcDataByType`

<a id="get-v2-api-getbtcdatabytype-29"></a>

- 路由键：`getBtcDataByType`
- 鉴权：需要 x-api-key，免登录
- v1 镜像：`GET /v1/api/getBtcDataByType`（同一 handler；v1 不校验 `x-api-key`）
- 实现：`ml4gp/ml4gp/controller/dashboard.py:453` `ml4gp.controller.dashboard.get_btc_data_by_type`
- 响应：JSON 信封 `{code,message,status,data}`

**Query**

| 字段 | 读取方式 | 默认值 |
| --- | --- | --- |
| `coinId` | `.get` | 无 |
| `type` | `.get` | `0` |

### GET `/v2/api/dashboard/token/search`

<a id="get-v2-api-dashboard-token-search-30"></a>

- 路由键：`dashboardTokenSearch`
- 鉴权：需要 x-api-key，v2 需登录；v1 免登录
- v1 镜像：`GET /v1/api/dashboard/token/search`（同一 handler；v1 不校验 `x-api-key`）
- 实现：`ml4gp/ml4gp/controller/dashboard.py:497` `ml4gp.controller.dashboard.dashboard_search`
- 响应：JSON 信封 `{code,message,status,data}`

**Query**

| 字段 | 读取方式 | 默认值 |
| --- | --- | --- |
| `keyword` | `.get` | 无 |
| `page` | `.get` | `1` |
| `limit` | `.get` | `15` |
| `current_mode` | `.get` | 无 |

### POST `/v2/api/dashboard/detail/qrcode/generate`

<a id="post-v2-api-dashboard-detail-qrcode-generate-31"></a>

- 路由键：`generateDashboardDetailQrCode`
- 鉴权：需要 x-api-key，v2 免登录；v1 需登录
- v1 镜像：`POST /v1/api/dashboard/detail/qrcode/generate`（同一 handler；v1 不校验 `x-api-key`）
- 实现：`ml4gp/ml4gp/controller/dashboard.py:511` `ml4gp.controller.dashboard.generate_qrcode`
- 响应：JSON 信封 `{code,message,status,data}`

**JSON Body**

| 字段 | 读取方式 | 默认值 |
| --- | --- | --- |
| `qrcode_url` | `.get` | `` |
