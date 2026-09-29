# AI 榜单

本模块 10 个已挂载接口。通用约定见 [README](README.md)。

## 索引

| 方法 | 路径 | 鉴权 |
| --- | --- | --- |
| GET | [`/v2/api/ai_ranking`](#get-v2-api-ai-ranking-1) | 需要 x-api-key，免登录 |
| GET | [`/v2/api/ai_compare`](#get-v2-api-ai-compare-2) | 需要 x-api-key，免登录 |
| POST | [`/v2/api/ai_ranking_insight`](#post-v2-api-ai-ranking-insight-3) | 需要 x-api-key，免登录 |
| GET | [`/v2/api/ai_ranking_price`](#get-v2-api-ai-ranking-price-4) | 需要 x-api-key，免登录 |
| GET | [`/v2/api/ai_ranking_people`](#get-v2-api-ai-ranking-people-5) | 需要 x-api-key，免登录 |
| GET | [`/v2/api/ai_compare_people`](#get-v2-api-ai-compare-people-6) | 需要 x-api-key，免登录 |
| POST | [`/v2/api/ai_ranking_insight_people`](#post-v2-api-ai-ranking-insight-people-7) | 需要 x-api-key，免登录 |
| GET | [`/v2/api/ai_ranking_investor`](#get-v2-api-ai-ranking-investor-8) | 需要 x-api-key，免登录 |
| GET | [`/v2/api/ai_compare_investor`](#get-v2-api-ai-compare-investor-9) | 需要 x-api-key，免登录 |
| POST | [`/v2/api/ai_ranking_insight_investor`](#post-v2-api-ai-ranking-insight-investor-10) | 需要 x-api-key，免登录 |

## 详情

### GET `/v2/api/ai_ranking`

<a id="get-v2-api-ai-ranking-1"></a>

- 路由键：`getAIRanking`
- 鉴权：需要 x-api-key，免登录
- v1 镜像：`GET /v1/api/ai_ranking`（同一 handler；v1 不校验 `x-api-key`）
- 实现：`ml4gp/ml4gp/controller/ai_ranking.py:21` `ml4gp.controller.ai_ranking.ai_ranking`
- 响应：JSON 信封 `{code,message,status,data}`

**Query**

| 字段 | 读取方式 | 默认值 |
| --- | --- | --- |
| `language` | `.get` | `en` |
| `projects_type` | `.get` | 无 |
| `order_by` | `.get` | `project_id` |
| `direction` | `.get` | `asc` |
| `page` | `.get` | `1` |
| `limit` | `.get` | `10` |

### GET `/v2/api/ai_compare`

<a id="get-v2-api-ai-compare-2"></a>

- 路由键：`getAICompare`
- 鉴权：需要 x-api-key，免登录
- v1 镜像：`GET /v1/api/ai_compare`（同一 handler；v1 不校验 `x-api-key`）
- 实现：`ml4gp/ml4gp/controller/ai_ranking.py:62` `ml4gp.controller.ai_ranking.project_compare`
- 响应：流式（SSE / chunk）

**Query**

| 字段 | 读取方式 | 默认值 |
| --- | --- | --- |
| `language` | `.get` | `en` |
| `projects_id` | `.get` | 无 |
| `projects_type` | `.get` | 无 |

### POST `/v2/api/ai_ranking_insight`

<a id="post-v2-api-ai-ranking-insight-3"></a>

- 路由键：`getAIRAnkingInsight`
- 鉴权：需要 x-api-key，免登录
- v1 镜像：`POST /v1/api/ai_ranking_insight`（同一 handler；v1 不校验 `x-api-key`）
- 实现：`ml4gp/ml4gp/controller/ai_ranking.py:228` `ml4gp.controller.ai_ranking.ai_ranking_insight`
- 响应：流式（SSE / chunk）

**JSON Body**

| 字段 | 读取方式 | 默认值 |
| --- | --- | --- |
| `id` | `.get` | 无 |
| `projects_type` | `.get` | 无 |
| `language` | `.get` | `cn` |

### GET `/v2/api/ai_ranking_price`

<a id="get-v2-api-ai-ranking-price-4"></a>

- 路由键：`getAIRAnkingPrice`
- 鉴权：需要 x-api-key，免登录
- v1 镜像：`GET /v1/api/ai_ranking_price`（同一 handler；v1 不校验 `x-api-key`）
- 实现：`ml4gp/ml4gp/controller/ai_ranking.py:325` `ml4gp.controller.ai_ranking.ai_ranking_price`
- 响应：JSON 信封 `{code,message,status,data}`

**Query**

| 字段 | 读取方式 | 默认值 |
| --- | --- | --- |
| `ticker_id` | `.get` | 无 |

### GET `/v2/api/ai_ranking_people`

<a id="get-v2-api-ai-ranking-people-5"></a>

- 路由键：`getAIRankingPeople`
- 鉴权：需要 x-api-key，免登录
- v1 镜像：`GET /v1/api/ai_ranking_people`（同一 handler；v1 不校验 `x-api-key`）
- 实现：`ml4gp/ml4gp/controller/ai_ranking.py:34` `ml4gp.controller.ai_ranking.ai_ranking_people`
- 响应：JSON 信封 `{code,message,status,data}`

**Query**

| 字段 | 读取方式 | 默认值 |
| --- | --- | --- |
| `language` | `.get` | `en` |
| `order_by` | `.get` | `project_id` |
| `direction` | `.get` | `asc` |
| `type` | `.get` | 无 |
| `value` | `.get` | 无 |
| `page` | `.get` | `1` |
| `limit` | `.get` | `10` |

### GET `/v2/api/ai_compare_people`

<a id="get-v2-api-ai-compare-people-6"></a>

- 路由键：`getAIPeopleCompare`
- 鉴权：需要 x-api-key，免登录
- v1 镜像：`GET /v1/api/ai_compare_people`（同一 handler；v1 不校验 `x-api-key`）
- 实现：`ml4gp/ml4gp/controller/ai_ranking.py:80` `ml4gp.controller.ai_ranking.people_compare`
- 响应：流式（SSE / chunk）

**Query**

| 字段 | 读取方式 | 默认值 |
| --- | --- | --- |
| `language` | `.get` | `en` |
| `peoples_id` | `.get` | 无 |

### POST `/v2/api/ai_ranking_insight_people`

<a id="post-v2-api-ai-ranking-insight-people-7"></a>

- 路由键：`getAIRAnkingPeopleInsight`
- 鉴权：需要 x-api-key，免登录
- v1 镜像：`POST /v1/api/ai_ranking_insight_people`（同一 handler；v1 不校验 `x-api-key`）
- 实现：`ml4gp/ml4gp/controller/ai_ranking.py:213` `ml4gp.controller.ai_ranking.ai_ranking_people_insight`
- 响应：流式（SSE / chunk）

**JSON Body**

| 字段 | 读取方式 | 默认值 |
| --- | --- | --- |
| `people_id` | `.get` | 无 |
| `language` | `.get` | `cn` |

### GET `/v2/api/ai_ranking_investor`

<a id="get-v2-api-ai-ranking-investor-8"></a>

- 路由键：`getAIRankingInvestor`
- 鉴权：需要 x-api-key，免登录
- v1 镜像：`GET /v1/api/ai_ranking_investor`（同一 handler；v1 不校验 `x-api-key`）
- 实现：`ml4gp/ml4gp/controller/ai_ranking.py:48` `ml4gp.controller.ai_ranking.ai_ranking_investor`
- 响应：JSON 信封 `{code,message,status,data}`

**Query**

| 字段 | 读取方式 | 默认值 |
| --- | --- | --- |
| `language` | `.get` | `en` |
| `order_by` | `.get` | `project_id` |
| `direction` | `.get` | `asc` |
| `type` | `.get` | 无 |
| `value` | `.get` | 无 |
| `page` | `.get` | `1` |
| `limit` | `.get` | `10` |

### GET `/v2/api/ai_compare_investor`

<a id="get-v2-api-ai-compare-investor-9"></a>

- 路由键：`getAIInvestorCompare`
- 鉴权：需要 x-api-key，免登录
- v1 镜像：`GET /v1/api/ai_compare_investor`（同一 handler；v1 不校验 `x-api-key`）
- 实现：`ml4gp/ml4gp/controller/ai_ranking.py:97` `ml4gp.controller.ai_ranking.investor_compare`
- 响应：流式（SSE / chunk）

**Query**

| 字段 | 读取方式 | 默认值 |
| --- | --- | --- |
| `language` | `.get` | `en` |
| `investors_id` | `.get` | 无 |

### POST `/v2/api/ai_ranking_insight_investor`

<a id="post-v2-api-ai-ranking-insight-investor-10"></a>

- 路由键：`getAIRAnkingInvestorInsight`
- 鉴权：需要 x-api-key，免登录
- v1 镜像：`POST /v1/api/ai_ranking_insight_investor`（同一 handler；v1 不校验 `x-api-key`）
- 实现：`ml4gp/ml4gp/controller/ai_ranking.py:198` `ml4gp.controller.ai_ranking.ai_ranking_investor_insight`
- 响应：流式（SSE / chunk）

**JSON Body**

| 字段 | 读取方式 | 默认值 |
| --- | --- | --- |
| `investor_id` | `.get` | 无 |
| `language` | `.get` | `cn` |
