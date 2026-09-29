# 行情与预测

本模块 13 个已挂载接口。通用约定见 [README](README.md)。

## 索引

| 方法 | 路径 | 鉴权 |
| --- | --- | --- |
| GET | [`/v2/api/getCoinInfo`](#get-v2-api-getcoininfo-1) | 需要 x-api-key，免登录 |
| GET | [`/v2/api/getCoinList`](#get-v2-api-getcoinlist-2) | 需要 x-api-key，免登录 |
| GET | [`/v2/api/getKlineInfo`](#get-v2-api-getklineinfo-3) | 需要 x-api-key，免登录 |
| GET | [`/v2/api/getPresetTwo`](#get-v2-api-getpresettwo-4) | 需要 x-api-key，免登录 |
| GET | [`/v2/api/getPresetThree`](#get-v2-api-getpresetthree-5) | 需要 x-api-key，免登录 |
| GET | [`/v2/api/getPredictInfo`](#get-v2-api-getpredictinfo-6) | 需要 x-api-key，免登录 |
| GET | [`/v2/api/getRealTimePrice`](#get-v2-api-getrealtimeprice-7) | 需要 x-api-key，免登录 |
| GET | [`/v2/api/getWeekPrice`](#get-v2-api-getweekprice-8) | 需要 x-api-key，免登录 |
| GET | [`/v2/api/getReportPDF`](#get-v2-api-getreportpdf-9) | 需要 x-api-key，免登录 |
| GET | [`/v2/api/getPredictPDF`](#get-v2-api-getpredictpdf-10) | 需要 x-api-key，免登录 |
| GET | [`/v2/api/getCoinSentiment`](#get-v2-api-getcoinsentiment-11) | 需要 x-api-key，免登录 |
| GET | [`/v2/api/token/ai/choose/query`](#get-v2-api-token-ai-choose-query-12) | 需要 x-api-key，v2 免登录；v1 需登录 |
| POST | [`/v2/api/trend/getTrendInfo`](#post-v2-api-trend-gettrendinfo-13) | 需要 x-api-key，v2 免登录；v1 需登录 |

## 详情

### GET `/v2/api/getCoinInfo`

<a id="get-v2-api-getcoininfo-1"></a>

- 路由键：`getCoinInfo`
- 鉴权：需要 x-api-key，免登录
- v1 镜像：`GET /v1/api/getCoinInfo`（同一 handler；v1 不校验 `x-api-key`）
- 实现：`ml4gp/ml4gp/controller/kchart.py:24` `ml4gp.controller.kchart.get_coin_info`
- 响应：JSON 信封 `{code,message,status,data}`

无额外 query/body 字段（或参数在更下游动态拼装）。

### GET `/v2/api/getCoinList`

<a id="get-v2-api-getcoinlist-2"></a>

- 路由键：`getCoinList`
- 鉴权：需要 x-api-key，免登录
- v1 镜像：`GET /v1/api/getCoinList`（同一 handler；v1 不校验 `x-api-key`）
- 实现：`ml4gp/ml4gp/controller/coin.py:8` `ml4gp.controller.coin.get_coin_list`
- 响应：JSON 信封 `{code,message,status,data}`

无额外 query/body 字段（或参数在更下游动态拼装）。

### GET `/v2/api/getKlineInfo`

<a id="get-v2-api-getklineinfo-3"></a>

- 路由键：`getKlineInfo`
- 鉴权：需要 x-api-key，免登录
- v1 镜像：`GET /v1/api/getKlineInfo`（同一 handler；v1 不校验 `x-api-key`）
- 实现：`ml4gp/ml4gp/controller/firstTask.py:71` `ml4gp.controller.firstTask.get_kline_info`
- 响应：JSON 信封 `{code,message,status,data}`

**Query**

| 字段 | 读取方式 | 默认值 |
| --- | --- | --- |
| `code` | `.get` | 无 |
| `msggroup` | `.get` | 无 |
| `language` | `.get` | 无 |

### GET `/v2/api/getPresetTwo`

<a id="get-v2-api-getpresettwo-4"></a>

- 路由键：`getPresetTwo`
- 鉴权：需要 x-api-key，免登录
- v1 镜像：`GET /v1/api/getPresetTwo`（同一 handler；v1 不校验 `x-api-key`）
- 实现：`ml4gp/ml4gp/controller/kchart.py:43` `ml4gp.controller.kchart.get_preset_two`
- 响应：JSON 信封 `{code,message,status,data}`

**Query**

| 字段 | 读取方式 | 默认值 |
| --- | --- | --- |
| `code` | 下标，缺失会抛错 | 必有 |
| `msggroup` | 下标，缺失会抛错 | 必有 |
| `language` | 下标，缺失会抛错 | 必有 |

### GET `/v2/api/getPresetThree`

<a id="get-v2-api-getpresetthree-5"></a>

- 路由键：`getPresetThree`
- 鉴权：需要 x-api-key，免登录
- v1 镜像：`GET /v1/api/getPresetThree`（同一 handler；v1 不校验 `x-api-key`）
- 实现：`ml4gp/ml4gp/controller/kchart.py:57` `ml4gp.controller.kchart.get_preset_three`
- 响应：JSON 信封 `{code,message,status,data}`

**Query**

| 字段 | 读取方式 | 默认值 |
| --- | --- | --- |
| `code` | 下标，缺失会抛错 | 必有 |
| `msggroup` | 下标，缺失会抛错 | 必有 |
| `language` | 下标，缺失会抛错 | 必有 |

### GET `/v2/api/getPredictInfo`

<a id="get-v2-api-getpredictinfo-6"></a>

- 路由键：`getPredictInfo`
- 鉴权：需要 x-api-key，免登录
- v1 镜像：`GET /v1/api/getPredictInfo`（同一 handler；v1 不校验 `x-api-key`）
- 实现：`ml4gp/ml4gp/controller/predict.py:61` `ml4gp.controller.predict.get_predict`
- 响应：JSON 信封 `{code,message,status,data}`

**Query**

| 字段 | 读取方式 | 默认值 |
| --- | --- | --- |
| `code` | 下标，缺失会抛错 | 必有 |
| `msggroup` | 下标，缺失会抛错 | 必有 |
| `language` | 下标，缺失会抛错 | 必有 |
| `fixedSource` | `.get` | `` |

### GET `/v2/api/getRealTimePrice`

<a id="get-v2-api-getrealtimeprice-7"></a>

- 路由键：`getRealTimePrice`
- 鉴权：需要 x-api-key，免登录
- v1 镜像：`GET /v1/api/getRealTimePrice`（同一 handler；v1 不校验 `x-api-key`）
- 实现：`ml4gp/ml4gp/controller/predict.py:371` `ml4gp.controller.predict.get_real_time_price`
- 响应：JSON 信封 `{code,message,status,data}`
- 显式错误码：`PARAMS_ERROR`

**Query**

| 字段 | 读取方式 | 默认值 |
| --- | --- | --- |
| `code` | 下标，缺失会抛错 | 必有 |

### GET `/v2/api/getWeekPrice`

<a id="get-v2-api-getweekprice-8"></a>

- 路由键：`getWeekPrice`
- 鉴权：需要 x-api-key，免登录
- v1 镜像：`GET /v1/api/getWeekPrice`（同一 handler；v1 不校验 `x-api-key`）
- 实现：`ml4gp/ml4gp/controller/predict.py:404` `ml4gp.controller.predict.get_week_price`
- 响应：JSON 信封 `{code,message,status,data}`

**Query**

| 字段 | 读取方式 | 默认值 |
| --- | --- | --- |
| `type` | `.get` | `` |

### GET `/v2/api/getReportPDF`

<a id="get-v2-api-getreportpdf-9"></a>

- 路由键：`getReportPDF`
- 鉴权：需要 x-api-key，免登录
- v1 镜像：`GET /v1/api/getReportPDF`（同一 handler；v1 不校验 `x-api-key`）
- 实现：`ml4gp/ml4gp/controller/predict.py:434` `ml4gp.controller.predict.get_report_pdf`
- 响应：JSON 信封 `{code,message,status,data}`
- 显式错误码：`PARAMS_ERROR`, `POINTS_EXCHANGE_TIMES_LIMITED`

**Query**

| 字段 | 读取方式 | 默认值 |
| --- | --- | --- |
| `code` | `.get` | `` |
| `id` | `.get` | `` |
| `lan` | `.get` | `zh` |
| `fixedSource` | `.get` | `` |

### GET `/v2/api/getPredictPDF`

<a id="get-v2-api-getpredictpdf-10"></a>

- 路由键：`getPredictPDF`
- 鉴权：需要 x-api-key，免登录
- v1 镜像：`GET /v1/api/getPredictPDF`（同一 handler；v1 不校验 `x-api-key`）
- 实现：`ml4gp/ml4gp/controller/predict.py:462` `ml4gp.controller.predict.get_prediction_pdf`
- 响应：JSON 信封 `{code,message,status,data}`
- 显式错误码：`PARAMS_ERROR`, `POINTS_EXCHANGE_TIMES_LIMITED`

**Query**

| 字段 | 读取方式 | 默认值 |
| --- | --- | --- |
| `code` | `.get` | `` |
| `id` | `.get` | `` |
| `lan` | `.get` | `zh` |

### GET `/v2/api/getCoinSentiment`

<a id="get-v2-api-getcoinsentiment-11"></a>

- 路由键：`getCoinSentiment`
- 鉴权：需要 x-api-key，免登录
- v1 镜像：`GET /v1/api/getCoinSentiment`（同一 handler；v1 不校验 `x-api-key`）
- 实现：`ml4gp/ml4gp/controller/coin_sentiment.py:55` `ml4gp.controller.coin_sentiment.get_combined_data`
- 响应：JSON 信封 `{code,message,status,data}`

无额外 query/body 字段（或参数在更下游动态拼装）。

### GET `/v2/api/token/ai/choose/query`

<a id="get-v2-api-token-ai-choose-query-12"></a>

- 路由键：`queryAiChooseToken`
- 鉴权：需要 x-api-key，v2 免登录；v1 需登录
- v1 镜像：`GET /v1/api/token/ai/choose/query`（同一 handler；v1 不校验 `x-api-key`）
- 实现：`ml4gp/ml4gp/controller/ai_choose_token.py:9` `ml4gp.controller.ai_choose_token.query_ai_choose_token`
- 响应：JSON 信封 `{code,message,status,data}`

**Query**

| 字段 | 读取方式 | 默认值 |
| --- | --- | --- |
| `keyword` | `.get` | 无 |
| `refresh_cache` | `.get` | 无 |
| `page` | `.get` | 无 |
| `limit` | `.get` | 无 |
| `language` | `.get` | `zh` |

### POST `/v2/api/trend/getTrendInfo`

<a id="post-v2-api-trend-gettrendinfo-13"></a>

- 路由键：`getRelatedNews`
- 鉴权：需要 x-api-key，v2 免登录；v1 需登录
- v1 镜像：`POST /v1/api/trend/getTrendInfo`（同一 handler；v1 不校验 `x-api-key`）
- 实现：`ml4gp/ml4gp/controller/predict.py:486` `ml4gp.controller.predict.get_trend_news`
- 响应：JSON 信封 `{code,message,status,data}`
- 显式错误码：`PARAMS_ERROR`

**JSON Body**

| 字段 | 读取方式 | 默认值 |
| --- | --- | --- |
| `coinCode` | `.get` | `` |
| `trend` | `.get` | `` |
| `startTime` | `.get` | `` |
| `endTime` | `.get` | `` |
| `language` | `.get` | `zh` |
