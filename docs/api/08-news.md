# 快讯与新闻

本模块 32 个已挂载接口。通用约定见 [README](README.md)。

## 索引

| 方法 | 路径 | 鉴权 |
| --- | --- | --- |
| GET | [`/v2/api/news/real/time`](#get-v2-api-news-real-time-1) | 需要 x-api-key，免登录 |
| GET | [`/v2/api/news/real/time/keywords`](#get-v2-api-news-real-time-keywords-2) | 需要 x-api-key，v2 免登录；v1 需登录 |
| GET | [`/v2/api/news/real/time/recommend`](#get-v2-api-news-real-time-recommend-3) | 需要 x-api-key，v2 免登录；v1 需登录 |
| GET | [`/v2/api/news/security`](#get-v2-api-news-security-4) | 需要 x-api-key，免登录 |
| GET | [`/v2/api/news/real/time/sw`](#get-v2-api-news-real-time-sw-5) | 需要 x-api-key，免登录 |
| GET | [`/v2/api/news/real/time/ai`](#get-v2-api-news-real-time-ai-6) | 需要 x-api-key，免登录 |
| GET | [`/v2/api/news/search`](#get-v2-api-news-search-7) | 需要 x-api-key，免登录 |
| GET | [`/v2/api/news/real/time/ai/recommend`](#get-v2-api-news-real-time-ai-recommend-8) | 需要 x-api-key，v2 免登录；v1 需登录 |
| GET | [`/v2/api/news/real/time/general`](#get-v2-api-news-real-time-general-9) | 需要 x-api-key，免登录 |
| GET | [`/v2/api/news/real/time/general/recommend`](#get-v2-api-news-real-time-general-recommend-10) | 需要 x-api-key，免登录 |
| GET | [`/v2/api/news/real/time/general/filters`](#get-v2-api-news-real-time-general-filters-11) | 需要 x-api-key，免登录 |
| GET | [`/v2/api/news/real/time/ai/sw`](#get-v2-api-news-real-time-ai-sw-12) | 需要 x-api-key，免登录 |
| POST | [`/v2/api/news/real/time/comment/short/gen`](#post-v2-api-news-real-time-comment-short-gen-13) | 需要 x-api-key，免登录 |
| GET | [`/v2/api/tw/news/real/time`](#get-v2-api-tw-news-real-time-14) | 需要 x-api-key，免登录 |
| GET | [`/v2/api/v2/news/flash/home`](#get-v2-api-v2-news-flash-home-15) | 需要 x-api-key，v2 免登录；v1 需登录 |
| GET | [`/v2/api/v2/news/flash/list`](#get-v2-api-v2-news-flash-list-16) | 需要 x-api-key，v2 免登录；v1 需登录 |
| GET | [`/v2/api/v2/news/flash/detail`](#get-v2-api-v2-news-flash-detail-17) | 需要 x-api-key，v2 免登录；v1 需登录 |
| POST | [`/v2/api/v2/news/flash/vote`](#post-v2-api-v2-news-flash-vote-18) | 需要 x-api-key，v2 免登录；v1 需登录 |
| GET | [`/v2/api/news/daily/hot`](#get-v2-api-news-daily-hot-19) | 需要 x-api-key，免登录 |
| GET | [`/v2/api/news/weekly/hot`](#get-v2-api-news-weekly-hot-20) | 需要 x-api-key，免登录 |
| GET | [`/v2/api/word/hot/get`](#get-v2-api-word-hot-get-21) | 需要 x-api-key，免登录 |
| GET | [`/v2/api/data/board/news`](#get-v2-api-data-board-news-22) | 需要 x-api-key，免登录 |
| POST | [`/v2/api/broadcast/daily/add`](#post-v2-api-broadcast-daily-add-23) | 需要 x-api-key，免登录 |
| GET | [`/v2/api/broadcast/daily/query`](#get-v2-api-broadcast-daily-query-24) | 需要 x-api-key，免登录 |
| POST | [`/v2/api/broadcast/daily/share/add`](#post-v2-api-broadcast-daily-share-add-25) | 需要 x-api-key，免登录 |
| GET | [`/v2/api/broadcast/daily/share/query`](#get-v2-api-broadcast-daily-share-query-26) | 需要 x-api-key，免登录 |
| GET | [`/v2/api/news/hot/list`](#get-v2-api-news-hot-list-27) | 需要 x-api-key，免登录 |
| GET | [`/v2/api/podcast/list`](#get-v2-api-podcast-list-28) | 需要 x-api-key，v2 免登录；v1 需登录 |
| POST | [`/v2/api/news/feedback/add`](#post-v2-api-news-feedback-add-29) | 需要 x-api-key，需登录 |
| GET | [`/v2/api/newsRewite/typelist`](#get-v2-api-newsrewite-typelist-30) | 需要 x-api-key，v2 免登录；v1 需登录 |
| POST | [`/v2/api/newsRewite/content`](#post-v2-api-newsrewite-content-31) | 需要 x-api-key，v2 免登录；v1 需登录 |
| GET | [`/v2/api/newsbot`](#get-v2-api-newsbot-32) | 需要 x-api-key，免登录 |

## 详情

### GET `/v2/api/news/real/time`

<a id="get-v2-api-news-real-time-1"></a>

- 路由键：`realTimeNews`
- 鉴权：需要 x-api-key，免登录
- v1 镜像：`GET /v1/api/news/real/time`（同一 handler；v1 不校验 `x-api-key`）
- 实现：`ml4gp/ml4gp/controller/real_time_news.py:34` `ml4gp.controller.real_time_news.real_time_news`
- 响应：JSON 信封 `{code,message,status,data}`

**Query**

| 字段 | 读取方式 | 默认值 |
| --- | --- | --- |
| `query_date` | `.get` | `null` |
| `language` | `.get` | `en` |
| `time_zone` | `.get` | `Asia/Shanghai` |
| `is_hot` | `.get` | 无 |
| `num` | `.get` | `40` |
| `page` | `.get` | `1` |
| `client` | `.get` | `APP` |

### GET `/v2/api/news/real/time/keywords`

<a id="get-v2-api-news-real-time-keywords-2"></a>

- 路由键：`realTimeNews1`
- 鉴权：需要 x-api-key，v2 免登录；v1 需登录
- v1 镜像：`GET /v1/api/news/real/time/keywords`（同一 handler；v1 不校验 `x-api-key`）
- 实现：`ml4gp/ml4gp/controller/real_time_news.py:87` `ml4gp.controller.real_time_news.real_time_news_by_keywords`
- 响应：JSON 信封 `{code,message,status,data}`

**Query**

| 字段 | 读取方式 | 默认值 |
| --- | --- | --- |
| `language` | `.get` | `en` |
| `time_zone` | `.get` | `Asia/Shanghai` |
| `is_hot` | `.get` | 无 |
| `num` | `.get` | `10` |
| `page` | `.get` | `1` |
| `client` | `.get` | `APP` |
| `keywords` | `.get` | `` |

### GET `/v2/api/news/real/time/recommend`

<a id="get-v2-api-news-real-time-recommend-3"></a>

- 路由键：`realTimeNewsRecommend`
- 鉴权：需要 x-api-key，v2 免登录；v1 需登录
- v1 镜像：`GET /v1/api/news/real/time/recommend`（同一 handler；v1 不校验 `x-api-key`）
- 实现：`ml4gp/ml4gp/controller/real_time_news.py:142` `ml4gp.controller.real_time_news.real_time_news_recommend`
- 响应：JSON 信封 `{code,message,status,data}`

**Query**

| 字段 | 读取方式 | 默认值 |
| --- | --- | --- |
| `language` | `.get` | `en` |
| `time_zone` | `.get` | `Asia/Shanghai` |
| `news_id` | `.get` | 无 |

### GET `/v2/api/news/security`

<a id="get-v2-api-news-security-4"></a>

- 路由键：`securityNews`
- 鉴权：需要 x-api-key，免登录
- v1 镜像：`GET /v1/api/news/security`（同一 handler；v1 不校验 `x-api-key`）
- 实现：`ml4gp/ml4gp/controller/real_time_news.py:361` `ml4gp.controller.real_time_news.security_news`
- 响应：JSON 信封 `{code,message,status,data}`

**Query**

| 字段 | 读取方式 | 默认值 |
| --- | --- | --- |
| `language` | `.get` | `en` |
| `days` | `.get` | `7` |
| `security_type` | `.get` | `null` |

### GET `/v2/api/news/real/time/sw`

<a id="get-v2-api-news-real-time-sw-5"></a>

- 路由键：`realTimeNewsSw`
- 鉴权：需要 x-api-key，免登录
- v1 镜像：`GET /v1/api/news/real/time/sw`（同一 handler；v1 不校验 `x-api-key`）
- 实现：`ml4gp/ml4gp/controller/real_time_news_sw.py:17` `ml4gp.controller.real_time_news_sw.real_time_news_sw`
- 响应：JSON 信封 `{code,message,status,data}`

**Query**

| 字段 | 读取方式 | 默认值 |
| --- | --- | --- |
| `query_date` | `.get` | `null` |
| `language` | `.get` | `en` |
| `time_zone` | `.get` | `Asia/Shanghai` |
| `num` | `.get` | 无 |

### GET `/v2/api/news/real/time/ai`

<a id="get-v2-api-news-real-time-ai-6"></a>

- 路由键：`realTimeNewsAi`
- 鉴权：需要 x-api-key，免登录
- v1 镜像：`GET /v1/api/news/real/time/ai`（同一 handler；v1 不校验 `x-api-key`）
- 实现：`ml4gp/ml4gp/controller/real_time_news_ai.py:17` `ml4gp.controller.real_time_news_ai.real_time_news_ai`
- 响应：JSON 信封 `{code,message,status,data}`
- `data` 字面量键：`data`, `pagination`

**Query**

| 字段 | 读取方式 | 默认值 |
| --- | --- | --- |
| `query_date` | `.get` | `null` |
| `language` | `.get` | `en` |
| `time_zone` | `.get` | `Asia/Shanghai` |
| `num` | `.get` | 无 |
| `page` | `.get` | `1` |
| `dopage` | `.get` | 无 |

### GET `/v2/api/news/search`

<a id="get-v2-api-news-search-7"></a>

- 路由键：`realTimeNewsSearch`
- 鉴权：需要 x-api-key，免登录
- v1 镜像：`GET /v1/api/news/search`（同一 handler；v1 不校验 `x-api-key`）
- 实现：`ml4gp/ml4gp/controller/real_time_news_ai.py:79` `ml4gp.controller.real_time_news_ai.real_time_news_search`
- 响应：JSON 信封 `{code,message,status,data}`

**Query**

| 字段 | 读取方式 | 默认值 |
| --- | --- | --- |
| `q` | `.get` | 无 |
| `newsType` | `.get` | 无 |
| `type` | `.get` | 无 |
| `language` | `.get` | 无 |
| `limit` | `.get` | 无 |

### GET `/v2/api/news/real/time/ai/recommend`

<a id="get-v2-api-news-real-time-ai-recommend-8"></a>

- 路由键：`realTimeNewsAiRecommend`
- 鉴权：需要 x-api-key，v2 免登录；v1 需登录
- v1 镜像：`GET /v1/api/news/real/time/ai/recommend`（同一 handler；v1 不校验 `x-api-key`）
- 实现：`ml4gp/ml4gp/controller/real_time_news_ai.py:117` `ml4gp.controller.real_time_news_ai.real_time_news_ai_recommend`
- 响应：JSON 信封 `{code,message,status,data}`

**Query**

| 字段 | 读取方式 | 默认值 |
| --- | --- | --- |
| `language` | `.get` | `en` |
| `time_zone` | `.get` | `Asia/Shanghai` |
| `news_id` | `.get` | 无 |

### GET `/v2/api/news/real/time/general`

<a id="get-v2-api-news-real-time-general-9"></a>

- 路由键：`realTimeNewsGeneral`
- 鉴权：需要 x-api-key，免登录
- v1 镜像：`GET /v1/api/news/real/time/general`（同一 handler；v1 不校验 `x-api-key`）
- 实现：`ml4gp/ml4gp/controller/real_time_news_general.py:36` `ml4gp.controller.real_time_news_general.real_time_news_general`
- 响应：JSON 信封 `{code,message,status,data}`

**Query**

| 字段 | 读取方式 | 默认值 |
| --- | --- | --- |
| `query_date` | `.get` | `null` |
| `language` | `.get` | `en` |
| `time_zone` | `.get` | `Asia/Shanghai` |
| `category` | `.get` | `all` |

### GET `/v2/api/news/real/time/general/recommend`

<a id="get-v2-api-news-real-time-general-recommend-10"></a>

- 路由键：`realTimeNewsGeneralRecommend`
- 鉴权：需要 x-api-key，免登录
- v1 镜像：`GET /v1/api/news/real/time/general/recommend`（同一 handler；v1 不校验 `x-api-key`）
- 实现：`ml4gp/ml4gp/controller/real_time_news_general.py:62` `ml4gp.controller.real_time_news_general.real_time_news_general_recommend`
- 响应：JSON 信封 `{code,message,status,data}`

**Query**

| 字段 | 读取方式 | 默认值 |
| --- | --- | --- |
| `language` | `.get` | `en` |
| `time_zone` | `.get` | `Asia/Shanghai` |
| `category` | `.get` | `all` |
| `news_id` | `.get` | 无 |

### GET `/v2/api/news/real/time/general/filters`

<a id="get-v2-api-news-real-time-general-filters-11"></a>

- 路由键：`realTimeNewsGeneralFilters`
- 鉴权：需要 x-api-key，免登录
- v1 镜像：`GET /v1/api/news/real/time/general/filters`（同一 handler；v1 不校验 `x-api-key`）
- 实现：`ml4gp/ml4gp/controller/real_time_news_general.py:80` `ml4gp.controller.real_time_news_general.real_time_news_general_filters`
- 响应：JSON 信封 `{code,message,status,data}`
- `data` 字面量键：`categories`

**Query**

| 字段 | 读取方式 | 默认值 |
| --- | --- | --- |
| `language` | `.get` | `cn` |

### GET `/v2/api/news/real/time/ai/sw`

<a id="get-v2-api-news-real-time-ai-sw-12"></a>

- 路由键：`realTimeNewsAiSw`
- 鉴权：需要 x-api-key，免登录
- v1 镜像：`GET /v1/api/news/real/time/ai/sw`（同一 handler；v1 不校验 `x-api-key`）
- 实现：`ml4gp/ml4gp/controller/real_time_news_ai_sw.py:11` `ml4gp.controller.real_time_news_ai_sw.real_time_news_ai_sw`
- 响应：JSON 信封 `{code,message,status,data}`

**Query**

| 字段 | 读取方式 | 默认值 |
| --- | --- | --- |
| `query_date` | `.get` | `null` |
| `language` | `.get` | `en` |
| `time_zone` | `.get` | `Asia/Shanghai` |
| `num` | `.get` | 无 |

### POST `/v2/api/news/real/time/comment/short/gen`

<a id="post-v2-api-news-real-time-comment-short-gen-13"></a>

- 路由键：`realTimeNewsShortCommentGen`
- 鉴权：需要 x-api-key，免登录
- v1 镜像：`POST /v1/api/news/real/time/comment/short/gen`（同一 handler；v1 不校验 `x-api-key`）
- 实现：`ml4gp/ml4gp/controller/real_time_news_short_comment.py:10` `ml4gp.controller.real_time_news_short_comment.gen_short_comment`
- 响应：流式（SSE / chunk）
- 显式错误码：`PARAMS_ERROR`

**JSON Body**

| 字段 | 读取方式 | 默认值 |
| --- | --- | --- |
| `news_id` | `.get` | 无 |
| `language` | `.get` | 无 |
| `news_type` | `.get` | 无 |

### GET `/v2/api/tw/news/real/time`

<a id="get-v2-api-tw-news-real-time-14"></a>

- 路由键：`realTimeNewsTw`
- 鉴权：需要 x-api-key，免登录
- v1 镜像：`GET /v1/api/tw/news/real/time`（同一 handler；v1 不校验 `x-api-key`）
- 实现：`ml4gp/ml4gp/controller/real_time_news.py:269` `ml4gp.controller.real_time_news.real_time_news_tw`
- 响应：JSON 信封 `{code,message,status,data}`

**Query**

| 字段 | 读取方式 | 默认值 |
| --- | --- | --- |
| `query_date` | `.get` | `null` |
| `language` | `.get` | `en` |
| `createTime` | `.get` | `null` |

### GET `/v2/api/v2/news/flash/home`

<a id="get-v2-api-v2-news-flash-home-15"></a>

- 路由键：`flashHome`
- 鉴权：需要 x-api-key，v2 免登录；v1 需登录
- v1 镜像：`GET /v1/api/v2/news/flash/home`（同一 handler；v1 不校验 `x-api-key`）
- 实现：`ml4gp/ml4gp/controller/real_time_news_v2.py:56` `ml4gp.controller.real_time_news_v2.flash_home`
- 响应：JSON 信封 `{code,message,status,data}`

**Query**

| 字段 | 读取方式 | 默认值 |
| --- | --- | --- |
| `language` | `.get` | `cn` |
| `num` | `.get` | 无 |
| `time_zone` | `.get` | `null` |
| `device_id` | `.get` | `null` |

### GET `/v2/api/v2/news/flash/list`

<a id="get-v2-api-v2-news-flash-list-16"></a>

- 路由键：`flashList`
- 鉴权：需要 x-api-key，v2 免登录；v1 需登录
- v1 镜像：`GET /v1/api/v2/news/flash/list`（同一 handler；v1 不校验 `x-api-key`）
- 实现：`ml4gp/ml4gp/controller/real_time_news_v2.py:76` `ml4gp.controller.real_time_news_v2.flash_list`
- 响应：JSON 信封 `{code,message,status,data}`

**Query**

| 字段 | 读取方式 | 默认值 |
| --- | --- | --- |
| `language` | `.get` | `cn` |
| `category` | `.get` | `all` |
| `page` | `.get` | 无 |
| `num` | `.get` | 无 |
| `is_hot` | `.get` | `null` |
| `query_date` | `.get` | `null` |
| `time_zone` | `.get` | `null` |
| `keyword` | `.get` | `` |
| `device_id` | `.get` | `null` |

### GET `/v2/api/v2/news/flash/detail`

<a id="get-v2-api-v2-news-flash-detail-17"></a>

- 路由键：`flashDetail`
- 鉴权：需要 x-api-key，v2 免登录；v1 需登录
- v1 镜像：`GET /v1/api/v2/news/flash/detail`（同一 handler；v1 不校验 `x-api-key`）
- 实现：`ml4gp/ml4gp/controller/real_time_news_v2.py:131` `ml4gp.controller.real_time_news_v2.flash_detail`
- 响应：JSON 信封 `{code,message,status,data}`

**Query**

| 字段 | 读取方式 | 默认值 |
| --- | --- | --- |
| `news_id` | `.get` | 无 |
| `language` | `.get` | `cn` |
| `time_zone` | `.get` | `null` |
| `device_id` | `.get` | `null` |

### POST `/v2/api/v2/news/flash/vote`

<a id="post-v2-api-v2-news-flash-vote-18"></a>

- 路由键：`flashVote`
- 鉴权：需要 x-api-key，v2 免登录；v1 需登录
- v1 镜像：`POST /v1/api/v2/news/flash/vote`（同一 handler；v1 不校验 `x-api-key`）
- 实现：`ml4gp/ml4gp/controller/real_time_news_v2.py:161` `ml4gp.controller.real_time_news_v2.flash_vote`
- 响应：JSON 信封 `{code,message,status,data}`
- `data` 字面量键：`like_num`, `dislike_num`, `my_vote`

**JSON Body**

| 字段 | 读取方式 | 默认值 |
| --- | --- | --- |
| `news_id` | `.get` | 无 |
| `language` | `.get` | 无 |
| `device_id` | `.get` | `` |
| `vote_type` | `.get` | `` |

### GET `/v2/api/news/daily/hot`

<a id="get-v2-api-news-daily-hot-19"></a>

- 路由键：`dayHotNews`
- 鉴权：需要 x-api-key，免登录
- v1 镜像：`GET /v1/api/news/daily/hot`（同一 handler；v1 不校验 `x-api-key`）
- 实现：`ml4gp/ml4gp/controller/day_hot_news.py:10` `ml4gp.controller.day_hot_news.day_hot_news`
- 响应：JSON 信封 `{code,message,status,data}`

**Query**

| 字段 | 读取方式 | 默认值 |
| --- | --- | --- |
| `language` | `.get` | `en` |

### GET `/v2/api/news/weekly/hot`

<a id="get-v2-api-news-weekly-hot-20"></a>

获取每周热点新闻

- 路由键：`weekHotNews`
- 鉴权：需要 x-api-key，免登录
- v1 镜像：`GET /v1/api/news/weekly/hot`（同一 handler；v1 不校验 `x-api-key`）
- 实现：`ml4gp/ml4gp/controller/weekly_hot_news.py:8` `ml4gp.controller.weekly_hot_news.weekly_hot_news`
- 响应：JSON 信封 `{code,message,status,data}`

**Query**

| 字段 | 读取方式 | 默认值 |
| --- | --- | --- |
| `language` | `.get` | `cn` |
| `page` | `.get` | 无 |
| `pagesize` | `.get` | 无 |

### GET `/v2/api/word/hot/get`

<a id="get-v2-api-word-hot-get-21"></a>

- 路由键：`hotWordGet`
- 鉴权：需要 x-api-key，免登录
- v1 镜像：`GET /v1/api/word/hot/get`（同一 handler；v1 不校验 `x-api-key`）
- 实现：`ml4gp/ml4gp/controller/hot_word.py:13` `ml4gp.controller.hot_word.hot_words`
- 响应：JSON 信封 `{code,message,status,data}`

**Query**

| 字段 | 读取方式 | 默认值 |
| --- | --- | --- |
| `language` | `.get` | `cn` |

### GET `/v2/api/data/board/news`

<a id="get-v2-api-data-board-news-22"></a>

- 路由键：`dataBoardNews`
- 鉴权：需要 x-api-key，免登录
- v1 镜像：`GET /v1/api/data/board/news`（同一 handler；v1 不校验 `x-api-key`）
- 实现：`ml4gp/ml4gp/controller/data_board_news.py:15` `ml4gp.controller.data_board_news.data_board_news`
- 响应：JSON 信封 `{code,message,status,data}`

**Query**

| 字段 | 读取方式 | 默认值 |
| --- | --- | --- |
| `query_date` | `.get` | `null` |
| `symbol` | `.get` | `null` |
| `language` | `.get` | `en` |
| `time_zone` | `.get` | `Asia/Shanghai` |
| `needRefresh` | `.get` | `0` |
| `visitor_id` | `.get` | `` |

### POST `/v2/api/broadcast/daily/add`

<a id="post-v2-api-broadcast-daily-add-23"></a>

- 路由键：`addDailyBroadcastModule`
- 鉴权：需要 x-api-key，免登录
- v1 镜像：`POST /v1/api/broadcast/daily/add`（同一 handler；v1 不校验 `x-api-key`）
- 实现：`ml4gp/ml4gp/controller/daily_broadcast.py:9` `ml4gp.controller.daily_broadcast.add_daily_broadcast`
- 响应：JSON 信封 `{code,message,status,data}`

**JSON Body**

| 字段 | 读取方式 | 默认值 |
| --- | --- | --- |
| `bd_date` | `.get` | 无 |
| `title` | `.get` | 无 |
| `texts` | `.get` | 无 |
| `language` | `.get` | `en` |

### GET `/v2/api/broadcast/daily/query`

<a id="get-v2-api-broadcast-daily-query-24"></a>

- 路由键：`queryDailyBroadcastModule`
- 鉴权：需要 x-api-key，免登录
- v1 镜像：`GET /v1/api/broadcast/daily/query`（同一 handler；v1 不校验 `x-api-key`）
- 实现：`ml4gp/ml4gp/controller/daily_broadcast.py:31` `ml4gp.controller.daily_broadcast.query_daily_broadcast`
- 响应：JSON 信封 `{code,message,status,data}`

**Query**

| 字段 | 读取方式 | 默认值 |
| --- | --- | --- |
| `bd_date` | `.get` | 无 |
| `language` | `.get` | `en` |
| `visitor_id` | `.get` | `` |

### POST `/v2/api/broadcast/daily/share/add`

<a id="post-v2-api-broadcast-daily-share-add-25"></a>

- 路由键：`addDailyBroadcastShare`
- 鉴权：需要 x-api-key，免登录
- v1 镜像：`POST /v1/api/broadcast/daily/share/add`（同一 handler；v1 不校验 `x-api-key`）
- 实现：`ml4gp/ml4gp/controller/daily_broadcast.py:45` `ml4gp.controller.daily_broadcast.add_daily_broadcast_share`
- 响应：JSON 信封 `{code,message,status,data}`

**JSON Body**

| 字段 | 读取方式 | 默认值 |
| --- | --- | --- |
| `bd_id` | `.get` | 无 |
| `qrcode_url` | `.get` | 无 |
| `code` | `.get` | 无 |
| `language` | `.get` | 无 |

### GET `/v2/api/broadcast/daily/share/query`

<a id="get-v2-api-broadcast-daily-share-query-26"></a>

- 路由键：`queryDailyBroadcastShare`
- 鉴权：需要 x-api-key，免登录
- v1 镜像：`GET /v1/api/broadcast/daily/share/query`（同一 handler；v1 不校验 `x-api-key`）
- 实现：`ml4gp/ml4gp/controller/daily_broadcast.py:70` `ml4gp.controller.daily_broadcast.query_daily_broadcast_share`
- 响应：JSON 信封 `{code,message,status,data}`

**Query**

| 字段 | 读取方式 | 默认值 |
| --- | --- | --- |
| `code` | `.get` | 无 |
| `language` | `.get` | 无 |

### GET `/v2/api/news/hot/list`

<a id="get-v2-api-news-hot-list-27"></a>

- 路由键：`hotNewsList`
- 鉴权：需要 x-api-key，免登录
- v1 镜像：`GET /v1/api/news/hot/list`（同一 handler；v1 不校验 `x-api-key`）
- 实现：`ml4gp/ml4gp/controller/hot_news_list.py:10` `ml4gp.controller.hot_news_list.hot_news_list`
- 响应：JSON 信封 `{code,message,status,data}`

**Query**

| 字段 | 读取方式 | 默认值 |
| --- | --- | --- |
| `language` | `.get` | `en` |
| `time_zone` | `.get` | `Asia/Shanghai` |
| `fixedSource` | `.get` | 无 |

### GET `/v2/api/podcast/list`

<a id="get-v2-api-podcast-list-28"></a>

- 路由键：`podcastList`
- 鉴权：需要 x-api-key，v2 免登录；v1 需登录
- v1 镜像：`GET /v1/api/podcast/list`（同一 handler；v1 不校验 `x-api-key`）
- 实现：`ml4gp/ml4gp/controller/podcast.py:7` `ml4gp.controller.podcast.list`
- 响应：JSON 信封 `{code,message,status,data}`

**Query**

| 字段 | 读取方式 | 默认值 |
| --- | --- | --- |
| `language` | `.get` | `en` |

### POST `/v2/api/news/feedback/add`

<a id="post-v2-api-news-feedback-add-29"></a>

- 路由键：`addNewsFeedback`
- 鉴权：需要 x-api-key，需登录
- v1 镜像：`POST /v1/api/news/feedback/add`（同一 handler；v1 不校验 `x-api-key`）
- 实现：`ml4gp/ml4gp/controller/news_feedback.py:29` `ml4gp.controller.news_feedback.add_news_feedback`
- 响应：JSON 信封 `{code,message,status,data}`

**JSON Body**

| 字段 | 读取方式 | 默认值 |
| --- | --- | --- |
| `news_id` | `.get` | 无 |
| `type` | `.get` | 无 |
| `news_type` | `.get` | 无 |
| `language` | `.get` | `zh` |
| `source` | `.get` | `app` |

### GET `/v2/api/newsRewite/typelist`

<a id="get-v2-api-newsrewite-typelist-30"></a>

- 路由键：`newsRewiteTypeList`
- 鉴权：需要 x-api-key，v2 免登录；v1 需登录
- v1 镜像：`GET /v1/api/newsRewite/typelist`（同一 handler；v1 不校验 `x-api-key`）
- 实现：`ml4gp/ml4gp/controller/news_rewrite.py:13` `ml4gp.controller.news_rewrite.rewrite_type_list`
- 响应：JSON 信封 `{code,message,status,data}`

无额外 query/body 字段（或参数在更下游动态拼装）。

### POST `/v2/api/newsRewite/content`

<a id="post-v2-api-newsrewite-content-31"></a>

- 路由键：`newsRewiteContent`
- 鉴权：需要 x-api-key，v2 免登录；v1 需登录
- v1 镜像：`POST /v1/api/newsRewite/content`（同一 handler；v1 不校验 `x-api-key`）
- 实现：`ml4gp/ml4gp/controller/news_rewrite.py:57` `ml4gp.controller.news_rewrite.rewrite`
- 响应：流式（SSE / chunk）

**JSON Body**

| 字段 | 读取方式 | 默认值 |
| --- | --- | --- |
| `title` | `.get` | `` |
| `content` | `.get` | `` |
| `type` | `.get` | `` |
| `lan` | `.get` | `cn` |
| `image_url` | `.get` | `` |

### GET `/v2/api/newsbot`

<a id="get-v2-api-newsbot-32"></a>

- 路由键：`get_news`
- 鉴权：需要 x-api-key，免登录
- 实现：`GenAI/genaipf/controller/user.py:193` `genaipf.controller.user.get_news`
- 响应：JSON 信封 `{code,message,status,data}`

无额外 query/body 字段（或参数在更下游动态拼装）。
