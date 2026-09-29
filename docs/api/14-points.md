# 积分

本模块 15 个已挂载接口。通用约定见 [README](README.md)。

## 索引

| 方法 | 路径 | 鉴权 |
| --- | --- | --- |
| GET | [`/v2/api/points/getUserPointsInfo`](#get-v2-api-points-getuserpointsinfo-1) | 需要 x-api-key，需登录 |
| GET | [`/v2/api/points/getUserSignInfo`](#get-v2-api-points-getusersigninfo-2) | 需要 x-api-key，需登录 |
| POST | [`/v2/api/points/sign`](#post-v2-api-points-sign-3) | 需要 x-api-key，需登录 |
| POST | [`/v2/api/points/share`](#post-v2-api-points-share-4) | 需要 x-api-key，需登录 |
| GET | [`/v2/api/points/getUserShareCount`](#get-v2-api-points-getusersharecount-5) | 需要 x-api-key，需登录 |
| GET | [`/v2/api/points/getUserActList`](#get-v2-api-points-getuseractlist-6) | 需要 x-api-key，需登录 |
| POST | [`/v2/api/points/pointsCharge`](#post-v2-api-points-pointscharge-7) | 需要 x-api-key，需登录 |
| POST | [`/v2/api/points/pointsExchange`](#post-v2-api-points-pointsexchange-8) | 需要 x-api-key，需登录 |
| POST | [`/v2/api/points/confirmExchange`](#post-v2-api-points-confirmexchange-9) | 需要 x-api-key，需登录 |
| POST | [`/v2/api/pay/preCharge`](#post-v2-api-pay-precharge-10) | 需要 x-api-key，需登录 |
| POST | [`/v2/api/pay/uploadHash`](#post-v2-api-pay-uploadhash-11) | 需要 x-api-key，需登录 |
| GET | [`/v2/api/pay/getBoughtList`](#get-v2-api-pay-getboughtlist-12) | 需要 x-api-key，需登录 |
| GET | [`/v2/api/points/insight/analysis/check`](#get-v2-api-points-insight-analysis-check-13) | 需要 x-api-key，需登录 |
| GET | [`/v2/api/userLanguageSetting`](#get-v2-api-userlanguagesetting-14) | 需要 x-api-key，v2 免登录；v1 需登录 |
| GET | [`/v2/api/userFmcCode`](#get-v2-api-userfmccode-15) | 需要 x-api-key，v2 免登录；v1 需登录 |

## 详情

### GET `/v2/api/points/getUserPointsInfo`

<a id="get-v2-api-points-getuserpointsinfo-1"></a>

- 路由键：`getUserPointsInfo`
- 鉴权：需要 x-api-key，需登录
- v1 镜像：`GET /v1/api/points/getUserPointsInfo`（同一 handler；v1 不校验 `x-api-key`）
- 实现：`ml4gp/ml4gp/controller/points.py:11` `ml4gp.controller.points.get_user_points_info`
- 响应：JSON 信封 `{code,message,status,data}`

**Query**

| 字段 | 读取方式 | 默认值 |
| --- | --- | --- |
| `fixedSource` | `.get` | `` |

### GET `/v2/api/points/getUserSignInfo`

<a id="get-v2-api-points-getusersigninfo-2"></a>

- 路由键：`getUserSigninInfo`
- 鉴权：需要 x-api-key，需登录
- v1 镜像：`GET /v1/api/points/getUserSignInfo`（同一 handler；v1 不校验 `x-api-key`）
- 实现：`ml4gp/ml4gp/controller/points.py:19` `ml4gp.controller.points.get_user_sign_info`
- 响应：JSON 信封 `{code,message,status,data}`

无额外 query/body 字段（或参数在更下游动态拼装）。

### POST `/v2/api/points/sign`

<a id="post-v2-api-points-sign-3"></a>

- 路由键：`userSignin`
- 鉴权：需要 x-api-key，需登录
- v1 镜像：`POST /v1/api/points/sign`（同一 handler；v1 不校验 `x-api-key`）
- 实现：`ml4gp/ml4gp/controller/points.py:26` `ml4gp.controller.points.user_sign`
- 响应：JSON 信封 `{code,message,status,data}`

**JSON Body**

读取整包 `request.json`，字段在下游服务里拆，调用时按业务传 JSON 对象。

### POST `/v2/api/points/share`

<a id="post-v2-api-points-share-4"></a>

- 路由键：`userShare`
- 鉴权：需要 x-api-key，需登录
- v1 镜像：`POST /v1/api/points/share`（同一 handler；v1 不校验 `x-api-key`）
- 实现：`ml4gp/ml4gp/controller/points.py:37` `ml4gp.controller.points.user_share`
- 响应：JSON 信封 `{code,message,status,data}`
- 显式错误码：`POINTS_SHARE_COUNT_LIMITED`

**JSON Body**

| 字段 | 读取方式 | 默认值 |
| --- | --- | --- |
| `type` | `.get` | `1` |

### GET `/v2/api/points/getUserShareCount`

<a id="get-v2-api-points-getusersharecount-5"></a>

- 路由键：`getUserShareCount`
- 鉴权：需要 x-api-key，需登录
- v1 镜像：`GET /v1/api/points/getUserShareCount`（同一 handler；v1 不校验 `x-api-key`）
- 实现：`ml4gp/ml4gp/controller/points.py:47` `ml4gp.controller.points.get_user_share_count`
- 响应：JSON 信封 `{code,message,status,data}`

无额外 query/body 字段（或参数在更下游动态拼装）。

### GET `/v2/api/points/getUserActList`

<a id="get-v2-api-points-getuseractlist-6"></a>

- 路由键：`getUserActivityLists`
- 鉴权：需要 x-api-key，需登录
- v1 镜像：`GET /v1/api/points/getUserActList`（同一 handler；v1 不校验 `x-api-key`）
- 实现：`ml4gp/ml4gp/controller/points.py:52` `ml4gp.controller.points.get_user_act_list`
- 响应：JSON 信封 `{code,message,status,data}`

**Query**

| 字段 | 读取方式 | 默认值 |
| --- | --- | --- |
| `page` | `.get` | `1` |
| `pageNum` | `.get` | `20` |
| `activityType` | `.get` | `` |

### POST `/v2/api/points/pointsCharge`

<a id="post-v2-api-points-pointscharge-7"></a>

- 路由键：`pointsCharge`
- 鉴权：需要 x-api-key，需登录
- v1 镜像：`POST /v1/api/points/pointsCharge`（同一 handler；v1 不校验 `x-api-key`）
- 实现：`ml4gp/ml4gp/controller/points.py:61` `ml4gp.controller.points.points_charge`
- 响应：JSON 信封 `{code,message,status,data}`
- 显式错误码：`PARAMS_ERROR`

**JSON Body**

| 字段 | 读取方式 | 默认值 |
| --- | --- | --- |
| `chargeId` | `.get` | `` |

### POST `/v2/api/points/pointsExchange`

<a id="post-v2-api-points-pointsexchange-8"></a>

2024年12月25日针对AI洞察功能，新增了两个参数：newsid和language，其余场景不用这两个参数。newsid是快讯新闻id，language是语言:zh或者cn代表中文，en代表英文

- 路由键：`pointExchange`
- 鉴权：需要 x-api-key，需登录
- v1 镜像：`POST /v1/api/points/pointsExchange`（同一 handler；v1 不校验 `x-api-key`）
- 实现：`ml4gp/ml4gp/controller/points.py:71` `ml4gp.controller.points.points_exchange`
- 响应：JSON 信封 `{code,message,status,data}`
- 显式错误码：`PARAMS_ERROR`

**JSON Body**

| 字段 | 读取方式 | 默认值 |
| --- | --- | --- |
| `msggroup` | `.get` | `` |
| `msgid` | `.get` | `` |
| `scenario` | `.get` | `` |
| `newsid` | `.get` | 无 |
| `language` | `.get` | 无 |

### POST `/v2/api/points/confirmExchange`

<a id="post-v2-api-points-confirmexchange-9"></a>

- 路由键：`confirmExchange`
- 鉴权：需要 x-api-key，需登录
- v1 镜像：`POST /v1/api/points/confirmExchange`（同一 handler；v1 不校验 `x-api-key`）
- 实现：`ml4gp/ml4gp/controller/points.py:100` `ml4gp.controller.points.confirm_exchange`
- 响应：JSON 信封 `{code,message,status,data}`
- 显式错误码：`PARAMS_ERROR`, `POINTS_EXCHANGE_TIMES_LIMITED`

**JSON Body**

| 字段 | 读取方式 | 默认值 |
| --- | --- | --- |
| `msggroup` | `.get` | `` |
| `msgid` | `.get` | `` |
| `scenario` | `.get` | `` |

### POST `/v2/api/pay/preCharge`

<a id="post-v2-api-pay-precharge-10"></a>

- 路由键：`preCharge`
- 鉴权：需要 x-api-key，需登录
- v1 镜像：`POST /v1/api/pay/preCharge`（同一 handler；v1 不校验 `x-api-key`）
- 实现：`ml4gp/ml4gp/controller/points.py:114` `ml4gp.controller.points.pre_charge`
- 响应：JSON 信封 `{code,message,status,data}`
- 显式错误码：`PARAMS_ERROR`, `PAY_SCENARIO_DUPLICATED`, `PAY_SCENARIO_NOT_EXIST`, `PAY_SUB_ID_GET_ERROR`

**JSON Body**

| 字段 | 读取方式 | 默认值 |
| --- | --- | --- |
| `productType` | `.get` | `` |
| `productId` | `.get` | `` |
| `fixedSource` | `.get` | `` |

### POST `/v2/api/pay/uploadHash`

<a id="post-v2-api-pay-uploadhash-11"></a>

- 路由键：`uploadHash`
- 鉴权：需要 x-api-key，需登录
- v1 镜像：`POST /v1/api/pay/uploadHash`（同一 handler；v1 不校验 `x-api-key`）
- 实现：`ml4gp/ml4gp/controller/points.py:144` `ml4gp.controller.points.upload_hash`
- 响应：JSON 信封 `{code,message,status,data}`
- 显式错误码：`PARAMS_ERROR`

**JSON Body**

| 字段 | 读取方式 | 默认值 |
| --- | --- | --- |
| `productType` | `.get` | `` |
| `productId` | `.get` | `` |
| `usedPlugin` | `.get` | `0` |
| `chargeHash` | `.get` | `` |
| `chargeChain` | `.get` | `` |

### GET `/v2/api/pay/getBoughtList`

<a id="get-v2-api-pay-getboughtlist-12"></a>

- 路由键：`getBoughtList`
- 鉴权：需要 x-api-key，需登录
- v1 镜像：`GET /v1/api/pay/getBoughtList`（同一 handler；v1 不校验 `x-api-key`）
- 实现：`ml4gp/ml4gp/controller/points.py:135` `ml4gp.controller.points.get_bought_product_list`
- 响应：JSON 信封 `{code,message,status,data}`

**Query**

| 字段 | 读取方式 | 默认值 |
| --- | --- | --- |
| `page` | `.get` | `1` |
| `pageNum` | `.get` | `20` |

### GET `/v2/api/points/insight/analysis/check`

<a id="get-v2-api-points-insight-analysis-check-13"></a>

验证ai洞察是否需要扣积分

- 路由键：`CheckInsightAnalysisNeedPoints`
- 鉴权：需要 x-api-key，需登录
- v1 镜像：`GET /v1/api/points/insight/analysis/check`（同一 handler；v1 不校验 `x-api-key`）
- 实现：`ml4gp/ml4gp/controller/points.py:88` `ml4gp.controller.points.check_insight_analysis_need_points`
- 响应：JSON 信封 `{code,message,status,data}`

**Query**

| 字段 | 读取方式 | 默认值 |
| --- | --- | --- |
| `newsid` | `.get` | 无 |
| `language` | `.get` | 无 |

### GET `/v2/api/userLanguageSetting`

<a id="get-v2-api-userlanguagesetting-14"></a>

- 路由键：`UserLanguageSetting`
- 鉴权：需要 x-api-key，v2 免登录；v1 需登录
- v1 镜像：`GET /v1/api/userLanguageSetting`（同一 handler；v1 不校验 `x-api-key`）
- 实现：`ml4gp/ml4gp/controller/points.py:160` `ml4gp.controller.points.set_user_language_setting`
- 响应：JSON 信封 `{code,message,status,data}`

**Query**

| 字段 | 读取方式 | 默认值 |
| --- | --- | --- |
| `code` | `.get` | 无 |
| `language` | `.get` | `1` |

### GET `/v2/api/userFmcCode`

<a id="get-v2-api-userfmccode-15"></a>

- 路由键：`GetUserFmcCode`
- 鉴权：需要 x-api-key，v2 免登录；v1 需登录
- v1 镜像：`GET /v1/api/userFmcCode`（同一 handler；v1 不校验 `x-api-key`）
- 实现：`ml4gp/ml4gp/controller/points.py:171` `ml4gp.controller.points.get_user_fmc_code`
- 响应：JSON 信封 `{code,message,status,data}`

**Query**

| 字段 | 读取方式 | 默认值 |
| --- | --- | --- |
| `code` | `.get` | 无 |
| `device_type` | `.get` | 无 |
| `user_id` | `.get` | `0` |
| `language` | `.get` | 无 |
