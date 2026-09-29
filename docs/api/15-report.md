# 研报

本模块 12 个已挂载接口。通用约定见 [README](README.md)。

## 索引

| 方法 | 路径 | 鉴权 |
| --- | --- | --- |
| GET | [`/v2/api/report/pdf/download/users`](#get-v2-api-report-pdf-download-users-1) | 需要 x-api-key，v2 免登录；v1 需登录 |
| POST | [`/v2/api/share/pic/report`](#post-v2-api-share-pic-report-2) | 需要 x-api-key，v2 免登录；v1 需登录 |
| GET | [`/v2/api/price/predict/pdf/download`](#get-v2-api-price-predict-pdf-download-3) | 需要 x-api-key，需登录 |
| GET | [`/v2/api/getReportData`](#get-v2-api-getreportdata-4) | 需要 x-api-key，v2 免登录；v1 需登录 |
| GET | [`/v2/api/getReportDataTask`](#get-v2-api-getreportdatatask-5) | 需要 x-api-key，v2 免登录；v1 需登录 |
| GET | [`/v2/api/getReportDataForTW`](#get-v2-api-getreportdatafortw-6) | 需要 x-api-key，v2 免登录；v1 需登录 |
| GET | [`/v2/api/getReportUpdateTime`](#get-v2-api-getreportupdatetime-7) | 需要 x-api-key，v2 免登录；v1 需登录 |
| GET | [`/v2/api/getReportTypeUpdateTime`](#get-v2-api-getreporttypeupdatetime-8) | 需要 x-api-key，v2 免登录；v1 需登录 |
| GET | [`/v2/api/report/ai/companies`](#get-v2-api-report-ai-companies-9) | 需要 x-api-key，v2 免登录；v1 需登录 |
| GET | [`/v2/api/report/ai`](#get-v2-api-report-ai-10) | 需要 x-api-key，v2 免登录；v1 需登录 |
| GET | [`/v2/api/getAndPickReportDataForInner`](#get-v2-api-getandpickreportdataforinner-11) | 需要 x-api-key，免登录 |
| POST | [`/v2/api/trigger/pdf/report/research`](#post-v2-api-trigger-pdf-report-research-12) | 需要 x-api-key，v2 免登录；v1 需登录 |

## 详情

### GET `/v2/api/report/pdf/download/users`

<a id="get-v2-api-report-pdf-download-users-1"></a>

- 路由键：`reportPdfDownloadUsers`
- 鉴权：需要 x-api-key，v2 免登录；v1 需登录
- v1 镜像：`GET /v1/api/report/pdf/download/users`（同一 handler；v1 不校验 `x-api-key`）
- 实现：`ml4gp/ml4gp/controller/report_pdf_download_users.py:7` `ml4gp.controller.report_pdf_download_users.download_users`
- 响应：JSON 信封 `{code,message,status,data}`

无额外 query/body 字段（或参数在更下游动态拼装）。

### POST `/v2/api/share/pic/report`

<a id="post-v2-api-share-pic-report-2"></a>

- 路由键：`ShareReport`
- 鉴权：需要 x-api-key，v2 免登录；v1 需登录
- v1 镜像：`POST /v1/api/share/pic/report`（同一 handler；v1 不校验 `x-api-key`）
- 实现：`ml4gp/ml4gp/controller/reportdata.py:78` `ml4gp.controller.reportdata.share_research_report`
- 响应：JSON 信封 `{code,message,status,data}`

**Query**

| 字段 | 读取方式 | 默认值 |
| --- | --- | --- |
| `pc_or_phone` | `.get` | `pc` |
| `fixedSource` | `.get` | `` |

**JSON Body**

| 字段 | 读取方式 | 默认值 |
| --- | --- | --- |
| `symbol` | `.get` | `null` |
| `language` | `.get` | `en` |
| `price` | `.get` | `` |
| `percent_change` | `.get` | `` |
| `logo` | `.get` | `` |
| `utcOffset` | `.get` | `` |
| `black_or_white` | `.get` | `black` |
| `client` | `.get` | `web` |

### GET `/v2/api/price/predict/pdf/download`

<a id="get-v2-api-price-predict-pdf-download-3"></a>

- 路由键：`pricePredictPdfDownload`
- 鉴权：需要 x-api-key，需登录
- v1 镜像：`GET /v1/api/price/predict/pdf/download`（同一 handler；v1 不校验 `x-api-key`）
- 实现：`ml4gp/ml4gp/controller/token_predict_pdf.py:10` `ml4gp.controller.token_predict_pdf.price_predict_pdf_download`
- 响应：JSON 信封 `{code,message,status,data}`

**Query**

| 字段 | 读取方式 | 默认值 |
| --- | --- | --- |
| `code` | 下标，缺失会抛错 | 必有 |
| `language` | 下标，缺失会抛错 | 必有 |
| `month_day` | 下标，缺失会抛错 | 必有 |
| `year` | 下标，缺失会抛错 | 必有 |
| `week` | 下标，缺失会抛错 | 必有 |

### GET `/v2/api/getReportData`

<a id="get-v2-api-getreportdata-4"></a>

- 路由键：`getReportData`
- 鉴权：需要 x-api-key，v2 免登录；v1 需登录
- v1 镜像：`GET /v1/api/getReportData`（同一 handler；v1 不校验 `x-api-key`）
- 实现：`ml4gp/ml4gp/controller/reportdata.py:16` `ml4gp.controller.reportdata.get_report_data`
- 响应：JSON 信封 `{code,message,status,data}`

**Query**

| 字段 | 读取方式 | 默认值 |
| --- | --- | --- |
| `symbol` | `.get` | `null` |
| `language` | `.get` | `en` |
| `report_type` | `.get` | `1` |
| `usecache` | `.get` | `false` |

### GET `/v2/api/getReportDataTask`

<a id="get-v2-api-getreportdatatask-5"></a>

处理加密货币报告请求

- 路由键：`getReportDataTask`
- 鉴权：需要 x-api-key，v2 免登录；v1 需登录
- v1 镜像：`GET /v1/api/getReportDataTask`（同一 handler；v1 不校验 `x-api-key`）
- 实现：`ml4gp/ml4gp/controller/reportdata.py:139` `ml4gp.controller.reportdata.get_report_data_task`
- 响应：JSON 信封 `{code,message,status,data}`
- `data` 字面量键：`result`, `data`, `task_id`

**Query**

| 字段 | 读取方式 | 默认值 |
| --- | --- | --- |
| `symbol` | `.get` | `null` |
| `language` | `.get` | `en` |
| `report_type` | `.get` | `1` |
| `usecache` | `.get` | `false` |

### GET `/v2/api/getReportDataForTW`

<a id="get-v2-api-getreportdatafortw-6"></a>

- 路由键：`getReportDataTW`
- 鉴权：需要 x-api-key，v2 免登录；v1 需登录
- v1 镜像：`GET /v1/api/getReportDataForTW`（同一 handler；v1 不校验 `x-api-key`）
- 实现：`ml4gp/ml4gp/controller/reportdata.py:44` `ml4gp.controller.reportdata.get_report_data_for_tw`
- 响应：JSON 信封 `{code,message,status,data}`

**Query**

| 字段 | 读取方式 | 默认值 |
| --- | --- | --- |
| `symbol` | `.get` | `null` |
| `language` | `.get` | `en` |
| `report_type` | `.get` | `1` |

### GET `/v2/api/getReportUpdateTime`

<a id="get-v2-api-getreportupdatetime-7"></a>

- 路由键：`getReportUpdateTime`
- 鉴权：需要 x-api-key，v2 免登录；v1 需登录
- v1 镜像：`GET /v1/api/getReportUpdateTime`（同一 handler；v1 不校验 `x-api-key`）
- 实现：`ml4gp/ml4gp/controller/reportdata.py:59` `ml4gp.controller.reportdata.get_report_update_time`
- 响应：JSON 信封 `{code,message,status,data}`

无额外 query/body 字段（或参数在更下游动态拼装）。

### GET `/v2/api/getReportTypeUpdateTime`

<a id="get-v2-api-getreporttypeupdatetime-8"></a>

- 路由键：`getReportTypeUpdateTime`
- 鉴权：需要 x-api-key，v2 免登录；v1 需登录
- v1 镜像：`GET /v1/api/getReportTypeUpdateTime`（同一 handler；v1 不校验 `x-api-key`）
- 实现：`ml4gp/ml4gp/controller/reportdata.py:63` `ml4gp.controller.reportdata.get_report_type_update_time`
- 响应：JSON 信封 `{code,message,status,data}`
- `data` 字面量键：`type_1`, `type_2`, `type_3`, `type_4`

**Query**

| 字段 | 读取方式 | 默认值 |
| --- | --- | --- |
| `symbol` | `.get` | `null` |
| `language` | `.get` | `en` |

### GET `/v2/api/report/ai/companies`

<a id="get-v2-api-report-ai-companies-9"></a>

- 路由键：`aiReportCompanies`
- 鉴权：需要 x-api-key，v2 免登录；v1 需登录
- v1 镜像：`GET /v1/api/report/ai/companies`（同一 handler；v1 不校验 `x-api-key`）
- 实现：`ml4gp/ml4gp/controller/ai_report.py:7` `ml4gp.controller.ai_report.company_list`
- 响应：JSON 信封 `{code,message,status,data}`

无额外 query/body 字段（或参数在更下游动态拼装）。

### GET `/v2/api/report/ai`

<a id="get-v2-api-report-ai-10"></a>

- 路由键：`aiReport`
- 鉴权：需要 x-api-key，v2 免登录；v1 需登录
- v1 镜像：`GET /v1/api/report/ai`（同一 handler；v1 不校验 `x-api-key`）
- 实现：`ml4gp/ml4gp/controller/ai_report.py:12` `ml4gp.controller.ai_report.ai_report`
- 响应：JSON 信封 `{code,message,status,data}`

**Query**

| 字段 | 读取方式 | 默认值 |
| --- | --- | --- |
| `language` | `.get` | `en` |
| `cmp_id` | `.get` | 无 |
| `user_input` | `.get` | 无 |
| `msggroup` | `.get` | 无 |

### GET `/v2/api/getAndPickReportDataForInner`

<a id="get-v2-api-getandpickreportdataforinner-11"></a>

- 路由键：`getAndPickReportDataForInner`
- 鉴权：需要 x-api-key，免登录
- v1 镜像：`GET /v1/api/getAndPickReportDataForInner`（同一 handler；v1 不校验 `x-api-key`）
- 实现：`ml4gp/ml4gp/controller/reportdata.py:115` `ml4gp.controller.reportdata.getAndPickReportDataForInner`
- 响应：JSON 信封 `{code,message,status,data}`

**Query**

| 字段 | 读取方式 | 默认值 |
| --- | --- | --- |
| `symbol` | `.get` | `null` |
| `language` | `.get` | `en` |

### POST `/v2/api/trigger/pdf/report/research`

<a id="post-v2-api-trigger-pdf-report-research-12"></a>

手动触发研报生成PDF

- 路由键：`triggeResearchReportToPdf`
- 鉴权：需要 x-api-key，v2 免登录；v1 需登录
- v1 镜像：`POST /v1/api/trigger/pdf/report/research`（同一 handler；v1 不校验 `x-api-key`）
- 实现：`ml4gp/ml4gp/controller/trigger.py:8` `ml4gp.controller.trigger.research_report_to_pdf`
- 响应：JSON 信封 `{code,message,status,data}`

**JSON Body**

| 字段 | 读取方式 | 默认值 |
| --- | --- | --- |
| `coins` | `.get` | 无 |
