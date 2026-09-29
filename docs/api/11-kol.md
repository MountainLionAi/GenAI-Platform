# KOL 与推文

本模块 16 个已挂载接口。通用约定见 [README](README.md)。

## 索引

| 方法 | 路径 | 鉴权 |
| --- | --- | --- |
| GET | [`/v2/api/news/follow_kol`](#get-v2-api-news-follow-kol-1) | 需要 x-api-key，需登录 |
| GET | [`/v2/api/news/unfollow_kol`](#get-v2-api-news-unfollow-kol-2) | 需要 x-api-key，需登录 |
| GET | [`/v2/api/news/kol/avatar/refresh`](#get-v2-api-news-kol-avatar-refresh-3) | 需要 x-api-key，免登录 |
| POST | [`/v2/api/news/kol/avatar/refresh`](#post-v2-api-news-kol-avatar-refresh-4) | 需要 x-api-key，免登录 |
| GET | [`/v2/api/news/tweet`](#get-v2-api-news-tweet-5) | 需要 x-api-key，免登录 |
| GET | [`/v2/api/news/kol/feed`](#get-v2-api-news-kol-feed-6) | 需要 x-api-key，免登录 |
| GET | [`/v2/api/news/tweet/recommend`](#get-v2-api-news-tweet-recommend-7) | 需要 x-api-key，v2 免登录；v1 需登录 |
| GET | [`/v2/api/news/kollist`](#get-v2-api-news-kollist-8) | 需要 x-api-key，免登录 |
| GET | [`/v2/api/twitterSignin`](#get-v2-api-twittersignin-9) | 需要 x-api-key，免登录 |
| GET | [`/v2/api/twitterBinding`](#get-v2-api-twitterbinding-10) | 需要 x-api-key，免登录 |
| GET | [`/v2/api/twitterUnBinding`](#get-v2-api-twitterunbinding-11) | 需要 x-api-key，免登录 |
| GET | [`/v2/api/getUserVerifiedTask`](#get-v2-api-getuserverifiedtask-12) | 需要 x-api-key，免登录 |
| GET | [`/v2/api/verifyUserOperation`](#get-v2-api-verifyuseroperation-13) | 需要 x-api-key，免登录 |
| POST | [`/v2/api/tweets/share/add`](#post-v2-api-tweets-share-add-14) | 需要 x-api-key，免登录 |
| GET | [`/v2/api/tweets/share/get`](#get-v2-api-tweets-share-get-15) | 需要 x-api-key，免登录 |
| POST | [`/v2/api/tweet/bot/comment/pic`](#post-v2-api-tweet-bot-comment-pic-16) | 需要 x-api-key，v2 免登录；v1 需登录 |

## 详情

### GET `/v2/api/news/follow_kol`

<a id="get-v2-api-news-follow-kol-1"></a>

- 路由键：`followKOL`
- 鉴权：需要 x-api-key，需登录
- v1 镜像：`GET /v1/api/news/follow_kol`（同一 handler；v1 不校验 `x-api-key`）
- 实现：`ml4gp/ml4gp/controller/tweet.py:597` `ml4gp.controller.tweet.follow_kol`
- 响应：JSON 信封 `{code,message,status,data}`

**Query**

| 字段 | 读取方式 | 默认值 |
| --- | --- | --- |
| `username` | `.get` | 无 |

### GET `/v2/api/news/unfollow_kol`

<a id="get-v2-api-news-unfollow-kol-2"></a>

- 路由键：`unfollowKOL`
- 鉴权：需要 x-api-key，需登录
- v1 镜像：`GET /v1/api/news/unfollow_kol`（同一 handler；v1 不校验 `x-api-key`）
- 实现：`ml4gp/ml4gp/controller/tweet.py:605` `ml4gp.controller.tweet.unfollow_kol`
- 响应：JSON 信封 `{code,message,status,data}`

**Query**

| 字段 | 读取方式 | 默认值 |
| --- | --- | --- |
| `username` | `.get` | 无 |

### GET `/v2/api/news/kol/avatar/refresh`

<a id="get-v2-api-news-kol-avatar-refresh-3"></a>

头像加载失败时按 username 拉最新头像并回写 kol_info / crawl config。

- 路由键：`refreshKolAvatar`
- 鉴权：需要 x-api-key，免登录
- v1 镜像：`GET /v1/api/news/kol/avatar/refresh`（同一 handler；v1 不校验 `x-api-key`）
- 实现：`ml4gp/ml4gp/controller/tweet.py:613` `ml4gp.controller.tweet.refresh_kol_avatar`
- 响应：JSON 信封 `{code,message,status,data}`
- `data` 字面量键：`username`, `image_url`, `channel`

**Query**

| 字段 | 读取方式 | 默认值 |
| --- | --- | --- |
| `username` | `.get` | 无 |

**JSON Body**

| 字段 | 读取方式 | 默认值 |
| --- | --- | --- |
| `username` | `.get` | 无 |

### POST `/v2/api/news/kol/avatar/refresh`

<a id="post-v2-api-news-kol-avatar-refresh-4"></a>

头像加载失败时按 username 拉最新头像并回写 kol_info / crawl config。

- 路由键：`refreshKolAvatar`
- 鉴权：需要 x-api-key，免登录
- v1 镜像：`POST /v1/api/news/kol/avatar/refresh`（同一 handler；v1 不校验 `x-api-key`）
- 实现：`ml4gp/ml4gp/controller/tweet.py:613` `ml4gp.controller.tweet.refresh_kol_avatar`
- 响应：JSON 信封 `{code,message,status,data}`
- `data` 字面量键：`username`, `image_url`, `channel`

**Query**

| 字段 | 读取方式 | 默认值 |
| --- | --- | --- |
| `username` | `.get` | 无 |

**JSON Body**

| 字段 | 读取方式 | 默认值 |
| --- | --- | --- |
| `username` | `.get` | 无 |

### GET `/v2/api/news/tweet`

<a id="get-v2-api-news-tweet-5"></a>

- 路由键：`tweet`
- 鉴权：需要 x-api-key，免登录
- v1 镜像：`GET /v1/api/news/tweet`（同一 handler；v1 不校验 `x-api-key`）
- 实现：`ml4gp/ml4gp/controller/tweet.py:129` `ml4gp.controller.tweet.tweet`
- 响应：JSON 信封 `{code,message,status,data}`
- `data` 字面量键：`total_num`, `tweet`, `followed`, `kol_info`, `following_num`

**Query**

| 字段 | 读取方式 | 默认值 |
| --- | --- | --- |
| `query_date` | `.get` | 无 |
| `language` | `.get` | `cn` |
| `keywords` | `.get` | `` |
| `following` | `.get` | `` |
| `page` | `.get` | `1` |
| `pageSize` | `.get` | `50` |
| `time_zone` | `.get` | `Asia/Shanghai` |
| `fixedSource` | `.get` | `` |
| `username` | `.get` | `` |
| `search_username` | `.get` | `` |
| `is_homepage` | `.get` | `false` |

### GET `/v2/api/news/kol/feed`

<a id="get-v2-api-news-kol-feed-6"></a>

GET news/kol/feed

- 路由键：`kolFeed`
- 鉴权：需要 x-api-key，免登录
- v1 镜像：`GET /v1/api/news/kol/feed`（同一 handler；v1 不校验 `x-api-key`）
- 实现：`ml4gp/ml4gp/controller/kol_feed.py:216` `ml4gp.controller.kol_feed.kol_feed`
- 响应：JSON 信封 `{code,message,status,data}`
- `data` 字面量键：`tweet`, `total_num`, `following_num`, `has_more`, `page`, `pageSize`

**Query**

| 字段 | 读取方式 | 默认值 |
| --- | --- | --- |
| `keywords` | `.get` | 无 |
| `query_date` | `.get` | 无 |
| `language` | `.get` | `cn` |
| `following` | `.get` | `` |
| `page` | `.get` | `1` |
| `pageSize` | `.get` | `30` |
| `time_zone` | `.get` | `Asia/Shanghai` |
| `category` | `.get` | 无 |

### GET `/v2/api/news/tweet/recommend`

<a id="get-v2-api-news-tweet-recommend-7"></a>

- 路由键：`tweetRecommend`
- 鉴权：需要 x-api-key，v2 免登录；v1 需登录
- v1 镜像：`GET /v1/api/news/tweet/recommend`（同一 handler；v1 不校验 `x-api-key`）
- 实现：`ml4gp/ml4gp/controller/tweet.py:947` `ml4gp.controller.tweet.tweets_recommend`
- 响应：JSON 信封 `{code,message,status,data}`

**Query**

| 字段 | 读取方式 | 默认值 |
| --- | --- | --- |
| `language` | `.get` | `en` |
| `time_zone` | `.get` | `Asia/Shanghai` |
| `tweet_id` | `.get` | 无 |

### GET `/v2/api/news/kollist`

<a id="get-v2-api-news-kollist-8"></a>

- 路由键：`kolList`
- 鉴权：需要 x-api-key，免登录
- v1 镜像：`GET /v1/api/news/kollist`（同一 handler；v1 不校验 `x-api-key`）
- 实现：`ml4gp/ml4gp/controller/tweet.py:376` `ml4gp.controller.tweet.get_kol_list`
- 响应：JSON 信封 `{code,message,status,data}`
- `data` 字面量键：`kol_list`, `following_num`

**Query**

| 字段 | 读取方式 | 默认值 |
| --- | --- | --- |
| `language` | `.get` | `cn` |
| `following` | `.get` | `` |
| `search_username` | `.get` | `` |
| `type` | `.get` | 无 |

### GET `/v2/api/twitterSignin`

<a id="get-v2-api-twittersignin-9"></a>

- 路由键：`twitterSignin`
- 鉴权：需要 x-api-key，免登录
- v1 镜像：`GET /v1/api/twitterSignin`（同一 handler；v1 不校验 `x-api-key`）
- 实现：`ml4gp/ml4gp/controller/tweet.py:700` `ml4gp.controller.tweet.twitter_signin`
- 响应：JSON 信封 `{code,message,status,data}`

无额外 query/body 字段（或参数在更下游动态拼装）。

### GET `/v2/api/twitterBinding`

<a id="get-v2-api-twitterbinding-10"></a>

- 路由键：`twitterBinding`
- 鉴权：需要 x-api-key，免登录
- v1 镜像：`GET /v1/api/twitterBinding`（同一 handler；v1 不校验 `x-api-key`）
- 实现：`ml4gp/ml4gp/controller/tweet.py:718` `ml4gp.controller.tweet.bind_twitter`
- 响应：JSON 信封 `{code,message,status,data}`
- `data` 字面量键：`screen_name`

**Query**

| 字段 | 读取方式 | 默认值 |
| --- | --- | --- |
| `oauthToken` | `.get` | `` |
| `oauthVerifier` | `.get` | `` |

### GET `/v2/api/twitterUnBinding`

<a id="get-v2-api-twitterunbinding-11"></a>

- 路由键：`twitterUnBinding`
- 鉴权：需要 x-api-key，免登录
- v1 镜像：`GET /v1/api/twitterUnBinding`（同一 handler；v1 不校验 `x-api-key`）
- 实现：`ml4gp/ml4gp/controller/tweet.py:767` `ml4gp.controller.tweet.unbinding_twitter`
- 响应：JSON 信封 `{code,message,status,data}`

无额外 query/body 字段（或参数在更下游动态拼装）。

### GET `/v2/api/getUserVerifiedTask`

<a id="get-v2-api-getuserverifiedtask-12"></a>

- 路由键：`getUserVerifiedTask`
- 鉴权：需要 x-api-key，免登录
- v1 镜像：`GET /v1/api/getUserVerifiedTask`（同一 handler；v1 不校验 `x-api-key`）
- 实现：`ml4gp/ml4gp/controller/tweet.py:894` `ml4gp.controller.tweet.get_user_verified_task`
- 响应：JSON 信封 `{code,message,status,data}`

无额外 query/body 字段（或参数在更下游动态拼装）。

### GET `/v2/api/verifyUserOperation`

<a id="get-v2-api-verifyuseroperation-13"></a>

- 路由键：`verifyUserOperation`
- 鉴权：需要 x-api-key，免登录
- v1 镜像：`GET /v1/api/verifyUserOperation`（同一 handler；v1 不校验 `x-api-key`）
- 实现：`ml4gp/ml4gp/controller/tweet.py:774` `ml4gp.controller.tweet.verify_user_operation`
- 响应：JSON 信封 `{code,message,status,data}`

**Query**

| 字段 | 读取方式 | 默认值 |
| --- | --- | --- |
| `type` | `.get` | `1` |

### POST `/v2/api/tweets/share/add`

<a id="post-v2-api-tweets-share-add-14"></a>

添加分享tweets

- 路由键：`sharedTweetssAdd`
- 鉴权：需要 x-api-key，免登录
- v1 镜像：`POST /v1/api/tweets/share/add`（同一 handler；v1 不校验 `x-api-key`）
- 实现：`ml4gp/ml4gp/controller/shared_tweets.py:9` `ml4gp.controller.shared_tweets.add_share_tweets`
- 响应：JSON 信封 `{code,message,status,data}`

**JSON Body**

| 字段 | 读取方式 | 默认值 |
| --- | --- | --- |
| `shared_tweets` | `.get` | `[]` |
| `qrcode_url` | `.get` | `` |

### GET `/v2/api/tweets/share/get`

<a id="get-v2-api-tweets-share-get-15"></a>

根据code查询分享的tweet信息

- 路由键：`sharedTweetssGet`
- 鉴权：需要 x-api-key，免登录
- v1 镜像：`GET /v1/api/tweets/share/get`（同一 handler；v1 不校验 `x-api-key`）
- 实现：`ml4gp/ml4gp/controller/shared_tweets.py:46` `ml4gp.controller.shared_tweets.query_shared_tweets`
- 响应：JSON 信封 `{code,message,status,data}`

**Query**

| 字段 | 读取方式 | 默认值 |
| --- | --- | --- |
| `code` | `.get` | 无 |

### POST `/v2/api/tweet/bot/comment/pic`

<a id="post-v2-api-tweet-bot-comment-pic-16"></a>

- 路由键：`TweetBotPic`
- 鉴权：需要 x-api-key，v2 免登录；v1 需登录
- v1 镜像：`POST /v1/api/tweet/bot/comment/pic`（同一 handler；v1 不校验 `x-api-key`）
- 实现：`ml4gp/ml4gp/controller/tweet_bot_pic.py:16` `ml4gp.controller.tweet_bot_pic.tweet_comment_to_pic`
- 响应：JSON 信封 `{code,message,status,data}`

**JSON Body**

| 字段 | 读取方式 | 默认值 |
| --- | --- | --- |
| `content` | `.get` | 无 |
| `language` | `.get` | `en` |
