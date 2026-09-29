# 用户与账号

本模块 20 个已挂载接口。通用约定见 [README](README.md)。

## 索引

| 方法 | 路径 | 鉴权 |
| --- | --- | --- |
| POST | [`/v2/api/email/subscribe`](#post-v2-api-email-subscribe-1) | 需要 x-api-key，需登录 |
| GET | [`/v2/api/dailyBrief/open`](#get-v2-api-dailybrief-open-2) | 需要 x-api-key，v2 免登录；v1 需登录 |
| POST | [`/v2/api/dailyBrief/unsubscribe`](#post-v2-api-dailybrief-unsubscribe-3) | 需要 x-api-key，v2 免登录；v1 需登录 |
| POST | [`/v2/api/email/unsubscribe`](#post-v2-api-email-unsubscribe-4) | 需要 x-api-key，需登录 |
| GET | [`/v2/api/email/subscribe/check`](#get-v2-api-email-subscribe-check-5) | 需要 x-api-key，需登录 |
| POST | [`/v2/api/swftgpt/login`](#post-v2-api-swftgpt-login-6) | 需要 x-api-key，v2 免登录；v1 需登录 |
| POST | [`/v2/api/userLogin`](#post-v2-api-userlogin-7) | 需要 x-api-key，免登录 |
| GET | [`/v2/api/checkLogin`](#get-v2-api-checklogin-8) | 需要 x-api-key，需登录 |
| POST | [`/v2/api/register`](#post-v2-api-register-9) | 需要 x-api-key，免登录 |
| GET | [`/v2/api/loginOut`](#get-v2-api-loginout-10) | 需要 x-api-key，需登录 |
| POST | [`/v2/api/sendVerifyCode`](#post-v2-api-sendverifycode-11) | 需要 x-api-key，免登录 |
| POST | [`/v2/api/sendEmailCode`](#post-v2-api-sendemailcode-12) | 需要 x-api-key，免登录 |
| GET | [`/v2/api/getCaptcha`](#get-v2-api-getcaptcha-13) | 需要 x-api-key，免登录 |
| POST | [`/v2/api/testVerifyCode`](#post-v2-api-testverifycode-14) | 需要 x-api-key，免登录 |
| POST | [`/v2/api/modifyPassword`](#post-v2-api-modifypassword-15) | 需要 x-api-key，免登录 |
| POST | [`/v2/api/userLoginOther`](#post-v2-api-userloginother-16) | 需要 x-api-key，免登录 |
| POST | [`/v2/api/userCheckExist`](#post-v2-api-usercheckexist-17) | 需要 x-api-key，免登录 |
| POST | [`/v2/api/addFeedback`](#post-v2-api-addfeedback-18) | 需要 x-api-key，免登录 |
| POST | [`/v2/api/sendAppEmailCode`](#post-v2-api-sendappemailcode-19) | 需要 x-api-key，免登录 |
| POST | [`/v2/api/plugin/login`](#post-v2-api-plugin-login-20) | 需要 x-api-key，免登录 |

## 详情

### POST `/v2/api/email/subscribe`

<a id="post-v2-api-email-subscribe-1"></a>

- 路由键：`emailSubscribe`
- 鉴权：需要 x-api-key，需登录
- v1 镜像：`POST /v1/api/email/subscribe`（同一 handler；v1 不校验 `x-api-key`）
- 实现：`ml4gp/ml4gp/controller/email_subscribe.py:12` `ml4gp.controller.email_subscribe.subscribe`
- 响应：JSON 信封 `{code,message,status,data}`

**JSON Body**

| 字段 | 读取方式 | 默认值 |
| --- | --- | --- |
| `email` | `.get` | 无 |

### GET `/v2/api/dailyBrief/open`

<a id="get-v2-api-dailybrief-open-2"></a>

- 路由键：`dailyBriefOpen`
- 鉴权：需要 x-api-key，v2 免登录；v1 需登录
- v1 镜像：`GET /v1/api/dailyBrief/open`（同一 handler；v1 不校验 `x-api-key`）
- 实现：`ml4gp/ml4gp/controller/daily_brief.py:45` `ml4gp.controller.daily_brief.open_brief`
- 响应：JSON 信封 `{code,message,status,data}`

**Query**

| 字段 | 读取方式 | 默认值 |
| --- | --- | --- |
| `uid` | `.get` | 无 |
| `sig` | `.get` | 无 |
| `lang` | `.get` | 无 |
| `date` | `.get` | 无 |

### POST `/v2/api/dailyBrief/unsubscribe`

<a id="post-v2-api-dailybrief-unsubscribe-3"></a>

- 路由键：`dailyBriefUnsubscribe`
- 鉴权：需要 x-api-key，v2 免登录；v1 需登录
- v1 镜像：`POST /v1/api/dailyBrief/unsubscribe`（同一 handler；v1 不校验 `x-api-key`）
- 实现：`ml4gp/ml4gp/controller/daily_brief.py:127` `ml4gp.controller.daily_brief.unsubscribe_brief`
- 响应：JSON 信封 `{code,message,status,data}`

**Query**

| 字段 | 读取方式 | 默认值 |
| --- | --- | --- |
| `uid` | `.get` | 无 |
| `sig` | `.get` | 无 |
| `reason` | `.get` | 无 |

**JSON Body**

| 字段 | 读取方式 | 默认值 |
| --- | --- | --- |
| `uid` | `.get` | 无 |
| `sig` | `.get` | 无 |
| `reason` | `.get` | 无 |

### POST `/v2/api/email/unsubscribe`

<a id="post-v2-api-email-unsubscribe-4"></a>

- 路由键：`emailunSubscribe`
- 鉴权：需要 x-api-key，需登录
- v1 镜像：`POST /v1/api/email/unsubscribe`（同一 handler；v1 不校验 `x-api-key`）
- 实现：`ml4gp/ml4gp/controller/email_subscribe.py:46` `ml4gp.controller.email_subscribe.unsubscribe`
- 响应：JSON 信封 `{code,message,status,data}`

无额外 query/body 字段（或参数在更下游动态拼装）。

### GET `/v2/api/email/subscribe/check`

<a id="get-v2-api-email-subscribe-check-5"></a>

- 路由键：`checkEmailSubscribe`
- 鉴权：需要 x-api-key，需登录
- v1 镜像：`GET /v1/api/email/subscribe/check`（同一 handler；v1 不校验 `x-api-key`）
- 实现：`ml4gp/ml4gp/controller/email_subscribe.py:59` `ml4gp.controller.email_subscribe.checkSubscribe`
- 响应：JSON 信封 `{code,message,status,data}`

无额外 query/body 字段（或参数在更下游动态拼装）。

### POST `/v2/api/swftgpt/login`

<a id="post-v2-api-swftgpt-login-6"></a>

- 路由键：`swftgptLogin`
- 鉴权：需要 x-api-key，v2 免登录；v1 需登录
- v1 镜像：`POST /v1/api/swftgpt/login`（同一 handler；v1 不校验 `x-api-key`）
- 实现：`ml4gp/ml4gp/controller/swftgpt.py:10` `ml4gp.controller.swftgpt.swftgpt_login`
- 响应：JSON 信封 `{code,message,status,data}`
- 显式错误码：`PARAMS_ERROR`

**JSON Body**

| 字段 | 读取方式 | 默认值 |
| --- | --- | --- |
| `data` | `.get` | `{}` |

### POST `/v2/api/userLogin`

<a id="post-v2-api-userlogin-7"></a>

`type=0` 邮箱密码，要 `email`、`password`；`type=1` 钱包签名，要 `timestamp`、`signature`、`wallet_address`；`type=2` 第三方登录，要 `access_token`、`oauth`。

- 路由键：`login`
- 鉴权：需要 x-api-key，免登录
- 实现：`GenAI/genaipf/controller/user.py:17` `genaipf.controller.user.login`
- 响应：JSON 信封 `{code,message,status,data}`
- 显式错误码：`PARAMS_ERROR`

**JSON Body**

| 字段 | 读取方式 | 默认值 |
| --- | --- | --- |
| `type` | `.get` | `0` |
| `email` | `.get` | `` |
| `password` | `.get` | `` |
| `timestamp` | `.get` | `` |
| `signature` | `.get` | `` |
| `wallet_address` | `.get` | `` |
| `access_token` | `.get` | `` |
| `oauth` | `.get` | `` |

### GET `/v2/api/checkLogin`

<a id="get-v2-api-checklogin-8"></a>

- 路由键：`check_login`
- 鉴权：需要 x-api-key，需登录
- 实现：`GenAI/genaipf/controller/user.py:59` `genaipf.controller.user.check_login`
- 响应：JSON 信封 `{code,message,status,data}`
- `data` 字面量键：`is_login`, `account`, `user_id`

无额外 query/body 字段（或参数在更下游动态拼装）。

### POST `/v2/api/register`

<a id="post-v2-api-register-9"></a>

- 路由键：`register`
- 鉴权：需要 x-api-key，免登录
- 实现：`GenAI/genaipf/controller/user.py:84` `genaipf.controller.user.register`
- 响应：JSON 信封 `{code,message,status,data}`
- 显式错误码：`PARAMS_ERROR`

**JSON Body**

| 字段 | 读取方式 | 默认值 |
| --- | --- | --- |
| `email` | 下标，缺失会抛错 | 必有 |
| `password` | 下标，缺失会抛错 | 必有 |
| `verifyCode` | 下标，缺失会抛错 | 必有 |
| `inviter` | `.get` | `` |

### GET `/v2/api/loginOut`

<a id="get-v2-api-loginout-10"></a>

- 路由键：`login_out`
- 鉴权：需要 x-api-key，需登录
- 实现：`GenAI/genaipf/controller/user.py:114` `genaipf.controller.user.login_out`
- 响应：JSON 信封 `{code,message,status,data}`

无额外 query/body 字段（或参数在更下游动态拼装）。

### POST `/v2/api/sendVerifyCode`

<a id="post-v2-api-sendverifycode-11"></a>

- 路由键：`send_verify_code`
- 鉴权：需要 x-api-key，免登录
- 实现：`GenAI/genaipf/controller/user.py:123` `genaipf.controller.user.send_verify_code`
- 响应：JSON 信封 `{code,message,status,data}`
- 显式错误码：`PARAMS_ERROR`

**JSON Body**

| 字段 | 读取方式 | 默认值 |
| --- | --- | --- |
| `email` | 下标，缺失会抛错 | 必有 |
| `captchaCode` | 下标，缺失会抛错 | 必有 |

### POST `/v2/api/sendEmailCode`

<a id="post-v2-api-sendemailcode-12"></a>

- 路由键：`send_verify_code_new`
- 鉴权：需要 x-api-key，免登录
- 实现：`GenAI/genaipf/controller/user.py:135` `genaipf.controller.user.send_verify_code_new`
- 响应：JSON 信封 `{code,message,status,data}`
- 显式错误码：`PARAMS_ERROR`

**JSON Body**

| 字段 | 读取方式 | 默认值 |
| --- | --- | --- |
| `email` | `.get` | 无 |
| `cf-turnstile-response` | `.get` | `` |
| `language` | `.get` | `en` |
| `scene` | `.get` | `REGISTER` |

### GET `/v2/api/getCaptcha`

<a id="get-v2-api-getcaptcha-13"></a>

- 路由键：`get_captcha`
- 鉴权：需要 x-api-key，免登录
- 实现：`GenAI/genaipf/controller/user.py:172` `genaipf.controller.user.get_captcha`
- 响应：JSON 信封 `{code,message,status,data}`

无额外 query/body 字段（或参数在更下游动态拼装）。

### POST `/v2/api/testVerifyCode`

<a id="post-v2-api-testverifycode-14"></a>

- 路由键：`verify_captcha_code`
- 鉴权：需要 x-api-key，免登录
- 实现：`GenAI/genaipf/controller/user.py:187` `genaipf.controller.user.verify_captcha_code`
- 响应：JSON 信封 `{code,message,status,data}`

**Form**

| 字段 | 读取方式 | 默认值 |
| --- | --- | --- |
| `g-recaptcha-response` | `.get` | 无 |

### POST `/v2/api/modifyPassword`

<a id="post-v2-api-modifypassword-15"></a>

- 路由键：`modify_password`
- 鉴权：需要 x-api-key，免登录
- 实现：`GenAI/genaipf/controller/user.py:96` `genaipf.controller.user.modify_password`
- 响应：JSON 信封 `{code,message,status,data}`
- `data` 字面量键：`remain_num`
- 显式错误码：`MODIFY_PASSWORD_VERIFY_TIME_ERROR`, `PARAMS_ERROR`, `VERIFY_CODE_ERROR`

**JSON Body**

| 字段 | 读取方式 | 默认值 |
| --- | --- | --- |
| `email` | 下标，缺失会抛错 | 必有 |
| `password` | 下标，缺失会抛错 | 必有 |
| `verifyCode` | 下标，缺失会抛错 | 必有 |

### POST `/v2/api/userLoginOther`

<a id="post-v2-api-userloginother-16"></a>

- 路由键：`login_other`
- 鉴权：需要 x-api-key，免登录
- 实现：`GenAI/genaipf/controller/user.py:42` `genaipf.controller.user.login_other`
- 响应：JSON 信封 `{code,message,status,data}`
- 显式错误码：`PARAMS_ERROR`

**JSON Body**

| 字段 | 读取方式 | 默认值 |
| --- | --- | --- |
| `email` | `.get` | `` |
| `wallet_address` | `.get` | `` |
| `source` | `.get` | `` |

### POST `/v2/api/userCheckExist`

<a id="post-v2-api-usercheckexist-17"></a>

- 路由键：`check_exist`
- 鉴权：需要 x-api-key，免登录
- 实现：`GenAI/genaipf/controller/user.py:72` `genaipf.controller.user.check_exist`
- 响应：JSON 信封 `{code,message,status,data}`
- `data` 字面量键：`exist`
- 显式错误码：`PARAMS_ERROR`

**JSON Body**

| 字段 | 读取方式 | 默认值 |
| --- | --- | --- |
| `email` | 下标，缺失会抛错 | 必有 |

### POST `/v2/api/addFeedback`

<a id="post-v2-api-addfeedback-18"></a>

- 路由键：`add_feedback`
- 鉴权：需要 x-api-key，免登录
- 实现：`GenAI/genaipf/controller/feedback.py:10` `genaipf.controller.feedback.add_feedback`
- 响应：JSON 信封 `{code,message,status,data}`
- 显式错误码：`PARAMS_ERROR`

**JSON Body**

| 字段 | 读取方式 | 默认值 |
| --- | --- | --- |
| `seriousness` | 下标，缺失会抛错 | 必有 |
| `type` | 下标，缺失会抛错 | 必有 |
| `content` | 下标，缺失会抛错 | 必有 |
| `contact` | 下标，缺失会抛错 | 必有 |
| `bug_location` | `.get` | `` |
| `base64_content` | `.get` | `` |

### POST `/v2/api/sendAppEmailCode`

<a id="post-v2-api-sendappemailcode-19"></a>

- 路由键：`send_verify_code_mobile`
- 鉴权：需要 x-api-key，免登录
- 实现：`GenAI/genaipf/controller/user.py:149` `genaipf.controller.user.send_verify_code_mobile`
- 响应：JSON 信封 `{code,message,status,data}`
- 显式错误码：`PARAMS_ERROR`

**JSON Body**

| 字段 | 读取方式 | 默认值 |
| --- | --- | --- |
| `email` | `.get` | 无 |
| `language` | `.get` | `en` |
| `scene` | `.get` | `REGISTER` |
| `uuid` | `.get` | `` |
| `fixedSource` | `.get` | `MLAPP` |

### POST `/v2/api/plugin/login`

<a id="post-v2-api-plugin-login-20"></a>

- 路由键：`plugin_login`
- 鉴权：需要 x-api-key，免登录
- 实现：`GenAI/genaipf/controller/user.py:50` `genaipf.controller.user.plugin_login`
- 响应：JSON 信封 `{code,message,status,data}`
- 显式错误码：`PARAMS_ERROR`

**JSON Body**

| 字段 | 读取方式 | 默认值 |
| --- | --- | --- |
| `email` | `.get` | `` |
| `wallet_address` | `.get` | `` |
| `source` | `.get` | `` |
| `data` | `.get` | `{}` |
