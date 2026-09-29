# Mlion 客户端 API（GenAI + ml4gp）

给自动化测试用的接口清单。范围是 **GenAI 进程实际挂载**、给 Web / H5 / iOS / Android 调用的 HTTP 接口。

- 宿主路由：`GenAI/genaipf/routers/routers.py`（只统计未注释的 `add_route`）
- 插件路由：`ml4gp/ml4gp/routers/entry.py` 的 `plugin_router_mapping`（启动时同时挂到 v1 与 v2）
- 免登录名单：`genaipf/conf/path_without_login.py` + `ml4gp/routers/without_login.py`
- 机器可读清单：[catalog.json](catalog.json)（字段从控制器源码静态提取）

接口总数：**299**（按方法计；插件接口的 v1 镜像不重复计数）。

## 环境

| 项 | 值 |
| --- | --- |
| 测试环境 | `https://api-test.mountainlion.ai`（以实际网关为准） |
| 主路径 | `/v2/api/{uri}` |
| 插件镜像 | 同一 handler 同时在 `/v1/api/{uri}` |
| 旧聊天入口 | `/mpcbot/sendchat_gpt4` |

客户端当前应打 **v2**。v1 上 GenAI 自己的用户/聊天路由已注释，只剩插件镜像。

## 每个请求都要带的头

`/v2/api/*` 在进业务前过 `check_api_key`（`genaipf/middlewares/api_key_middleware.py`）：

| 头 | 必填 | 说明 |
| --- | --- | --- |
| `x-api-key` | v2 必填 | Redis 集合里的合法 key。缺失或非法返回 `code=4002` |
| `Authorization` | 需登录的接口 | `Bearer <jwt>`。Sanic 用 `request.token` 取 Bearer token |
| `Content-Type` | 有 JSON body 时 | `application/json` |

限制：同一 `x-api-key` + IP **每分钟 200 次**，超出后封禁 15 分钟，返回 `code=4003`。IP 在黑名单同样 `4003`。

`/v1/api/*` 与 `/mpcbot/*` **不跑** `x-api-key` 中间件。登录校验是全局限流前的 `check_user`，v1/v2 都生效。

免登录接口如果带了合法 token，仍会写入 `request.ctx.user`（用于白名单、个性化）。token 非法时免登录接口直接放行，不报 4001。

## 响应信封

成功：

```json
{"code": 200, "message": "success", "status": "true", "data": {}}
```

失败（`fail()`）：

```json
{"code": 4001, "message": "User Not Authorized ...", "status": "false"}
```

`message` 前半段是 `ERROR_MESSAGE[code]`，后半段是调用处附加文案。业务异常 `CustomerError` 也走同一套 code。

部分兑换接口用另一套：`resCode` / `resMsg` / `data`（`success_for_path`）。文档里响应类型标成 `file` 或 `sse` 的接口不是这个 JSON。

## 登录判定

路径（去掉尾部 `/` 后）命中免登录名单则不要求 token。`/static/` 一律免登录。

文档里「需登录」表示 **v2 路径** 不在名单里。插件接口若 v1 与 v2 名单不一致，详情里会分开写。

## 区域限制

`REGION_RESTRICT_US_ENABLED=true` 时，`/v1/api`、`/v2/api`、`/mpcbot` 会拦美国来源，`code=5021`。登录/注册一类接口在豁免名单里。细节见 [region-restriction-us.md](../region-restriction-us.md)。白名单管理接口见 [04-region.md](04-region.md)。

## 错误码

| code | 常量 | message |
| --- | --- | --- |
| 1001 | `PARAMS_ERROR` | Params error |
| 1002 | `INVALID_SIGNATURE` | INVALID_SIGNATURE |
| 2001 | `USER_NOT_EXIST` | User not exist |
| 2002 | `PWD_ERROR` | User password error |
| 2003 | `EMPTY_USER_TOKEN` | User Token is empty |
| 2004 | `CAPTCHA_ERROR` | Captcha code error |
| 2005 | `USER_EXIST` | User already exists, please use another email |
| 2006 | `VERIFY_CODE_ERROR` | Email verify-code error |
| 2007 | `EMAIL_LIMIT` | Send Email Limit |
| 2008 | `EMAIL_TIME_LIMIT` | Send Email Time-limit, Please Try Later |
| 2009 | `REGISTER_ERROR` | User Register Error |
| 2010 | `MODIFY_PASSWORD_ERROR` | User Modify Password Error |
| 2011 | `LOGIN_EXPIRED` | User Login Time Out |
| 2012 | `WALLET_SIGN_ERROR` | User Wallet Sign Message Error |
| 2013 | `GOOGLE_OAUTH_ERROR` | Request is missing required authentication credential |
| 2014 | `MODIFY_USER_PROFILE_ERROR` | MODIFY_USER_PROFILE_ERROR |
| 2015 | `MODIFY_PASSWORD_VERIFY_TIME_ERROR` | Modify Password Time Limit |
| 4001 | `NOT_AUTHORIZED` | User Not Authorized |
| 4002 | `ILLEGAL_REQUEST` | Illegal Request |
| 4003 | `REQUEST_FREQUENCY_TOO_HIGH` | Request Frequency Is Too High |
| 5001 | `TOKEN_NOT_SUPPORTED` | The token you mentioned not supported |
| 5021 | `REGION_NOT_SUPPORTED` | Service is not available in your region |
| 5022 | `REGION_WHITELIST_ADMIN_INVALID` | Region whitelist admin authentication failed |
| 5023 | `REGION_WHITELIST_ADMIN_FORBIDDEN` | Region whitelist admin operator not allowed |
| 5003 | `PLATFORM_NOT_SUPPORTED` | The platform not supported swap |
| 5004 | `NO_REMAINING_TIMES` | No remaining times |
| 5005 | `NO_REMAINING_QUERIES_TIME` | No remaining queries times |
| 6001 | `PATH_API_ERROR` | Path Api Request Error |
| 6002 | `SWAP_OUT_OF_RANGE` | Exchange Out of Range |
| 6003 | `SWAP_ADDRESS_ERROR` | Swap From or To Address Error |
| 6004 | `RAG_CONFIG_ERROR` | Rag config error |
| 7001 | `CHAIN_NOT_SUPPORTED` | The Chain Not Supported |
| 8001 | `USER_ACTIVITY_NOT_EXIST` | User Account Activity Not Exist |
| 8002 | `REPEAT_RECHARGE` | Repeat Recharge |
| 8003 | `USER_SUB_ACCOUNT_NOT_EXIST` | User Sub Accout Not Exist |
| 8004 | `CREATE_RECORD_ERROR` | Create Record Error |
| 8005 | `SWAP_BALANCE_NOT_ENOUGH` | Balance Not Enough |
| 8006 | `SWAP_API_ERROR` | Swap API Error |
| 8007 | `CREATE_ACTIVITY_ERROR` | Create Activity Error |
| 8008 | `TOKEN_CANT_WITHDRAW` | The Token Cannot Withdraw Right Now |
| 8009 | `WITHDRAW_BALANCE_NOT_ENOUGH` | Withdraw Balance Not Enough |
| 8010 | `WITHDRAW_AMT_MIN` | Withdraw Amount Too Small |
| 8011 | `PRE_WITHDRAW_API` | Request Pre Withdraw Api Error, Maybe Email Problem |
| 8012 | `CHECK_WITHDRAW_INFO_ERROR` | Check Withdraw Info Error |
| 8013 | `WITHDRAW_API_ERROR` | Withdraw API Error |
| 8014 | `USER_MAIN_ACCOUNT_NOT_EXIST` | User Main Account Not Supported |
| 8015 | `LIMIT_ORDER_NOT_EXIST` | Limit Order Not Exsit |
| 8016 | `WALLET_ADDRESS_IS_EMPTY` | Wallet Address is Empty |
| 8017 | `FREE_FREEZE_ACCOUNT_ERROR` | Free Freeze Account Error |
| 8018 | `LIMIT_STATUS_ORDER_ERROR` | Limit Order Status Error |
| 9001 | `PAY_SCENARIO_NOT_EXIST` | Pay Scenario Not Exist |
| 9002 | `PAY_SCENARIO_BALANCE_NOT_ENOUGH` | Pay Scenario Balance Not Enough |
| 9003 | `PAY_SCENARIO_TOKEN_NOT_SUPPORTED` | Pay Scenario Token Not Supported |
| 9004 | `PAY_SCENARIO_DUPLICATED` | Pay Product Duplicated |
| 9005 | `PAY_SUB_ID_GET_ERROR` | Get Pay Sub Id Error |
| 9006 | `PAY_CHARGE_BIND_INFO_ERROR` | Pay Charge Bind Info Error |
| 9007 | `PAY_UPLOAD_HASH_EXIST` | The Hash You Uploaded Is Already Existed |
| 10001 | `USER_ALREADY_SIGNED` | User is Signed Already |
| 20001 | `CHARGE_POINTS_PRODUCT_NOT_EXIST` | Charge Product Not Exist |
| 20002 | `CONFIRM_CHARGE_POINTS_ERROR` | Confirm Charge Points Error |
| 20003 | `ADD_POINTS_ACTIVITY_LOG_ERROR` | Add Points Charge Log Error |
| 20004 | `POINTS_EXCHANGE_BALANCE_NOT_ENOUGH_ERROR` | User's Points Not Enough |
| 20005 | `POINTS_EXCHANGE_SCENARIO_NOT_EXIST_ERROR` | Points Exchange Scenario Not Exist |
| 20006 | `POINTS_EXCHANGE_TIMES_LIMITED` | Points Activity Times Limited |
| 20007 | `POINTS_SHARE_COUNT_LIMITED` | Points share count limited |
| 20008 | `POINTS_EXCHANGE_TO_5_OR_3_DAYS_VIP_TIME_LIMITED` | Redeem points for a 3-day or 5-day membership up to 5 times per day |
| 20009 | `VERIFICATION_FAILED` | Verification Failed |
| 20010 | `DUPLICATED_BINDING` | Duplicated Binding |
| 99999 | `SERVICE_UPDATING` | Service Updating |
| 1201 | `UPLOAD_FAIL` | Upload fail |
| 1202 | `BASE64_FORMAT_ERROR` | Base64 decode fail |
| 1203 | `DATA_NOT_FOUND` | Data not found |

## 模块

| 模块 | 接口数 | 文档 |
| --- | --- | --- |
| 用户与账号 | 20 | [01-user.md](01-user.md) |
| 对话与助手 | 33 | [02-chat.md](02-chat.md) |
| 支付 | 5 | [03-pay.md](03-pay.md) |
| 区域访问 | 3 | [04-region.md](04-region.md) |
| 行情与预测 | 13 | [05-market.md](05-market.md) |
| 兑换 Swap | 17 | [06-swap.md](06-swap.md) |
| NFT | 4 | [07-nft.md](07-nft.md) |
| 快讯与新闻 | 32 | [08-news.md](08-news.md) |
| AI 热点 | 9 | [09-aihot.md](09-aihot.md) |
| 公众号 | 8 | [10-gzh.md](10-gzh.md) |
| KOL 与推文 | 16 | [11-kol.md](11-kol.md) |
| 数据看板 | 31 | [12-dashboard.md](12-dashboard.md) |
| AI 账户与钱包 | 26 | [13-wallet.md](13-wallet.md) |
| 积分 | 15 | [14-points.md](14-points.md) |
| 研报 | 12 | [15-report.md](15-report.md) |
| AI 榜单 | 10 | [16-ranking.md](16-ranking.md) |
| 分享图与 PDF | 23 | [17-share.md](17-share.md) |
| GPT Action | 14 | [18-gptaction.md](18-gptaction.md) |
| 应用配置 | 8 | [19-app.md](19-app.md) |

## 路由表里没按字面挂上的条目

写在 ml4gp 里、但当前进程不会按这一条提供。原因里写了「路径仍然可用」的，以模块文档中同路径的那条为准。

| 方法 | 路径 | 原因 |
| --- | --- | --- |
| GET | `/v3/api/news/comment/list` | plugin_router_v3_mapping 未在 GenAI routers.py 注册，当前进程不会挂载 |
| POST | `/v3/api/news/comment/add` | plugin_router_v3_mapping 未在 GenAI routers.py 注册，当前进程不会挂载 |

## 静态资源

`app.static('/static', STATIC_PATH)`，免登录。隐私页路径在免登录名单里：`/static/privacy.html`、`/static/privacy/MLprivacyAgreement_zh.html`、`/static/privacy/MLprivacyAgreement_en.html`、`/static/twitter.html`。

## 字段说明

Query / Body 表来自控制器对 `request.args` / `request.json` / `request.form` 的读取：

- `.get`：代码用了默认值就写默认值；写「无」表示 `.get(key)` 没给默认值，缺失时是 `None`
- 「下标，缺失会抛错」：代码用 `obj["key"]`，缺字段会异常
- 字段放在 Query 还是 Body，以详情里的小标题为准。有的 POST 只读 query string（例如 `userRate`）

静态提取看不到「只在下游服务里拆的字段」。这类接口会注明整包 JSON。写用例时以详情表为准，缺字段再对照实现文件行号。
