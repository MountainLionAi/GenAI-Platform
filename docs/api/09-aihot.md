# AI 热点

本模块 9 个已挂载接口。通用约定见 [README](README.md)。

## 索引

| 方法 | 路径 | 鉴权 |
| --- | --- | --- |
| GET | [`/v2/api/news/aihot/reports`](#get-v2-api-news-aihot-reports-1) | 需要 x-api-key，免登录 |
| GET | [`/v2/api/news/aihot/reports/detail`](#get-v2-api-news-aihot-reports-detail-2) | 需要 x-api-key，免登录 |
| GET | [`/v2/api/news/aihot/hot`](#get-v2-api-news-aihot-hot-3) | 需要 x-api-key，免登录 |
| GET | [`/v2/api/news/aihot/hot/detail`](#get-v2-api-news-aihot-hot-detail-4) | 需要 x-api-key，免登录 |
| GET | [`/v2/api/news/aihot/topics`](#get-v2-api-news-aihot-topics-5) | 需要 x-api-key，免登录 |
| GET | [`/v2/api/news/aihot/topics/detail`](#get-v2-api-news-aihot-topics-detail-6) | 需要 x-api-key，免登录 |
| GET | [`/v2/api/news/aihot/models`](#get-v2-api-news-aihot-models-7) | 需要 x-api-key，免登录 |
| GET | [`/v2/api/news/aihot/models/detail`](#get-v2-api-news-aihot-models-detail-8) | 需要 x-api-key，免登录 |
| GET | [`/v2/api/news/aihot/item`](#get-v2-api-news-aihot-item-9) | 需要 x-api-key，免登录 |

## 详情

### GET `/v2/api/news/aihot/reports`

<a id="get-v2-api-news-aihot-reports-1"></a>

- 路由键：`aihotReports`
- 鉴权：需要 x-api-key，免登录
- v1 镜像：`GET /v1/api/news/aihot/reports`（同一 handler；v1 不校验 `x-api-key`）
- 实现：`ml4gp/ml4gp/controller/aihot_digest.py:167` `ml4gp.controller.aihot_digest.aihot_reports`
- 响应：JSON 信封 `{code,message,status,data}`

**Query**

| 字段 | 读取方式 | 默认值 |
| --- | --- | --- |
| `type` | `.get` | `daily` |
| `period_type` | `.get` | `daily` |
| `limit` | `.get` | `14` |
| `language` | `.get` | `cn` |
| `lang` | `.get` | `cn` |

### GET `/v2/api/news/aihot/reports/detail`

<a id="get-v2-api-news-aihot-reports-detail-2"></a>

- 路由键：`aihotReportDetail`
- 鉴权：需要 x-api-key，免登录
- v1 镜像：`GET /v1/api/news/aihot/reports/detail`（同一 handler；v1 不校验 `x-api-key`）
- 实现：`ml4gp/ml4gp/controller/aihot_digest.py:195` `ml4gp.controller.aihot_digest.aihot_report_detail`
- 响应：JSON 信封 `{code,message,status,data}`
- `data` 字面量键：`type`, `key`, `title`, `dateLabel`, `itemCount`, `readMinutes`, `sourceUrl`, `generatedAt`, `items`

**Query**

| 字段 | 读取方式 | 默认值 |
| --- | --- | --- |
| `type` | `.get` | `daily` |
| `period_type` | `.get` | `daily` |
| `key` | `.get` | 无 |
| `period_key` | `.get` | 无 |
| `language` | `.get` | `cn` |
| `lang` | `.get` | `cn` |

### GET `/v2/api/news/aihot/hot`

<a id="get-v2-api-news-aihot-hot-3"></a>

- 路由键：`aihotHot`
- 鉴权：需要 x-api-key，免登录
- v1 镜像：`GET /v1/api/news/aihot/hot`（同一 handler；v1 不校验 `x-api-key`）
- 实现：`ml4gp/ml4gp/controller/aihot_digest.py:234` `ml4gp.controller.aihot_digest.aihot_hot`
- 响应：JSON 信封 `{code,message,status,data}`

**Query**

| 字段 | 读取方式 | 默认值 |
| --- | --- | --- |
| `category` | `.get` | `ai` |
| `language` | `.get` | `cn` |
| `lang` | `.get` | `cn` |

### GET `/v2/api/news/aihot/hot/detail`

<a id="get-v2-api-news-aihot-hot-detail-4"></a>

- 路由键：`aihotHotDetail`
- 鉴权：需要 x-api-key，免登录
- v1 镜像：`GET /v1/api/news/aihot/hot/detail`（同一 handler；v1 不校验 `x-api-key`）
- 实现：`ml4gp/ml4gp/controller/aihot_digest.py:267` `ml4gp.controller.aihot_digest.aihot_hot_detail`
- 响应：JSON 信封 `{code,message,status,data}`
- `data` 字面量键：`id`, `rank`, `title`, `desc`, `digest`, `status`, `sourcesCount`, `participantsCount`, `score`, `timeText`, `sparkline`, `heatChart`, `sourceNames`, `storyUrl`, `reportCount`, `reports`

**Query**

| 字段 | 读取方式 | 默认值 |
| --- | --- | --- |
| `id` | `.get` | 无 |
| `story_id` | `.get` | 无 |
| `language` | `.get` | `cn` |
| `lang` | `.get` | `cn` |

### GET `/v2/api/news/aihot/topics`

<a id="get-v2-api-news-aihot-topics-5"></a>

- 路由键：`aihotTopics`
- 鉴权：需要 x-api-key，免登录
- v1 镜像：`GET /v1/api/news/aihot/topics`（同一 handler；v1 不校验 `x-api-key`）
- 实现：`ml4gp/ml4gp/controller/aihot_digest.py:333` `ml4gp.controller.aihot_digest.aihot_topics`
- 响应：JSON 信封 `{code,message,status,data}`

**Query**

| 字段 | 读取方式 | 默认值 |
| --- | --- | --- |
| `language` | `.get` | `cn` |
| `lang` | `.get` | `cn` |

### GET `/v2/api/news/aihot/topics/detail`

<a id="get-v2-api-news-aihot-topics-detail-6"></a>

- 路由键：`aihotTopicDetail`
- 鉴权：需要 x-api-key，免登录
- v1 镜像：`GET /v1/api/news/aihot/topics/detail`（同一 handler；v1 不校验 `x-api-key`）
- 实现：`ml4gp/ml4gp/controller/aihot_digest.py:366` `ml4gp.controller.aihot_digest.aihot_topic_detail`
- 响应：JSON 信封 `{code,message,status,data}`
- `data` 字面量键：`id`, `title`, `desc`, `logo`, `totalCount`, `selectedCount`, `updateTime`, `sourceUrl`, `hotTopics`, `feed`

**Query**

| 字段 | 读取方式 | 默认值 |
| --- | --- | --- |
| `slug` | `.get` | 无 |
| `id` | `.get` | 无 |
| `language` | `.get` | `cn` |
| `lang` | `.get` | `cn` |

### GET `/v2/api/news/aihot/models`

<a id="get-v2-api-news-aihot-models-7"></a>

- 路由键：`aihotModels`
- 鉴权：需要 x-api-key，免登录
- v1 镜像：`GET /v1/api/news/aihot/models`（同一 handler；v1 不校验 `x-api-key`）
- 实现：`ml4gp/ml4gp/controller/aihot_digest.py:418` `ml4gp.controller.aihot_digest.aihot_models`
- 响应：JSON 信封 `{code,message,status,data}`

**Query**

| 字段 | 读取方式 | 默认值 |
| --- | --- | --- |
| `category` | `.get` | `overall` |

### GET `/v2/api/news/aihot/models/detail`

<a id="get-v2-api-news-aihot-models-detail-8"></a>

- 路由键：`aihotModelDetail`
- 鉴权：需要 x-api-key，免登录
- v1 镜像：`GET /v1/api/news/aihot/models/detail`（同一 handler；v1 不校验 `x-api-key`）
- 实现：`ml4gp/ml4gp/controller/aihot_digest.py:444` `ml4gp.controller.aihot_digest.aihot_model_detail`
- 响应：JSON 信封 `{code,message,status,data}`
- `data` 字面量键：`id`, `name`, `company`, `logo`, `rank`, `score`, `date`, `contextWindow`, `categoryCovered`, `evalCount`, `priceIn`, `priceOut`, `officialPriceUrl`, `sourceUrl`, `updateTime`, `capabilities`, `evaluations`

**Query**

| 字段 | 读取方式 | 默认值 |
| --- | --- | --- |
| `slug` | `.get` | 无 |
| `id` | `.get` | 无 |

### GET `/v2/api/news/aihot/item`

<a id="get-v2-api-news-aihot-item-9"></a>

- 路由键：`aihotItem`
- 鉴权：需要 x-api-key，免登录
- v1 镜像：`GET /v1/api/news/aihot/item`（同一 handler；v1 不校验 `x-api-key`）
- 实现：`ml4gp/ml4gp/controller/aihot_digest.py:673` `ml4gp.controller.aihot_digest.aihot_item`
- 响应：JSON 信封 `{code,message,status,data}`
- `data` 字面量键：`itemId`, `newsId`, `kind`, `title`, `source`, `author`, `date`, `aiGuide`, `reason`, `score`, `originalUrl`, `aihotUrl`, `isWechat`, `content`

**Query**

| 字段 | 读取方式 | 默认值 |
| --- | --- | --- |
| `newsId` | `.get` | 无 |
| `news_id` | `.get` | 无 |
| `itemId` | `.get` | 无 |
| `item_id` | `.get` | 无 |
| `id` | `.get` | 无 |
| `language` | `.get` | `cn` |
| `lang` | `.get` | `cn` |
