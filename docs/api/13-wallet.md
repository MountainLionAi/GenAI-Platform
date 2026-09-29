# AI 账户与钱包

本模块 26 个已挂载接口。通用约定见 [README](README.md)。

## 索引

| 方法 | 路径 | 鉴权 |
| --- | --- | --- |
| POST | [`/v2/api/user/modifyProfile`](#post-v2-api-user-modifyprofile-1) | 需要 x-api-key，需登录 |
| GET | [`/v2/api/wallet/address/qrcode`](#get-v2-api-wallet-address-qrcode-2) | 需要 x-api-key，免登录 |
| GET | [`/v2/api/getTrustWalletInfo`](#get-v2-api-gettrustwalletinfo-3) | 需要 x-api-key，免登录 |
| GET | [`/v2/api/getCustomerServiceInfo`](#get-v2-api-getcustomerserviceinfo-4) | 需要 x-api-key，免登录 |
| GET | [`/v2/api/bscHashCheck`](#get-v2-api-bschashcheck-5) | 需要 x-api-key，免登录 |
| GET | [`/v2/api/answerForTW`](#get-v2-api-answerfortw-6) | 需要 x-api-key，免登录 |
| GET | [`/v2/api/getAIAccountInfo`](#get-v2-api-getaiaccountinfo-7) | 需要 x-api-key，需登录 |
| GET | [`/v2/api/pay/getSupportedCoinList`](#get-v2-api-pay-getsupportedcoinlist-8) | 需要 x-api-key，v2 免登录；v1 需登录 |
| GET | [`/v2/api/pay/getCoinsUsdt`](#get-v2-api-pay-getcoinsusdt-9) | 需要 x-api-key，需登录 |
| GET | [`/v2/api/getCustomerServiceList`](#get-v2-api-getcustomerservicelist-10) | 需要 x-api-key，免登录 |
| POST | [`/v2/api/chargeCallback`](#post-v2-api-chargecallback-11) | 需要 x-api-key，免登录 |
| POST | [`/v2/api/aiAccountSwap`](#post-v2-api-aiaccountswap-12) | 需要 x-api-key，需登录 |
| POST | [`/v2/api/aiAccountLimitSwap`](#post-v2-api-aiaccountlimitswap-13) | 需要 x-api-key，需登录 |
| POST | [`/v2/api/getWithdrawInfo`](#post-v2-api-getwithdrawinfo-14) | 需要 x-api-key，需登录 |
| POST | [`/v2/api/aiAccountPreWithdraw`](#post-v2-api-aiaccountprewithdraw-15) | 需要 x-api-key，需登录 |
| POST | [`/v2/api/aiAccountWithdraw`](#post-v2-api-aiaccountwithdraw-16) | 需要 x-api-key，需登录 |
| POST | [`/v2/api/getSwapOrders`](#post-v2-api-getswaporders-17) | 需要 x-api-key，v2 免登录；v1 需登录 |
| POST | [`/v2/api/cancelLimitOrder`](#post-v2-api-cancellimitorder-18) | 需要 x-api-key，需登录 |
| POST | [`/v2/api/getOrderStatus`](#post-v2-api-getorderstatus-19) | 需要 x-api-key，需登录 |
| POST | [`/v2/api/pay/getUserDepositQrCode`](#post-v2-api-pay-getuserdepositqrcode-20) | 需要 x-api-key，需登录 |
| POST | [`/v2/api/pay/getDepositQrCode`](#post-v2-api-pay-getdepositqrcode-21) | 需要 x-api-key，需登录 |
| POST | [`/v2/api/pay/confirmPayScenario`](#post-v2-api-pay-confirmpayscenario-22) | 需要 x-api-key，需登录 |
| POST | [`/v2/api/pay/getPaidInfo`](#post-v2-api-pay-getpaidinfo-23) | 需要 x-api-key，免登录 |
| POST | [`/v2/api/address/analysis/history/add`](#post-v2-api-address-analysis-history-add-24) | 需要 x-api-key，需登录 |
| GET | [`/v2/api/address/analysis/history/query`](#get-v2-api-address-analysis-history-query-25) | 需要 x-api-key，v2 免登录；v1 需登录 |
| GET | [`/v2/api/getBlackAddress`](#get-v2-api-getblackaddress-26) | 需要 x-api-key，v2 需登录；v1 免登录 |

## 详情

### POST `/v2/api/user/modifyProfile`

<a id="post-v2-api-user-modifyprofile-1"></a>

- 路由键：`modifyUserProfile`
- 鉴权：需要 x-api-key，需登录
- v1 镜像：`POST /v1/api/user/modifyProfile`（同一 handler；v1 不校验 `x-api-key`）
- 实现：`ml4gp/ml4gp/controller/ai_account.py:234` `ml4gp.controller.ai_account.modify_profile`
- 响应：JSON 信封 `{code,message,status,data}`
- 显式错误码：`MODIFY_USER_PROFILE_ERROR`, `USER_NOT_EXIST`

**JSON Body**

| 字段 | 读取方式 | 默认值 |
| --- | --- | --- |
| `userName` | `.get` | `` |
| `image` | `.get` | `` |

### GET `/v2/api/wallet/address/qrcode`

<a id="get-v2-api-wallet-address-qrcode-2"></a>

- 路由键：`address2qrCode`
- 鉴权：需要 x-api-key，免登录
- v1 镜像：`GET /v1/api/wallet/address/qrcode`（同一 handler；v1 不校验 `x-api-key`）
- 实现：`ml4gp/ml4gp/controller/qrcode.py:8` `ml4gp.controller.qrcode.generate_qrcode_4_wallet_address`
- 响应：JSON 信封 `{code,message,status,data}`

**Query**

| 字段 | 读取方式 | 默认值 |
| --- | --- | --- |
| `address` | `.get` | `null` |

### GET `/v2/api/getTrustWalletInfo`

<a id="get-v2-api-gettrustwalletinfo-3"></a>

- 路由键：`getTrustWalletInfo`
- 鉴权：需要 x-api-key，免登录
- v1 镜像：`GET /v1/api/getTrustWalletInfo`（同一 handler；v1 不校验 `x-api-key`）
- 实现：`ml4gp/ml4gp/controller/trust_wallet_customer.py:22` `ml4gp.controller.trust_wallet_customer.prepare_customer_service_data`
- 响应：JSON 信封 `{code,message,status,data}`

**Query**

| 字段 | 读取方式 | 默认值 |
| --- | --- | --- |
| `language` | `.get` | `en` |
| `type` | `.get` | `` |

### GET `/v2/api/getCustomerServiceInfo`

<a id="get-v2-api-getcustomerserviceinfo-4"></a>

- 路由键：`getCustomerServiceInfo`
- 鉴权：需要 x-api-key，免登录
- v1 镜像：`GET /v1/api/getCustomerServiceInfo`（同一 handler；v1 不校验 `x-api-key`）
- 实现：`ml4gp/ml4gp/controller/trust_wallet_customer.py:131` `ml4gp.controller.trust_wallet_customer.get_customer_service_data`
- 响应：JSON 信封 `{code,message,status,data}`

**Query**

| 字段 | 读取方式 | 默认值 |
| --- | --- | --- |
| `language` | `.get` | `en` |
| `type` | `.get` | `` |

### GET `/v2/api/bscHashCheck`

<a id="get-v2-api-bschashcheck-5"></a>

- 路由键：`getBscChainHash`
- 鉴权：需要 x-api-key，免登录
- v1 镜像：`GET /v1/api/bscHashCheck`（同一 handler；v1 不校验 `x-api-key`）
- 实现：`ml4gp/ml4gp/controller/trust_wallet_customer.py:272` `ml4gp.controller.trust_wallet_customer.check_hash_status`
- 响应：JSON 信封 `{code,message,status,data}`

**Query**

| 字段 | 读取方式 | 默认值 |
| --- | --- | --- |
| `hash` | `.get` | `` |

### GET `/v2/api/answerForTW`

<a id="get-v2-api-answerfortw-6"></a>

- 路由键：`answerForTW`
- 鉴权：需要 x-api-key，免登录
- v1 镜像：`GET /v1/api/answerForTW`（同一 handler；v1 不校验 `x-api-key`）
- 实现：`ml4gp/ml4gp/controller/trust_wallet_customer.py:240` `ml4gp.controller.trust_wallet_customer.answer_trust_wallet`
- 响应：JSON 信封 `{code,message,status,data}`

**Query**

| 字段 | 读取方式 | 默认值 |
| --- | --- | --- |
| `type` | `.get` | `` |
| `language` | `.get` | `en` |
| `step` | `.get` | 无 |
| `msg` | `.get` | 无 |

### GET `/v2/api/getAIAccountInfo`

<a id="get-v2-api-getaiaccountinfo-7"></a>

- 路由键：`getAIAccountInfo`
- 鉴权：需要 x-api-key，需登录
- v1 镜像：`GET /v1/api/getAIAccountInfo`（同一 handler；v1 不校验 `x-api-key`）
- 实现：`ml4gp/ml4gp/controller/ai_account.py:12` `ml4gp.controller.ai_account.get_ai_account_info`
- 响应：JSON 信封 `{code,message,status,data}`

无额外 query/body 字段（或参数在更下游动态拼装）。

### GET `/v2/api/pay/getSupportedCoinList`

<a id="get-v2-api-pay-getsupportedcoinlist-8"></a>

- 路由键：`getSupportedCoinList`
- 鉴权：需要 x-api-key，v2 免登录；v1 需登录
- v1 镜像：`GET /v1/api/pay/getSupportedCoinList`（同一 handler；v1 不校验 `x-api-key`）
- 实现：`ml4gp/ml4gp/controller/ai_account.py:224` `ml4gp.controller.ai_account.get_supported_coin_list`
- 响应：JSON 信封 `{code,message,status,data}`

无额外 query/body 字段（或参数在更下游动态拼装）。

### GET `/v2/api/pay/getCoinsUsdt`

<a id="get-v2-api-pay-getcoinsusdt-9"></a>

- 路由键：`getCoinsUsdt`
- 鉴权：需要 x-api-key，需登录
- v1 镜像：`GET /v1/api/pay/getCoinsUsdt`（同一 handler；v1 不校验 `x-api-key`）
- 实现：`ml4gp/ml4gp/controller/ai_account.py:228` `ml4gp.controller.ai_account.get_coins_usdt`
- 响应：JSON 信封 `{code,message,status,data}`

无额外 query/body 字段（或参数在更下游动态拼装）。

### GET `/v2/api/getCustomerServiceList`

<a id="get-v2-api-getcustomerservicelist-10"></a>

- 路由键：`getCustomerServiceList`
- 鉴权：需要 x-api-key，免登录
- v1 镜像：`GET /v1/api/getCustomerServiceList`（同一 handler；v1 不校验 `x-api-key`）
- 实现：`ml4gp/ml4gp/controller/trust_wallet_customer.py:16` `ml4gp.controller.trust_wallet_customer.get_customer_list`
- 响应：JSON 信封 `{code,message,status,data}`

无额外 query/body 字段（或参数在更下游动态拼装）。

### POST `/v2/api/chargeCallback`

<a id="post-v2-api-chargecallback-11"></a>

- 路由键：`chargeCallback`
- 鉴权：需要 x-api-key，免登录
- v1 镜像：`POST /v1/api/chargeCallback`（同一 handler；v1 不校验 `x-api-key`）
- 实现：`ml4gp/ml4gp/controller/ai_account.py:19` `ml4gp.controller.ai_account.charge_callback`
- 响应：JSON 信封 `{code,message,status,data}`
- 显式错误码：`PARAMS_ERROR`

**JSON Body**

| 字段 | 读取方式 | 默认值 |
| --- | --- | --- |
| `userSubId` | `.get` | `` |
| `coinCode` | `.get` | `` |
| `amount` | `.get` | `` |
| `address` | `.get` | `` |
| `hash` | `.get` | `` |
| `userNo` | `.get` | `` |

### POST `/v2/api/aiAccountSwap`

<a id="post-v2-api-aiaccountswap-12"></a>

- 路由键：`aiAccountSwap`
- 鉴权：需要 x-api-key，需登录
- v1 镜像：`POST /v1/api/aiAccountSwap`（同一 handler；v1 不校验 `x-api-key`）
- 实现：`ml4gp/ml4gp/controller/ai_account.py:42` `ml4gp.controller.ai_account.ai_account_swap`
- 响应：JSON 信封 `{code,message,status,data}`
- 显式错误码：`PARAMS_ERROR`

**JSON Body**

| 字段 | 读取方式 | 默认值 |
| --- | --- | --- |
| `quoteInfo` | `.get` | `{}` |

### POST `/v2/api/aiAccountLimitSwap`

<a id="post-v2-api-aiaccountlimitswap-13"></a>

- 路由键：`aiAccountLimitSwap`
- 鉴权：需要 x-api-key，需登录
- v1 镜像：`POST /v1/api/aiAccountLimitSwap`（同一 handler；v1 不校验 `x-api-key`）
- 实现：`ml4gp/ml4gp/controller/ai_account.py:55` `ml4gp.controller.ai_account.ai_account_limit_swap`
- 响应：JSON 信封 `{code,message,status,data}`
- 显式错误码：`PARAMS_ERROR`

**JSON Body**

| 字段 | 读取方式 | 默认值 |
| --- | --- | --- |
| `quoteInfo` | `.get` | `{}` |

### POST `/v2/api/getWithdrawInfo`

<a id="post-v2-api-getwithdrawinfo-14"></a>

- 路由键：`getWithdrawInfo`
- 鉴权：需要 x-api-key，需登录
- v1 镜像：`POST /v1/api/getWithdrawInfo`（同一 handler；v1 不校验 `x-api-key`）
- 实现：`ml4gp/ml4gp/controller/ai_account.py:152` `ml4gp.controller.ai_account.get_withdraw_info`
- 响应：JSON 信封 `{code,message,status,data}`
- 显式错误码：`PARAMS_ERROR`

**JSON Body**

| 字段 | 读取方式 | 默认值 |
| --- | --- | --- |
| `coinCode` | `.get` | `` |

### POST `/v2/api/aiAccountPreWithdraw`

<a id="post-v2-api-aiaccountprewithdraw-15"></a>

- 路由键：`aiAccountPreWithdraw`
- 鉴权：需要 x-api-key，需登录
- v1 镜像：`POST /v1/api/aiAccountPreWithdraw`（同一 handler；v1 不校验 `x-api-key`）
- 实现：`ml4gp/ml4gp/controller/ai_account.py:130` `ml4gp.controller.ai_account.ai_account_pre_withdraw`
- 响应：JSON 信封 `{code,message,status,data}`
- 显式错误码：`PARAMS_ERROR`

**JSON Body**

| 字段 | 读取方式 | 默认值 |
| --- | --- | --- |
| `coinCode` | `.get` | `` |
| `mainNetwork` | `.get` | `` |
| `targetAddress` | `.get` | `` |
| `chargingAmt` | `.get` | `` |
| `remark` | `.get` | `` |
| `language` | `.get` | `en` |

### POST `/v2/api/aiAccountWithdraw`

<a id="post-v2-api-aiaccountwithdraw-16"></a>

- 路由键：`aiAccountWithdraw`
- 鉴权：需要 x-api-key，需登录
- v1 镜像：`POST /v1/api/aiAccountWithdraw`（同一 handler；v1 不校验 `x-api-key`）
- 实现：`ml4gp/ml4gp/controller/ai_account.py:94` `ml4gp.controller.ai_account.ai_account_withdraw`
- 响应：JSON 信封 `{code,message,status,data}`
- 显式错误码：`PARAMS_ERROR`

**JSON Body**

| 字段 | 读取方式 | 默认值 |
| --- | --- | --- |
| `emailCode` | `.get` | `` |
| `withdrawKey` | `.get` | `` |

### POST `/v2/api/getSwapOrders`

<a id="post-v2-api-getswaporders-17"></a>

- 路由键：`getSwapOrders`
- 鉴权：需要 x-api-key，v2 免登录；v1 需登录
- v1 镜像：`POST /v1/api/getSwapOrders`（同一 handler；v1 不校验 `x-api-key`）
- 实现：`ml4gp/ml4gp/controller/ai_account.py:108` `ml4gp.controller.ai_account.get_swap_records`
- 响应：JSON 信封 `{code,message,status,data}`
- 显式错误码：`NOT_AUTHORIZED`, `PARAMS_ERROR`, `WALLET_ADDRESS_IS_EMPTY`

**JSON Body**

| 字段 | 读取方式 | 默认值 |
| --- | --- | --- |
| `walletType` | `.get` | `WEB3` |
| `walletAddress` | `.get` | `` |
| `pageSize` | `.get` | `50` |
| `page` | `.get` | `1` |

### POST `/v2/api/cancelLimitOrder`

<a id="post-v2-api-cancellimitorder-18"></a>

- 路由键：`cancelLimitOrder`
- 鉴权：需要 x-api-key，需登录
- v1 镜像：`POST /v1/api/cancelLimitOrder`（同一 handler；v1 不校验 `x-api-key`）
- 实现：`ml4gp/ml4gp/controller/ai_account.py:68` `ml4gp.controller.ai_account.cancel_limit_order`
- 响应：JSON 信封 `{code,message,status,data}`
- 显式错误码：`PARAMS_ERROR`

**JSON Body**

| 字段 | 读取方式 | 默认值 |
| --- | --- | --- |
| `orderId` | `.get` | 无 |

### POST `/v2/api/getOrderStatus`

<a id="post-v2-api-getorderstatus-19"></a>

- 路由键：`getOrderStatus`
- 鉴权：需要 x-api-key，需登录
- v1 镜像：`POST /v1/api/getOrderStatus`（同一 handler；v1 不校验 `x-api-key`）
- 实现：`ml4gp/ml4gp/controller/ai_account.py:81` `ml4gp.controller.ai_account.get_order_status`
- 响应：JSON 信封 `{code,message,status,data}`
- 显式错误码：`PARAMS_ERROR`

**JSON Body**

| 字段 | 读取方式 | 默认值 |
| --- | --- | --- |
| `orderId` | `.get` | 无 |

### POST `/v2/api/pay/getUserDepositQrCode`

<a id="post-v2-api-pay-getuserdepositqrcode-20"></a>

- 路由键：`userDepositQrCode`
- 鉴权：需要 x-api-key，需登录
- v1 镜像：`POST /v1/api/pay/getUserDepositQrCode`（同一 handler；v1 不校验 `x-api-key`）
- 实现：`ml4gp/ml4gp/controller/ai_account.py:166` `ml4gp.controller.ai_account.get_deposit_qr_code`
- 响应：JSON 信封 `{code,message,status,data}`
- 显式错误码：`PARAMS_ERROR`, `TOKEN_NOT_SUPPORTED`

**JSON Body**

| 字段 | 读取方式 | 默认值 |
| --- | --- | --- |
| `coinCode` | `.get` | `` |

### POST `/v2/api/pay/getDepositQrCode`

<a id="post-v2-api-pay-getdepositqrcode-21"></a>

- 路由键：`depositQrCode`
- 鉴权：需要 x-api-key，需登录
- v1 镜像：`POST /v1/api/pay/getDepositQrCode`（同一 handler；v1 不校验 `x-api-key`）
- 实现：`ml4gp/ml4gp/controller/ai_account.py:179` `ml4gp.controller.ai_account.get_deposit_qr_code_new`
- 响应：JSON 信封 `{code,message,status,data}`
- 显式错误码：`PARAMS_ERROR`

**JSON Body**

| 字段 | 读取方式 | 默认值 |
| --- | --- | --- |
| `coinCode` | `.get` | `` |
| `productType` | `.get` | `` |
| `productId` | `.get` | `` |
| `fixedSource` | `.get` | `` |

### POST `/v2/api/pay/confirmPayScenario`

<a id="post-v2-api-pay-confirmpayscenario-22"></a>

- 路由键：`confirmPayScenario`
- 鉴权：需要 x-api-key，需登录
- v1 镜像：`POST /v1/api/pay/confirmPayScenario`（同一 handler；v1 不校验 `x-api-key`）
- 实现：`ml4gp/ml4gp/controller/ai_account.py:192` `ml4gp.controller.ai_account.confirm_pay_scenario`
- 响应：JSON 信封 `{code,message,status,data}`
- 显式错误码：`PARAMS_ERROR`

**JSON Body**

| 字段 | 读取方式 | 默认值 |
| --- | --- | --- |
| `msggroup` | `.get` | `` |
| `msgid` | `.get` | `` |
| `scenario` | `.get` | `` |
| `coinCode` | `.get` | `` |
| `productId` | `.get` | `` |

### POST `/v2/api/pay/getPaidInfo`

<a id="post-v2-api-pay-getpaidinfo-23"></a>

- 路由键：`getPaidInfo`
- 鉴权：需要 x-api-key，免登录
- v1 镜像：`POST /v1/api/pay/getPaidInfo`（同一 handler；v1 不校验 `x-api-key`）
- 实现：`ml4gp/ml4gp/controller/ai_account.py:207` `ml4gp.controller.ai_account.get_paid_info`
- 响应：JSON 信封 `{code,message,status,data}`
- 显式错误码：`PARAMS_ERROR`

**JSON Body**

| 字段 | 读取方式 | 默认值 |
| --- | --- | --- |
| `msggroup` | `.get` | `` |
| `msgid` | `.get` | `` |
| `scenario` | `.get` | `` |
| `source` | `.get` | `` |
| `status` | `.get` | `false` |
| `visitor_id` | `.get` | `` |

### POST `/v2/api/address/analysis/history/add`

<a id="post-v2-api-address-analysis-history-add-24"></a>

- 路由键：`addAddressAnalysisHistory`
- 鉴权：需要 x-api-key，需登录
- v1 镜像：`POST /v1/api/address/analysis/history/add`（同一 handler；v1 不校验 `x-api-key`）
- 实现：`ml4gp/ml4gp/controller/address_analysis.py:10` `ml4gp.controller.address_analysis.add_history`
- 响应：JSON 信封 `{code,message,status,data}`

**JSON Body**

| 字段 | 读取方式 | 默认值 |
| --- | --- | --- |
| `address` | `.get` | 无 |

### GET `/v2/api/address/analysis/history/query`

<a id="get-v2-api-address-analysis-history-query-25"></a>

- 路由键：`queryAddressAnalysisHistory`
- 鉴权：需要 x-api-key，v2 免登录；v1 需登录
- v1 镜像：`GET /v1/api/address/analysis/history/query`（同一 handler；v1 不校验 `x-api-key`）
- 实现：`ml4gp/ml4gp/controller/address_analysis.py:19` `ml4gp.controller.address_analysis.query_history`
- 响应：JSON 信封 `{code,message,status,data}`

**Query**

| 字段 | 读取方式 | 默认值 |
| --- | --- | --- |
| `num` | `.get` | `9` |

### GET `/v2/api/getBlackAddress`

<a id="get-v2-api-getblackaddress-26"></a>

- 路由键：`getBlackAddress`
- 鉴权：需要 x-api-key，v2 需登录；v1 免登录
- v1 镜像：`GET /v1/api/getBlackAddress`（同一 handler；v1 不校验 `x-api-key`）
- 实现：`ml4gp/ml4gp/controller/black_address.py:10` `ml4gp.controller.black_address.get_black_address`
- 响应：JSON 信封 `{code,message,status,data}`

**Query**

| 字段 | 读取方式 | 默认值 |
| --- | --- | --- |
| `coin` | `.get` | `` |
| `address` | `.get` | `` |
