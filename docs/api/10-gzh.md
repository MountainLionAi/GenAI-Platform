# 公众号

本模块 8 个已挂载接口。通用约定见 [README](README.md)。

## 索引

| 方法 | 路径 | 鉴权 |
| --- | --- | --- |
| GET | [`/v2/api/gzh/articles`](#get-v2-api-gzh-articles-1) | 需要 x-api-key，v2 免登录；v1 需登录 |
| GET | [`/v2/api/gzh/list`](#get-v2-api-gzh-list-2) | 需要 x-api-key，v2 免登录；v1 需登录 |
| GET | [`/v2/api/gzh/following`](#get-v2-api-gzh-following-3) | 需要 x-api-key，需登录 |
| POST | [`/v2/api/gzh/follow`](#post-v2-api-gzh-follow-4) | 需要 x-api-key，需登录 |
| POST | [`/v2/api/gzh/unfollow`](#post-v2-api-gzh-unfollow-5) | 需要 x-api-key，需登录 |
| GET | [`/v2/api/gzh/detail`](#get-v2-api-gzh-detail-6) | 需要 x-api-key，v2 免登录；v1 需登录 |
| GET | [`/v2/api/gzh/article/detail`](#get-v2-api-gzh-article-detail-7) | 需要 x-api-key，v2 免登录；v1 需登录 |
| POST | [`/v2/api/gzh/article/insight`](#post-v2-api-gzh-article-insight-8) | 需要 x-api-key，需登录 |

## 详情

### GET `/v2/api/gzh/articles`

<a id="get-v2-api-gzh-articles-1"></a>

- 路由键：`gzhArticleList`
- 鉴权：需要 x-api-key，v2 免登录；v1 需登录
- v1 镜像：`GET /v1/api/gzh/articles`（同一 handler；v1 不校验 `x-api-key`）
- 实现：`ml4gp/ml4gp/controller/gzh.py:8` `ml4gp.controller.gzh.gzh_article_list`
- 响应：JSON 信封 `{code,message,status,data}`

**Query**

| 字段 | 读取方式 | 默认值 |
| --- | --- | --- |
| `page` | `.get` | `1` |
| `pageSize` | `.get` | `20` |
| `time_zone` | `.get` | `Asia/Shanghai` |

### GET `/v2/api/gzh/list`

<a id="get-v2-api-gzh-list-2"></a>

- 路由键：`gzhList`
- 鉴权：需要 x-api-key，v2 免登录；v1 需登录
- v1 镜像：`GET /v1/api/gzh/list`（同一 handler；v1 不校验 `x-api-key`）
- 实现：`ml4gp/ml4gp/controller/gzh.py:16` `ml4gp.controller.gzh.gzh_list`
- 响应：JSON 信封 `{code,message,status,data}`

**Query**

| 字段 | 读取方式 | 默认值 |
| --- | --- | --- |
| `page` | `.get` | `1` |
| `pageSize` | `.get` | `20` |
| `keyword` | `.get` | `` |

### GET `/v2/api/gzh/following`

<a id="get-v2-api-gzh-following-3"></a>

- 路由键：`gzhFollowing`
- 鉴权：需要 x-api-key，需登录
- v1 镜像：`GET /v1/api/gzh/following`（同一 handler；v1 不校验 `x-api-key`）
- 实现：`ml4gp/ml4gp/controller/gzh.py:25` `ml4gp.controller.gzh.gzh_following`
- 响应：JSON 信封 `{code,message,status,data}`

**Query**

| 字段 | 读取方式 | 默认值 |
| --- | --- | --- |
| `page` | `.get` | `1` |
| `pageSize` | `.get` | `20` |
| `keyword` | `.get` | `` |

### POST `/v2/api/gzh/follow`

<a id="post-v2-api-gzh-follow-4"></a>

- 路由键：`gzhFollow`
- 鉴权：需要 x-api-key，需登录
- v1 镜像：`POST /v1/api/gzh/follow`（同一 handler；v1 不校验 `x-api-key`）
- 实现：`ml4gp/ml4gp/controller/gzh.py:36` `ml4gp.controller.gzh.gzh_follow`
- 响应：JSON 信封 `{code,message,status,data}`

**JSON Body**

| 字段 | 读取方式 | 默认值 |
| --- | --- | --- |
| `wxid` | `.get` | `` |

### POST `/v2/api/gzh/unfollow`

<a id="post-v2-api-gzh-unfollow-5"></a>

- 路由键：`gzhUnfollow`
- 鉴权：需要 x-api-key，需登录
- v1 镜像：`POST /v1/api/gzh/unfollow`（同一 handler；v1 不校验 `x-api-key`）
- 实现：`ml4gp/ml4gp/controller/gzh.py:48` `ml4gp.controller.gzh.gzh_unfollow`
- 响应：JSON 信封 `{code,message,status,data}`

**JSON Body**

| 字段 | 读取方式 | 默认值 |
| --- | --- | --- |
| `wxid` | `.get` | `` |

### GET `/v2/api/gzh/detail`

<a id="get-v2-api-gzh-detail-6"></a>

- 路由键：`gzhDetail`
- 鉴权：需要 x-api-key，v2 免登录；v1 需登录
- v1 镜像：`GET /v1/api/gzh/detail`（同一 handler；v1 不校验 `x-api-key`）
- 实现：`ml4gp/ml4gp/controller/gzh.py:60` `ml4gp.controller.gzh.gzh_detail`
- 响应：JSON 信封 `{code,message,status,data}`

**Query**

| 字段 | 读取方式 | 默认值 |
| --- | --- | --- |
| `wxid` | `.get` | `` |
| `page` | `.get` | `1` |
| `pageSize` | `.get` | `20` |
| `time_zone` | `.get` | `Asia/Shanghai` |
| `keyword` | `.get` | 无 |
| `keywords` | `.get` | 无 |

### GET `/v2/api/gzh/article/detail`

<a id="get-v2-api-gzh-article-detail-7"></a>

- 路由键：`gzhArticleDetail`
- 鉴权：需要 x-api-key，v2 免登录；v1 需登录
- v1 镜像：`GET /v1/api/gzh/article/detail`（同一 handler；v1 不校验 `x-api-key`）
- 实现：`ml4gp/ml4gp/controller/gzh.py:75` `ml4gp.controller.gzh.gzh_article_detail`
- 响应：JSON 信封 `{code,message,status,data}`

**Query**

| 字段 | 读取方式 | 默认值 |
| --- | --- | --- |
| `gzh_art_id` | `.get` | 无 |
| `time_zone` | `.get` | `Asia/Shanghai` |

### POST `/v2/api/gzh/article/insight`

<a id="post-v2-api-gzh-article-insight-8"></a>

- 路由键：`gzhArticleDeepInsight`
- 鉴权：需要 x-api-key，需登录
- v1 镜像：`POST /v1/api/gzh/article/insight`（同一 handler；v1 不校验 `x-api-key`）
- 实现：`ml4gp/ml4gp/controller/gzh_deep_insight.py:25` `ml4gp.controller.gzh_deep_insight.gzh_article_deep_insight`
- 响应：流式（SSE / chunk）
- 显式错误码：`DATA_NOT_FOUND`, `NOT_AUTHORIZED`, `PARAMS_ERROR`

**JSON Body**

| 字段 | 读取方式 | 默认值 |
| --- | --- | --- |
| `gzh_art_id` | `.get` | 无 |
| `language` | `.get` | `cn` |
