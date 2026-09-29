# 分享图与 PDF

本模块 23 个已挂载接口。通用约定见 [README](README.md)。

## 索引

| 方法 | 路径 | 鉴权 |
| --- | --- | --- |
| POST | [`/v2/api/news/share/add`](#post-v2-api-news-share-add-1) | 需要 x-api-key，免登录 |
| GET | [`/v2/api/news/share/get`](#get-v2-api-news-share-get-2) | 需要 x-api-key，免登录 |
| POST | [`/v2/api/aiswap/token/info/share/add`](#post-v2-api-aiswap-token-info-share-add-3) | 需要 x-api-key，v2 免登录；v1 需登录 |
| GET | [`/v2/api/aiswap/token/info/share/get`](#get-v2-api-aiswap-token-info-share-get-4) | 需要 x-api-key，v2 免登录；v1 需登录 |
| POST | [`/v2/api/imageUpload`](#post-v2-api-imageupload-5) | 需要 x-api-key，v2 免登录；v1 需登录 |
| POST | [`/v2/api/imageListUpload`](#post-v2-api-imagelistupload-6) | 需要 x-api-key，v2 免登录；v1 需登录 |
| POST | [`/v2/api/share/pic/news`](#post-v2-api-share-pic-news-7) | 需要 x-api-key，v2 免登录；v1 需登录 |
| POST | [`/v2/api/share/pic/news/ai`](#post-v2-api-share-pic-news-ai-8) | 需要 x-api-key，v2 免登录；v1 需登录 |
| POST | [`/v2/api/share/pic/news/hot`](#post-v2-api-share-pic-news-hot-9) | 需要 x-api-key，v2 免登录；v1 需登录 |
| POST | [`/v2/api/share/pic/news/kol`](#post-v2-api-share-pic-news-kol-10) | 需要 x-api-key，v2 免登录；v1 需登录 |
| POST | [`/v2/api/share/pic/price_prediction`](#post-v2-api-share-pic-price-prediction-11) | 需要 x-api-key，v2 免登录；v1 需登录 |
| POST | [`/v2/api/share/pic/dashboard/ayalysis`](#post-v2-api-share-pic-dashboard-ayalysis-12) | 需要 x-api-key，v2 免登录；v1 需登录 |
| POST | [`/v2/api/share/pic/dashboard/news`](#post-v2-api-share-pic-dashboard-news-13) | 需要 x-api-key，v2 免登录；v1 需登录 |
| POST | [`/v2/api/share/pic/dashboard/kolortweeter`](#post-v2-api-share-pic-dashboard-kolortweeter-14) | 需要 x-api-key，v2 免登录；v1 需登录 |
| POST | [`/v2/api/share/pic/dashboard/analyst`](#post-v2-api-share-pic-dashboard-analyst-15) | 需要 x-api-key，v2 免登录；v1 需登录 |
| POST | [`/v2/api/share/pic/aiswap/token/info`](#post-v2-api-share-pic-aiswap-token-info-16) | 需要 x-api-key，v2 免登录；v1 需登录 |
| POST | [`/v2/api/share/pdf/news/crypto`](#post-v2-api-share-pdf-news-crypto-17) | 需要 x-api-key，v2 免登录；v1 需登录 |
| POST | [`/v2/api/share/pdf/news/ai`](#post-v2-api-share-pdf-news-ai-18) | 需要 x-api-key，v2 免登录；v1 需登录 |
| POST | [`/v2/api/share/pdf/kol/tweets`](#post-v2-api-share-pdf-kol-tweets-19) | 需要 x-api-key，v2 免登录；v1 需登录 |
| POST | [`/v2/api/share/pdf/gzh/article`](#post-v2-api-share-pdf-gzh-article-20) | 需要 x-api-key，v2 免登录；v1 需登录 |
| POST | [`/v2/api/transKOL`](#post-v2-api-transkol-21) | 需要 x-api-key，v2 免登录；v1 需登录 |
| GET | [`/v2/api/getBase64`](#get-v2-api-getbase64-22) | 需要 x-api-key，免登录 |
| POST | [`/v2/api/pic/base64`](#post-v2-api-pic-base64-23) | 需要 x-api-key，v2 免登录；v1 需登录 |

## 详情

### POST `/v2/api/news/share/add`

<a id="post-v2-api-news-share-add-1"></a>

添加分享新闻

- 路由键：`sharedNewsAdd`
- 鉴权：需要 x-api-key，免登录
- v1 镜像：`POST /v1/api/news/share/add`（同一 handler；v1 不校验 `x-api-key`）
- 实现：`ml4gp/ml4gp/controller/shared_news.py:9` `ml4gp.controller.shared_news.add_share_news`
- 响应：JSON 信封 `{code,message,status,data}`

**JSON Body**

| 字段 | 读取方式 | 默认值 |
| --- | --- | --- |
| `shared_news` | `.get` | `[]` |
| `qrcode_url` | `.get` | `` |

### GET `/v2/api/news/share/get`

<a id="get-v2-api-news-share-get-2"></a>

根据code查询分享的新闻列表

- 路由键：`sharedNewsGet`
- 鉴权：需要 x-api-key，免登录
- v1 镜像：`GET /v1/api/news/share/get`（同一 handler；v1 不校验 `x-api-key`）
- 实现：`ml4gp/ml4gp/controller/shared_news.py:35` `ml4gp.controller.shared_news.query_shared_news`
- 响应：JSON 信封 `{code,message,status,data}`

**Query**

| 字段 | 读取方式 | 默认值 |
| --- | --- | --- |
| `code` | `.get` | 无 |

### POST `/v2/api/aiswap/token/info/share/add`

<a id="post-v2-api-aiswap-token-info-share-add-3"></a>

添加AI兑换推荐币种详情

- 路由键：`sharedAiswapTokenInfoAdd`
- 鉴权：需要 x-api-key，v2 免登录；v1 需登录
- v1 镜像：`POST /v1/api/aiswap/token/info/share/add`（同一 handler；v1 不校验 `x-api-key`）
- 实现：`ml4gp/ml4gp/controller/shared_aiswap_token_info.py:9` `ml4gp.controller.shared_aiswap_token_info.add_aiswap_token_info`
- 响应：JSON 信封 `{code,message,status,data}`

**JSON Body**

| 字段 | 读取方式 | 默认值 |
| --- | --- | --- |
| `shared_token_info` | `.get` | `{}` |
| `qrcode_url` | `.get` | `` |

### GET `/v2/api/aiswap/token/info/share/get`

<a id="get-v2-api-aiswap-token-info-share-get-4"></a>

根据code查询AI兑换推荐币种详情

- 路由键：`sharedAiswapTokenInfoGet`
- 鉴权：需要 x-api-key，v2 免登录；v1 需登录
- v1 镜像：`GET /v1/api/aiswap/token/info/share/get`（同一 handler；v1 不校验 `x-api-key`）
- 实现：`ml4gp/ml4gp/controller/shared_aiswap_token_info.py:27` `ml4gp.controller.shared_aiswap_token_info.query_shared_aiswap_token_info`
- 响应：JSON 信封 `{code,message,status,data}`

**Query**

| 字段 | 读取方式 | 默认值 |
| --- | --- | --- |
| `code` | `.get` | 无 |

### POST `/v2/api/imageUpload`

<a id="post-v2-api-imageupload-5"></a>

- 路由键：`imageUpload`
- 鉴权：需要 x-api-key，v2 免登录；v1 需登录
- v1 镜像：`POST /v1/api/imageUpload`（同一 handler；v1 不校验 `x-api-key`）
- 实现：`ml4gp/ml4gp/controller/image_upload.py:11` `ml4gp.controller.image_upload.image_upload`
- 响应：JSON 信封 `{code,message,status,data}`
- `data` 字面量键：`file_url`
- 显式错误码：`BASE64_FORMAT_ERROR`, `UPLOAD_FAIL`

**JSON Body**

| 字段 | 读取方式 | 默认值 |
| --- | --- | --- |
| `base64content` | `.get` | 无 |
| `type` | `.get` | `png` |

### POST `/v2/api/imageListUpload`

<a id="post-v2-api-imagelistupload-6"></a>

- 路由键：`imageListUpload`
- 鉴权：需要 x-api-key，v2 免登录；v1 需登录
- v1 镜像：`POST /v1/api/imageListUpload`（同一 handler；v1 不校验 `x-api-key`）
- 实现：`ml4gp/ml4gp/controller/image_upload.py:30` `ml4gp.controller.image_upload.image_list_upload`
- 响应：JSON 信封 `{code,message,status,data}`
- `data` 字面量键：`files_url`

**JSON Body**

| 字段 | 读取方式 | 默认值 |
| --- | --- | --- |
| `image_list` | `.get` | `[]` |

### POST `/v2/api/share/pic/news`

<a id="post-v2-api-share-pic-news-7"></a>

- 路由键：`SharePicNews`
- 鉴权：需要 x-api-key，v2 免登录；v1 需登录
- v1 镜像：`POST /v1/api/share/pic/news`（同一 handler；v1 不校验 `x-api-key`）
- 实现：`ml4gp/ml4gp/controller/share_pic.py:40` `ml4gp.controller.share_pic.share_pic_news`
- 响应：JSON 信封 `{code,message,status,data}`

**JSON Body**

| 字段 | 读取方式 | 默认值 |
| --- | --- | --- |
| `day` | `.get` | 无 |
| `year_month` | `.get` | 无 |
| `time` | `.get` | 无 |
| `title` | `.get` | 无 |
| `content` | `.get` | 无 |
| `duanping` | `.get` | 无 |
| `black_or_white` | `.get` | 无 |
| `pc_or_phone` | `.get` | `pc` |
| `language` | `.get` | `en` |
| `pic_url` | `.get` | `` |
| `client` | `.get` | `web` |
| `fixedSource` | `.get` | `` |
| `rewrite_type` | `.get` | `` |
| `sentiment` | `.get` | `null` |
| `symbol` | `.get` | `null` |
| `article_url` | `.get` | 无 |
| `url` | `.get` | 无 |
| `link` | `.get` | 无 |
| `articleUrl` | `.get` | 无 |
| `tweets_url` | `.get` | 无 |

### POST `/v2/api/share/pic/news/ai`

<a id="post-v2-api-share-pic-news-ai-8"></a>

- 路由键：`SharePicNewsAi`
- 鉴权：需要 x-api-key，v2 免登录；v1 需登录
- v1 镜像：`POST /v1/api/share/pic/news/ai`（同一 handler；v1 不校验 `x-api-key`）
- 实现：`ml4gp/ml4gp/controller/share_pic.py:94` `ml4gp.controller.share_pic.share_pic_news_ai`
- 响应：JSON 信封 `{code,message,status,data}`

**JSON Body**

| 字段 | 读取方式 | 默认值 |
| --- | --- | --- |
| `day` | `.get` | 无 |
| `year_month` | `.get` | 无 |
| `time` | `.get` | 无 |
| `title` | `.get` | 无 |
| `content` | `.get` | 无 |
| `duanping` | `.get` | 无 |
| `black_or_white` | `.get` | 无 |
| `pc_or_phone` | `.get` | `pc` |
| `language` | `.get` | `en` |
| `pic_url` | `.get` | `` |
| `client` | `.get` | `web` |
| `fixedSource` | `.get` | `` |
| `rewrite_type` | `.get` | `` |
| `article_url` | `.get` | 无 |
| `url` | `.get` | 无 |
| `link` | `.get` | 无 |
| `articleUrl` | `.get` | 无 |
| `tweets_url` | `.get` | 无 |

### POST `/v2/api/share/pic/news/hot`

<a id="post-v2-api-share-pic-news-hot-9"></a>

- 路由键：`SharePicNewsHot`
- 鉴权：需要 x-api-key，v2 免登录；v1 需登录
- v1 镜像：`POST /v1/api/share/pic/news/hot`（同一 handler；v1 不校验 `x-api-key`）
- 实现：`ml4gp/ml4gp/controller/share_pic.py:146` `ml4gp.controller.share_pic.share_pic_news_hot`
- 响应：JSON 信封 `{code,message,status,data}`

**JSON Body**

| 字段 | 读取方式 | 默认值 |
| --- | --- | --- |
| `phase` | `.get` | 无 |
| `newses` | `.get` | 无 |
| `black_or_white` | `.get` | 无 |
| `pc_or_phone` | `.get` | `pc` |
| `language` | `.get` | `en` |
| `client` | `.get` | `web` |
| `week_range` | `.get` | 无 |
| `fixedSource` | `.get` | `` |

### POST `/v2/api/share/pic/news/kol`

<a id="post-v2-api-share-pic-news-kol-10"></a>

- 路由键：`ShareKOLNews`
- 鉴权：需要 x-api-key，v2 免登录；v1 需登录
- v1 镜像：`POST /v1/api/share/pic/news/kol`（同一 handler；v1 不校验 `x-api-key`）
- 实现：`ml4gp/ml4gp/controller/share_pic.py:183` `ml4gp.controller.share_pic.share_kol_tweets`
- 响应：JSON 信封 `{code,message,status,data}`

**JSON Body**

| 字段 | 读取方式 | 默认值 |
| --- | --- | --- |
| `day` | `.get` | 无 |
| `year_month` | `.get` | 无 |
| `time` | `.get` | 无 |
| `title` | `.get` | 无 |
| `content` | `.get` | 无 |
| `content_trans` | `.get` | `` |
| `content_rewrite` | `.get` | 无 |
| `trans_type` | `.get` | `` |
| `kol_img` | `.get` | 无 |
| `kol_name` | `.get` | 无 |
| `black_or_white` | `.get` | 无 |
| `pc_or_phone` | `.get` | `pc` |
| `language` | `.get` | `en` |
| `name` | `.get` | `` |
| `pic_url` | `.get` | `` |
| `client` | `.get` | `web` |
| `fixedSource` | `.get` | `` |
| `rewrite_type` | `.get` | `` |

### POST `/v2/api/share/pic/price_prediction`

<a id="post-v2-api-share-pic-price-prediction-11"></a>

- 路由键：`SharePricePrediction`
- 鉴权：需要 x-api-key，v2 免登录；v1 需登录
- v1 镜像：`POST /v1/api/share/pic/price_prediction`（同一 handler；v1 不校验 `x-api-key`）
- 实现：`ml4gp/ml4gp/controller/share_pic.py:233` `ml4gp.controller.share_pic.share_price_predict_web`
- 响应：JSON 信封 `{code,message,status,data}`

**JSON Body**

| 字段 | 读取方式 | 默认值 |
| --- | --- | --- |
| `code` | `.get` | 无 |
| `language` | `.get` | 无 |
| `month_day` | `.get` | 无 |
| `year` | `.get` | 无 |
| `week` | `.get` | 无 |
| `black_or_white` | `.get` | 无 |
| `pc_or_phone` | `.get` | `pc` |
| `day_predict_time` | `.get` | `` |
| `day_predict_price` | `.get` | `` |
| `operation` | `.get` | `` |
| `reason` | `.get` | `` |
| `utcOffset` | `.get` | `` |
| `client` | `.get` | `web` |
| `kline` | `.get` | `` |
| `pre_kline` | `.get` | `` |

### POST `/v2/api/share/pic/dashboard/ayalysis`

<a id="post-v2-api-share-pic-dashboard-ayalysis-12"></a>

- 路由键：`ShareDashboardAnalysis`
- 鉴权：需要 x-api-key，v2 免登录；v1 需登录
- v1 镜像：`POST /v1/api/share/pic/dashboard/ayalysis`（同一 handler；v1 不校验 `x-api-key`）
- 实现：`ml4gp/ml4gp/controller/share_pic.py:363` `ml4gp.controller.share_pic.share_pic_dashboard_analysis`
- 响应：JSON 信封 `{code,message,status,data}`

**JSON Body**

| 字段 | 读取方式 | 默认值 |
| --- | --- | --- |
| `token_pic_url` | `.get` | 无 |
| `title` | `.get` | 无 |
| `content_title` | `.get` | 无 |
| `content` | `.get` | 无 |
| `time` | `.get` | 无 |
| `black_or_white` | `.get` | 无 |
| `pc_or_phone` | `.get` | `pc` |
| `language` | `.get` | `en` |
| `client` | `.get` | `web` |

### POST `/v2/api/share/pic/dashboard/news`

<a id="post-v2-api-share-pic-dashboard-news-13"></a>

- 路由键：`ShareDashboardNews`
- 鉴权：需要 x-api-key，v2 免登录；v1 需登录
- v1 镜像：`POST /v1/api/share/pic/dashboard/news`（同一 handler；v1 不校验 `x-api-key`）
- 实现：`ml4gp/ml4gp/controller/share_pic.py:402` `ml4gp.controller.share_pic.share_pic_dashboard_news`
- 响应：JSON 信封 `{code,message,status,data}`

**JSON Body**

| 字段 | 读取方式 | 默认值 |
| --- | --- | --- |
| `title` | `.get` | 无 |
| `content` | `.get` | 无 |
| `time` | `.get` | 无 |
| `black_or_white` | `.get` | 无 |
| `pc_or_phone` | `.get` | `pc` |
| `language` | `.get` | `en` |
| `client` | `.get` | `web` |

### POST `/v2/api/share/pic/dashboard/kolortweeter`

<a id="post-v2-api-share-pic-dashboard-kolortweeter-14"></a>

- 路由键：`ShareDashboardKolOrTweeter`
- 鉴权：需要 x-api-key，v2 免登录；v1 需登录
- v1 镜像：`POST /v1/api/share/pic/dashboard/kolortweeter`（同一 handler；v1 不校验 `x-api-key`）
- 实现：`ml4gp/ml4gp/controller/share_pic.py:438` `ml4gp.controller.share_pic.share_pic_dashboard_kol_and_tweeter`
- 响应：JSON 信封 `{code,message,status,data}`

**JSON Body**

| 字段 | 读取方式 | 默认值 |
| --- | --- | --- |
| `user_pic_url` | `.get` | 无 |
| `name` | `.get` | 无 |
| `username` | `.get` | 无 |
| `time` | `.get` | 无 |
| `kol_or_tweet` | `.get` | 无 |
| `win_rate` | `.get` | 无 |
| `avg_return` | `.get` | 无 |
| `follower` | `.get` | 无 |
| `content` | `.get` | 无 |
| `black_or_white` | `.get` | 无 |
| `pc_or_phone` | `.get` | `pc` |
| `language` | `.get` | `en` |
| `client` | `.get` | `web` |

### POST `/v2/api/share/pic/dashboard/analyst`

<a id="post-v2-api-share-pic-dashboard-analyst-15"></a>

- 路由键：`ShareDashboardAnalyst`
- 鉴权：需要 x-api-key，v2 免登录；v1 需登录
- v1 镜像：`POST /v1/api/share/pic/dashboard/analyst`（同一 handler；v1 不校验 `x-api-key`）
- 实现：`ml4gp/ml4gp/controller/share_pic.py:482` `ml4gp.controller.share_pic.share_pic_dashboard_analyst`
- 响应：JSON 信封 `{code,message,status,data}`

**JSON Body**

| 字段 | 读取方式 | 默认值 |
| --- | --- | --- |
| `name` | `.get` | 无 |
| `time` | `.get` | 无 |
| `content` | `.get` | 无 |
| `black_or_white` | `.get` | 无 |
| `pc_or_phone` | `.get` | `pc` |
| `language` | `.get` | `en` |
| `client` | `.get` | `web` |

### POST `/v2/api/share/pic/aiswap/token/info`

<a id="post-v2-api-share-pic-aiswap-token-info-16"></a>

- 路由键：`ShareAiswapTokenInfo`
- 鉴权：需要 x-api-key，v2 免登录；v1 需登录
- v1 镜像：`POST /v1/api/share/pic/aiswap/token/info`（同一 handler；v1 不校验 `x-api-key`）
- 实现：`ml4gp/ml4gp/controller/share_pic.py:518` `ml4gp.controller.share_pic.share_pic_aiswap_token_info`
- 响应：JSON 信封 `{code,message,status,data}`

**JSON Body**

| 字段 | 读取方式 | 默认值 |
| --- | --- | --- |
| `token_image_url` | `.get` | 无 |
| `symbol` | `.get` | 无 |
| `name` | `.get` | 无 |
| `price` | `.get` | 无 |
| `content` | `.get` | 无 |
| `black_or_white` | `.get` | 无 |
| `pc_or_phone` | `.get` | `pc` |
| `language` | `.get` | `en` |
| `client` | `.get` | `web` |

### POST `/v2/api/share/pdf/news/crypto`

<a id="post-v2-api-share-pdf-news-crypto-17"></a>

- 路由键：`SharePdfNewsCrypto`
- 鉴权：需要 x-api-key，v2 免登录；v1 需登录
- v1 镜像：`POST /v1/api/share/pdf/news/crypto`（同一 handler；v1 不校验 `x-api-key`）
- 实现：`ml4gp/ml4gp/controller/share_pdf.py:8` `ml4gp.controller.share_pdf.share_pdf_news_crypto`
- 响应：JSON 信封 `{code,message,status,data}`

**JSON Body**

| 字段 | 读取方式 | 默认值 |
| --- | --- | --- |
| `day` | `.get` | 无 |
| `year` | `.get` | 无 |
| `month` | `.get` | 无 |
| `time` | `.get` | 无 |
| `title` | `.get` | 无 |
| `content` | `.get` | 无 |
| `duanping` | `.get` | 无 |
| `black_or_white` | `.get` | 无 |
| `pc_or_phone` | `.get` | `pc` |
| `language` | `.get` | `en` |
| `pic_url` | `.get` | `` |
| `client` | `.get` | `web` |
| `fixedSource` | `.get` | `` |
| `rewrite_type` | `.get` | `` |
| `return_type` | `.get` | `base64` |
| `sentiment` | `.get` | `null` |
| `symbol` | `.get` | `null` |
| `publisher` | `.get` | 无 |
| `share_publisher` | `.get` | 无 |

### POST `/v2/api/share/pdf/news/ai`

<a id="post-v2-api-share-pdf-news-ai-18"></a>

- 路由键：`SharePdfNewsAi`
- 鉴权：需要 x-api-key，v2 免登录；v1 需登录
- v1 镜像：`POST /v1/api/share/pdf/news/ai`（同一 handler；v1 不校验 `x-api-key`）
- 实现：`ml4gp/ml4gp/controller/share_pdf.py:42` `ml4gp.controller.share_pdf.share_pdf_news_ai`
- 响应：JSON 信封 `{code,message,status,data}`

**JSON Body**

| 字段 | 读取方式 | 默认值 |
| --- | --- | --- |
| `day` | `.get` | 无 |
| `year` | `.get` | 无 |
| `month` | `.get` | 无 |
| `time` | `.get` | 无 |
| `title` | `.get` | 无 |
| `content` | `.get` | 无 |
| `duanping` | `.get` | 无 |
| `black_or_white` | `.get` | 无 |
| `pc_or_phone` | `.get` | `pc` |
| `language` | `.get` | `en` |
| `pic_url` | `.get` | `` |
| `client` | `.get` | `web` |
| `fixedSource` | `.get` | `` |
| `rewrite_type` | `.get` | `` |
| `return_type` | `.get` | `base64` |
| `publisher` | `.get` | 无 |
| `share_publisher` | `.get` | 无 |

### POST `/v2/api/share/pdf/kol/tweets`

<a id="post-v2-api-share-pdf-kol-tweets-19"></a>

- 路由键：`SharePdfKolTweets`
- 鉴权：需要 x-api-key，v2 免登录；v1 需登录
- v1 镜像：`POST /v1/api/share/pdf/kol/tweets`（同一 handler；v1 不校验 `x-api-key`）
- 实现：`ml4gp/ml4gp/controller/share_pdf.py:95` `ml4gp.controller.share_pdf.share_pdf_kol_tweets`
- 响应：JSON 信封 `{code,message,status,data}`

**JSON Body**

| 字段 | 读取方式 | 默认值 |
| --- | --- | --- |
| `day` | `.get` | 无 |
| `year` | `.get` | 无 |
| `month` | `.get` | 无 |
| `time` | `.get` | 无 |
| `title` | `.get` | 无 |
| `content` | `.get` | 无 |
| `content_trans` | `.get` | `` |
| `content_rewrite` | `.get` | 无 |
| `trans_type` | `.get` | `` |
| `kol_img` | `.get` | 无 |
| `kol_name` | `.get` | 无 |
| `black_or_white` | `.get` | 无 |
| `pc_or_phone` | `.get` | `pc` |
| `language` | `.get` | `en` |
| `name` | `.get` | `` |
| `pic_url` | `.get` | `` |
| `client` | `.get` | `web` |
| `fixedSource` | `.get` | `` |
| `rewrite_type` | `.get` | `` |
| `return_type` | `.get` | `base64` |

### POST `/v2/api/share/pdf/gzh/article`

<a id="post-v2-api-share-pdf-gzh-article-20"></a>

- 路由键：`SharePdfGzhArticle`
- 鉴权：需要 x-api-key，v2 免登录；v1 需登录
- v1 镜像：`POST /v1/api/share/pdf/gzh/article`（同一 handler；v1 不校验 `x-api-key`）
- 实现：`ml4gp/ml4gp/controller/share_pdf.py:74` `ml4gp.controller.share_pdf.share_pdf_gzh_article`
- 响应：JSON 信封 `{code,message,status,data}`

**JSON Body**

| 字段 | 读取方式 | 默认值 |
| --- | --- | --- |
| `gzh_art_id` | `.get` | 无 |
| `black_or_white` | `.get` | `black` |
| `language` | `.get` | `cn` |
| `return_type` | `.get` | `base64` |
| `time_zone` | `.get` | `Asia/Shanghai` |

### POST `/v2/api/transKOL`

<a id="post-v2-api-transkol-21"></a>

- 路由键：`TransKOL`
- 鉴权：需要 x-api-key，v2 免登录；v1 需登录
- v1 镜像：`POST /v1/api/transKOL`（同一 handler；v1 不校验 `x-api-key`）
- 实现：`ml4gp/ml4gp/controller/share_pic.py:315` `ml4gp.controller.share_pic.trans_kol`
- 响应：JSON 信封 `{code,message,status,data}`
- `data` 字面量键：`origin`, `trans`

**JSON Body**

| 字段 | 读取方式 | 默认值 |
| --- | --- | --- |
| `content` | `.get` | 无 |
| `language` | `.get` | 无 |
| `lan` | `.get` | 无 |

### GET `/v2/api/getBase64`

<a id="get-v2-api-getbase64-22"></a>

- 路由键：`getBase64`
- 鉴权：需要 x-api-key，免登录
- v1 镜像：`GET /v1/api/getBase64`（同一 handler；v1 不校验 `x-api-key`）
- 实现：`ml4gp/ml4gp/controller/share_pic.py:356` `ml4gp.controller.share_pic.get_base64_by_url`
- 响应：JSON 信封 `{code,message,status,data}`

**Query**

| 字段 | 读取方式 | 默认值 |
| --- | --- | --- |
| `url` | `.get` | 无 |

### POST `/v2/api/pic/base64`

<a id="post-v2-api-pic-base64-23"></a>

- 路由键：`getBase64New`
- 鉴权：需要 x-api-key，v2 免登录；v1 需登录
- v1 镜像：`POST /v1/api/pic/base64`（同一 handler；v1 不校验 `x-api-key`）
- 实现：`ml4gp/ml4gp/controller/comm_util.py:13` `ml4gp.controller.comm_util.get_base64`
- 响应：JSON 信封 `{code,message,status,data}`

**JSON Body**

| 字段 | 读取方式 | 默认值 |
| --- | --- | --- |
| `pic_urls` | `.get` | 无 |
