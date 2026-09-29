# 应用配置

本模块 8 个已挂载接口。通用约定见 [README](README.md)。

## 索引

| 方法 | 路径 | 鉴权 |
| --- | --- | --- |
| GET | [`/v2/api/getTopics`](#get-v2-api-gettopics-1) | 需要 x-api-key，免登录 |
| GET | [`/v2/api/plugin/getTopics`](#get-v2-api-plugin-gettopics-2) | 需要 x-api-key，免登录 |
| GET | [`/v2/api/getPopups`](#get-v2-api-getpopups-3) | 需要 x-api-key，需登录 |
| GET | [`/v2/api/version/comment/list`](#get-v2-api-version-comment-list-4) | 需要 x-api-key，v2 免登录；v1 需登录 |
| POST | [`/v2/api/system/addInitTime`](#post-v2-api-system-addinittime-5) | 需要 x-api-key，v2 免登录；v1 需登录 |
| GET | [`/v2/api/ios/vip/config`](#get-v2-api-ios-vip-config-6) | 需要 x-api-key，v2 免登录；v1 需登录 |
| GET | [`/v2/api/del/user/info`](#get-v2-api-del-user-info-7) | 需要 x-api-key，需登录 |
| GET | [`/v2/api/app/info/latest`](#get-v2-api-app-info-latest-8) | 需要 x-api-key，v2 免登录；v1 需登录 |

## 详情

### GET `/v2/api/getTopics`

<a id="get-v2-api-gettopics-1"></a>

- 路由键：`getTopics`
- 鉴权：需要 x-api-key，免登录
- v1 镜像：`GET /v1/api/getTopics`（同一 handler；v1 不校验 `x-api-key`）
- 实现：`ml4gp/ml4gp/controller/topic.py:12` `ml4gp.controller.topic.get_topic_by_type`
- 响应：JSON 信封 `{code,message,status,data}`
- 显式错误码：`PARAMS_ERROR`

**Query**

| 字段 | 读取方式 | 默认值 |
| --- | --- | --- |
| `type` | `.get` | 无 |
| `coin` | `.get` | `` |

### GET `/v2/api/plugin/getTopics`

<a id="get-v2-api-plugin-gettopics-2"></a>

- 路由键：`getPluginTopics`
- 鉴权：需要 x-api-key，免登录
- v1 镜像：`GET /v1/api/plugin/getTopics`（同一 handler；v1 不校验 `x-api-key`）
- 实现：`ml4gp/ml4gp/controller/topic.py:24` `ml4gp.controller.topic.get_topic_by_plugin`
- 响应：JSON 信封 `{code,message,status,data}`
- 显式错误码：`PARAMS_ERROR`

**Query**

| 字段 | 读取方式 | 默认值 |
| --- | --- | --- |
| `source` | `.get` | 无 |
| `language` | `.get` | 无 |

### GET `/v2/api/getPopups`

<a id="get-v2-api-getpopups-3"></a>

- 路由键：`getPopup`
- 鉴权：需要 x-api-key，需登录
- v1 镜像：`GET /v1/api/getPopups`（同一 handler；v1 不校验 `x-api-key`）
- 实现：`ml4gp/ml4gp/controller/popup.py:9` `ml4gp.controller.popup.get_popups`
- 响应：JSON 信封 `{code,message,status,data}`

**Query**

| 字段 | 读取方式 | 默认值 |
| --- | --- | --- |
| `position` | `.get` | `homepage` |
| `type` | `.get` | `type` |

### GET `/v2/api/version/comment/list`

<a id="get-v2-api-version-comment-list-4"></a>

- 路由键：`VersionCommentList`
- 鉴权：需要 x-api-key，v2 免登录；v1 需登录
- v1 镜像：`GET /v1/api/version/comment/list`（同一 handler；v1 不校验 `x-api-key`）
- 实现：`ml4gp/ml4gp/controller/version_comment.py:7` `ml4gp.controller.version_comment.version_comment_list`
- 响应：JSON 信封 `{code,message,status,data}`

无额外 query/body 字段（或参数在更下游动态拼装）。

### POST `/v2/api/system/addInitTime`

<a id="post-v2-api-system-addinittime-5"></a>

- 路由键：`addInitTime`
- 鉴权：需要 x-api-key，v2 免登录；v1 需登录
- v1 镜像：`POST /v1/api/system/addInitTime`（同一 handler；v1 不校验 `x-api-key`）
- 实现：`ml4gp/ml4gp/controller/system.py:10` `ml4gp.controller.system.add_init_time`
- 响应：JSON 信封 `{code,message,status,data}`
- 显式错误码：`PARAMS_ERROR`

**JSON Body**

| 字段 | 读取方式 | 默认值 |
| --- | --- | --- |
| `startTime` | `.get` | `` |
| `endTime` | `.get` | `` |

**额外请求头**

| 字段 | 读取方式 | 默认值 |
| --- | --- | --- |
| `user-agent` | `.get` | `` |
| `referer` | `.get` | `` |

### GET `/v2/api/ios/vip/config`

<a id="get-v2-api-ios-vip-config-6"></a>

- 路由键：`getAppSettings`
- 鉴权：需要 x-api-key，v2 免登录；v1 需登录
- v1 镜像：`GET /v1/api/ios/vip/config`（同一 handler；v1 不校验 `x-api-key`）
- 实现：`ml4gp/ml4gp/controller/app_settings.py:8` `ml4gp.controller.app_settings.get_ios_vip_config`
- 响应：JSON 信封 `{code,message,status,data}`

**Query**

| 字段 | 读取方式 | 默认值 |
| --- | --- | --- |
| `v_id` | `.get` | `` |
| `channel` | `.get` | `` |

### GET `/v2/api/del/user/info`

<a id="get-v2-api-del-user-info-7"></a>

- 路由键：`delUserInfo`
- 鉴权：需要 x-api-key，需登录
- v1 镜像：`GET /v1/api/del/user/info`（同一 handler；v1 不校验 `x-api-key`）
- 实现：`ml4gp/ml4gp/controller/app_settings.py:15` `ml4gp.controller.app_settings.del_user_info`
- 响应：JSON 信封 `{code,message,status,data}`

**Query**

| 字段 | 读取方式 | 默认值 |
| --- | --- | --- |
| `user_id` | `.get` | `` |

### GET `/v2/api/app/info/latest`

<a id="get-v2-api-app-info-latest-8"></a>

- 路由键：`appInfoLatest`
- 鉴权：需要 x-api-key，v2 免登录；v1 需登录
- v1 镜像：`GET /v1/api/app/info/latest`（同一 handler；v1 不校验 `x-api-key`）
- 实现：`ml4gp/ml4gp/controller/app_info.py:7` `ml4gp.controller.app_info.app_info_latest`
- 响应：JSON 信封 `{code,message,status,data}`

**Query**

| 字段 | 读取方式 | 默认值 |
| --- | --- | --- |
| `version` | `.get` | 无 |
| `channel` | `.get` | 无 |
| `client` | `.get` | 无 |
