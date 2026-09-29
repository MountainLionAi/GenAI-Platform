# 对话与助手

本模块 33 个已挂载接口。通用约定见 [README](README.md)。

## 索引

| 方法 | 路径 | 鉴权 |
| --- | --- | --- |
| GET | [`/v2/api/getAIAgents`](#get-v2-api-getaiagents-1) | 需要 x-api-key，免登录 |
| GET | [`/v2/api/getSwapAgentQuestion`](#get-v2-api-getswapagentquestion-2) | 需要 x-api-key，免登录 |
| GET | [`/v2/api/getNftAgentQuestion`](#get-v2-api-getnftagentquestion-3) | 需要 x-api-key，免登录 |
| POST | [`/v2/api/deepInsight`](#post-v2-api-deepinsight-4) | 需要 x-api-key，免登录 |
| POST | [`/v2/api/deepinsightswftgpt`](#post-v2-api-deepinsightswftgpt-5) | 需要 x-api-key，免登录 |
| POST | [`/v2/api/deepinsightForTW`](#post-v2-api-deepinsightfortw-6) | 需要 x-api-key，v2 免登录；v1 需登录 |
| POST | [`/v2/api/deepInsightForTT`](#post-v2-api-deepinsightfortt-7) | 需要 x-api-key，免登录 |
| POST | [`/v2/api/textToImage`](#post-v2-api-texttoimage-8) | 需要 x-api-key，免登录 |
| POST | [`/v2/api/companyResearch`](#post-v2-api-companyresearch-9) | 需要 x-api-key，免登录 |
| GET | [`/v2/api/instruction/polish`](#get-v2-api-instruction-polish-10) | 需要 x-api-key，免登录 |
| POST | [`/v2/api/external/chatCompletions`](#post-v2-api-external-chatcompletions-11) | 需要 x-api-key，v2 免登录；v1 需登录 |
| POST | [`/v2/api/tw/chatCompletions`](#post-v2-api-tw-chatcompletions-12) | 需要 x-api-key，v2 免登录；v1 需登录 |
| POST | [`/v2/api/tw/delMsgGroupList`](#post-v2-api-tw-delmsggrouplist-13) | 需要 x-api-key，v2 免登录；v1 需登录 |
| POST | [`/v2/api/tw/msggroup/generate`](#post-v2-api-tw-msggroup-generate-14) | 需要 x-api-key，v2 免登录；v1 需登录 |
| POST | [`/v2/api/getMindMap`](#post-v2-api-getmindmap-15) | 需要 x-api-key，免登录 |
| GET | [`/v2/api/llm/model/list`](#get-v2-api-llm-model-list-16) | 需要 x-api-key，v2 免登录；v1 需登录 |
| POST | [`/v2/api/auto/ui/swap`](#post-v2-api-auto-ui-swap-17) | 需要 x-api-key，需登录 |
| GET | [`/v2/api/cryptoBeauty/questions`](#get-v2-api-cryptobeauty-questions-18) | 需要 x-api-key，v2 免登录；v1 需登录 |
| GET | [`/v2/api/cryptoBeauty/getAnlayzer`](#get-v2-api-cryptobeauty-getanlayzer-19) | 需要 x-api-key，免登录 |
| POST | [`/mpcbot/sendchat_gpt4`](#post-mpcbot-sendchat-gpt4-20) | 免 x-api-key，需登录 |
| POST | [`/v2/api/messages/add`](#post-v2-api-messages-add-21) | 需要 x-api-key，需登录 |
| GET | [`/v2/api/getMessageList`](#get-v2-api-getmessagelist-22) | 需要 x-api-key，免登录 |
| GET | [`/v2/api/getMsgGroupList`](#get-v2-api-getmsggrouplist-23) | 需要 x-api-key，免登录 |
| POST | [`/v2/api/delMsgGroupList`](#post-v2-api-delmsggrouplist-24) | 需要 x-api-key，需登录 |
| POST | [`/v2/api/sendStreamChat`](#post-v2-api-sendstreamchat-25) | 需要 x-api-key，免登录 |
| POST | [`/v2/api/sendStylizedRequest`](#post-v2-api-sendstylizedrequest-26) | 需要 x-api-key，免登录 |
| POST | [`/v2/api/userRate`](#post-v2-api-userrate-27) | 需要 x-api-key，需登录 |
| POST | [`/v2/api/delMessages`](#post-v2-api-delmessages-28) | 需要 x-api-key，需登录 |
| POST | [`/v2/api/shareMessages`](#post-v2-api-sharemessages-29) | 需要 x-api-key，免登录 |
| POST | [`/v2/api/getShareMessages`](#post-v2-api-getsharemessages-30) | 需要 x-api-key，免登录 |
| POST | [`/v2/api/tw/feedback`](#post-v2-api-tw-feedback-31) | 需要 x-api-key，免登录 |
| POST | [`/v2/api/assistantChat`](#post-v2-api-assistantchat-32) | 需要 x-api-key，免登录 |
| POST | [`/v2/api/getAssistantHistory`](#post-v2-api-getassistanthistory-33) | 需要 x-api-key，免登录 |

## 详情

### GET `/v2/api/getAIAgents`

<a id="get-v2-api-getaiagents-1"></a>

- 路由键：`getAIAgents`
- 鉴权：需要 x-api-key，免登录
- v1 镜像：`GET /v1/api/getAIAgents`（同一 handler；v1 不校验 `x-api-key`）
- 实现：`ml4gp/ml4gp/controller/ai_agent.py:11` `ml4gp.controller.ai_agent.get_ai_agents`
- 响应：JSON 信封 `{code,message,status,data}`
- 显式错误码：`PARAMS_ERROR`

**Query**

| 字段 | 读取方式 | 默认值 |
| --- | --- | --- |
| `language` | `.get` | `en` |
| `tag` | `.get` | `0` |
| `name` | `.get` | `` |
| `userid` | `.get` | `` |

### GET `/v2/api/getSwapAgentQuestion`

<a id="get-v2-api-getswapagentquestion-2"></a>

- 路由键：`getSwapAgentQuestion`
- 鉴权：需要 x-api-key，免登录
- v1 镜像：`GET /v1/api/getSwapAgentQuestion`（同一 handler；v1 不校验 `x-api-key`）
- 实现：`ml4gp/ml4gp/controller/ai_agent.py:24` `ml4gp.controller.ai_agent.get_swap_agent_question`
- 响应：JSON 信封 `{code,message,status,data}`

**Query**

| 字段 | 读取方式 | 默认值 |
| --- | --- | --- |
| `language` | `.get` | `en` |

### GET `/v2/api/getNftAgentQuestion`

<a id="get-v2-api-getnftagentquestion-3"></a>

- 路由键：`getNftAgentQuestion`
- 鉴权：需要 x-api-key，免登录
- v1 镜像：`GET /v1/api/getNftAgentQuestion`（同一 handler；v1 不校验 `x-api-key`）
- 实现：`ml4gp/ml4gp/controller/ai_agent.py:38` `ml4gp.controller.ai_agent.get_nft_agent_question`
- 响应：JSON 信封 `{code,message,status,data}`

**Query**

| 字段 | 读取方式 | 默认值 |
| --- | --- | --- |
| `language` | `.get` | `en` |

### POST `/v2/api/deepInsight`

<a id="post-v2-api-deepinsight-4"></a>

- 路由键：`deepInsight`
- 鉴权：需要 x-api-key，免登录
- v1 镜像：`POST /v1/api/deepInsight`（同一 handler；v1 不校验 `x-api-key`）
- 实现：`ml4gp/ml4gp/controller/deep_insight.py:42` `ml4gp.controller.deep_insight.deep_insight`
- 响应：流式（SSE / chunk）
- 显式错误码：`NOT_AUTHORIZED`

**JSON Body**

| 字段 | 读取方式 | 默认值 |
| --- | --- | --- |
| `news` | `.get` | 无 |
| `analysis` | `.get` | `` |
| `msggroup` | `.get` | `` |
| `language` | `.get` | `cn` |
| `code` | `.get` | `` |
| `from_ethf` | `.get` | `0` |
| `owner` | `.get` | `0` |
| `regenerate_response` | `.get` | `null` |
| `image_url` | `.get` | `null` |

### POST `/v2/api/deepinsightswftgpt`

<a id="post-v2-api-deepinsightswftgpt-5"></a>

- 路由键：`deepinsightswftgpt`
- 鉴权：需要 x-api-key，免登录
- v1 镜像：`POST /v1/api/deepinsightswftgpt`（同一 handler；v1 不校验 `x-api-key`）
- 实现：`ml4gp/ml4gp/controller/deep_insight.py:99` `ml4gp.controller.deep_insight.deep_insight_swftgpt`
- 响应：流式（SSE / chunk）
- 显式错误码：`NOT_AUTHORIZED`

**JSON Body**

| 字段 | 读取方式 | 默认值 |
| --- | --- | --- |
| `news` | `.get` | 无 |
| `analysis` | `.get` | `` |
| `msggroup` | `.get` | `` |
| `language` | `.get` | `cn` |
| `code` | `.get` | `` |
| `regenerate_response` | `.get` | `null` |

### POST `/v2/api/deepinsightForTW`

<a id="post-v2-api-deepinsightfortw-6"></a>

- 路由键：`deepinsighttw`
- 鉴权：需要 x-api-key，v2 免登录；v1 需登录
- v1 镜像：`POST /v1/api/deepinsightForTW`（同一 handler；v1 不校验 `x-api-key`）
- 实现：`ml4gp/ml4gp/controller/deep_insight.py:150` `ml4gp.controller.deep_insight.deep_insight_tw`
- 响应：流式（SSE / chunk）

**JSON Body**

| 字段 | 读取方式 | 默认值 |
| --- | --- | --- |
| `news` | `.get` | 无 |
| `analysis` | `.get` | `` |
| `msggroup` | `.get` | `` |
| `language` | `.get` | `cn` |
| `code` | `.get` | `` |
| `regenerate_response` | `.get` | `null` |

### POST `/v2/api/deepInsightForTT`

<a id="post-v2-api-deepinsightfortt-7"></a>

- 路由键：`deepinsighttt`
- 鉴权：需要 x-api-key，免登录
- v1 镜像：`POST /v1/api/deepInsightForTT`（同一 handler；v1 不校验 `x-api-key`）
- 实现：`ml4gp/ml4gp/controller/deep_insight.py:197` `ml4gp.controller.deep_insight.deep_insight_token_talk`
- 响应：JSON 信封 `{code,message,status,data}`

**JSON Body**

| 字段 | 读取方式 | 默认值 |
| --- | --- | --- |
| `news` | `.get` | 无 |
| `language` | `.get` | `cn` |

### POST `/v2/api/textToImage`

<a id="post-v2-api-texttoimage-8"></a>

- 路由键：`textToImage`
- 鉴权：需要 x-api-key，免登录
- v1 镜像：`POST /v1/api/textToImage`（同一 handler；v1 不校验 `x-api-key`）
- 实现：`ml4gp/ml4gp/controller/deep_insight.py:718` `ml4gp.controller.deep_insight.text_to_image`
- 响应：JSON 信封 `{code,message,status,data}`

**JSON Body**

| 字段 | 读取方式 | 默认值 |
| --- | --- | --- |
| `user_input` | `.get` | 无 |
| `msggroup` | `.get` | `` |
| `language` | `.get` | `cn` |
| `code` | `.get` | `` |
| `regenerate_response` | `.get` | `null` |

### POST `/v2/api/companyResearch`

<a id="post-v2-api-companyresearch-9"></a>

Async endpoint for company research with improved error handling and type hints.

- 路由键：`companyResearch`
- 鉴权：需要 x-api-key，免登录
- v1 镜像：`POST /v1/api/companyResearch`（同一 handler；v1 不校验 `x-api-key`）
- 实现：`ml4gp/ml4gp/controller/company_reasearch.py:32` `ml4gp.controller.company_reasearch.company_research`
- 响应：流式（SSE / chunk）

**JSON Body**

| 字段 | 读取方式 | 默认值 |
| --- | --- | --- |
| `messages` | `.get` | `[]` |
| `content` | `.get` | `` |
| `msggroup` | `.get` | `` |
| `language` | `.get` | `cn` |
| `code` | `.get` | `` |
| `regenerate_response` | `.get` | 无 |

### GET `/v2/api/instruction/polish`

<a id="get-v2-api-instruction-polish-10"></a>

- 路由键：`instructionPolish`
- 鉴权：需要 x-api-key，免登录
- v1 镜像：`GET /v1/api/instruction/polish`（同一 handler；v1 不校验 `x-api-key`）
- 实现：`ml4gp/ml4gp/controller/polishing_instruction.py:7` `ml4gp.controller.polishing_instruction.instruction_polish`
- 响应：JSON 信封 `{code,message,status,data}`

**Query**

| 字段 | 读取方式 | 默认值 |
| --- | --- | --- |
| `instruction` | `.get` | 无 |
| `language` | `.get` | `cn` |

### POST `/v2/api/external/chatCompletions`

<a id="post-v2-api-external-chatcompletions-11"></a>

- 路由键：`externalChatCompletions`
- 鉴权：需要 x-api-key，v2 免登录；v1 需登录
- v1 镜像：`POST /v1/api/external/chatCompletions`（同一 handler；v1 不校验 `x-api-key`）
- 实现：`ml4gp/ml4gp/controller/external_chat.py:13` `ml4gp.controller.external_chat.external_chat_completions`
- 响应：流式（SSE / chunk）
- 显式错误码：`PARAMS_ERROR`

**JSON Body**

| 字段 | 读取方式 | 默认值 |
| --- | --- | --- |
| `messages` | `.get` | 无 |

### POST `/v2/api/tw/chatCompletions`

<a id="post-v2-api-tw-chatcompletions-12"></a>

- 路由键：`chatCompletions`
- 鉴权：需要 x-api-key，v2 免登录；v1 需登录
- v1 镜像：`POST /v1/api/tw/chatCompletions`（同一 handler；v1 不校验 `x-api-key`）
- 实现：`ml4gp/ml4gp/controller/trust_wallet.py:22` `ml4gp.controller.trust_wallet.chat_completions`
- 响应：流式（SSE / chunk）
- 显式错误码：`ILLEGAL_REQUEST`, `PARAMS_ERROR`

**JSON Body**

| 字段 | 读取方式 | 默认值 |
| --- | --- | --- |
| `messages` | `.get` | 无 |
| `msggroup` | `.get` | 无 |

### POST `/v2/api/tw/delMsgGroupList`

<a id="post-v2-api-tw-delmsggrouplist-13"></a>

- 路由键：`delMsgGroupList`
- 鉴权：需要 x-api-key，v2 免登录；v1 需登录
- v1 镜像：`POST /v1/api/tw/delMsgGroupList`（同一 handler；v1 不校验 `x-api-key`）
- 实现：`ml4gp/ml4gp/controller/trust_wallet.py:64` `ml4gp.controller.trust_wallet.tw_del_msggroup_list`
- 响应：JSON 信封 `{code,message,status,data}`
- 显式错误码：`PARAMS_ERROR`

**JSON Body**

| 字段 | 读取方式 | 默认值 |
| --- | --- | --- |
| `msggroup` | 下标，缺失会抛错 | 必有 |

### POST `/v2/api/tw/msggroup/generate`

<a id="post-v2-api-tw-msggroup-generate-14"></a>

- 路由键：`generateMsggroup`
- 鉴权：需要 x-api-key，v2 免登录；v1 需登录
- v1 镜像：`POST /v1/api/tw/msggroup/generate`（同一 handler；v1 不校验 `x-api-key`）
- 实现：`ml4gp/ml4gp/controller/trust_wallet.py:76` `ml4gp.controller.trust_wallet.generate_msggroup`
- 响应：JSON 信封 `{code,message,status,data}`

无额外 query/body 字段（或参数在更下游动态拼装）。

### POST `/v2/api/getMindMap`

<a id="post-v2-api-getmindmap-15"></a>

- 路由键：`getMindMap`
- 鉴权：需要 x-api-key，免登录
- v1 镜像：`POST /v1/api/getMindMap`（同一 handler；v1 不校验 `x-api-key`）
- 实现：`ml4gp/ml4gp/controller/mind_maps.py:12` `ml4gp.controller.mind_maps.get_mind_map`
- 响应：JSON 信封 `{code,message,status,data}`
- 显式错误码：`NOT_AUTHORIZED`

**JSON Body**

| 字段 | 读取方式 | 默认值 |
| --- | --- | --- |
| `message` | `.get` | 无 |
| `msggroup` | `.get` | `` |
| `language` | `.get` | `cn` |
| `code` | `.get` | `` |
| `regenerate_response` | `.get` | `null` |
| `type` | `.get` | `1` |

### GET `/v2/api/llm/model/list`

<a id="get-v2-api-llm-model-list-16"></a>

- 路由键：`llmModelList`
- 鉴权：需要 x-api-key，v2 免登录；v1 需登录
- v1 镜像：`GET /v1/api/llm/model/list`（同一 handler；v1 不校验 `x-api-key`）
- 实现：`ml4gp/ml4gp/controller/llm_models.py:10` `ml4gp.controller.llm_models.llm_model_list`
- 响应：JSON 信封 `{code,message,status,data}`

无额外 query/body 字段（或参数在更下游动态拼装）。

### POST `/v2/api/auto/ui/swap`

<a id="post-v2-api-auto-ui-swap-17"></a>

- 路由键：`autoUIForSwap`
- 鉴权：需要 x-api-key，需登录
- v1 镜像：`POST /v1/api/auto/ui/swap`（同一 handler；v1 不校验 `x-api-key`）
- 实现：`ml4gp/ml4gp/controller/auto_ui.py:11` `ml4gp.controller.auto_ui.auto_ui_process`
- 响应：流式（SSE / chunk）

**JSON Body**

| 字段 | 读取方式 | 默认值 |
| --- | --- | --- |
| `query` | `.get` | `` |
| `msggroup` | `.get` | `` |
| `language` | `.get` | `cn` |
| `code` | `.get` | `` |
| `regenerate_response` | `.get` | `null` |

### GET `/v2/api/cryptoBeauty/questions`

<a id="get-v2-api-cryptobeauty-questions-18"></a>

- 路由键：`cryptoBeautyQuestions`
- 鉴权：需要 x-api-key，v2 免登录；v1 需登录
- v1 镜像：`GET /v1/api/cryptoBeauty/questions`（同一 handler；v1 不校验 `x-api-key`）
- 实现：`ml4gp/ml4gp/controller/cryptobeauty.py:6` `ml4gp.controller.cryptobeauty.quess_question`
- 响应：JSON 信封 `{code,message,status,data}`

无额外 query/body 字段（或参数在更下游动态拼装）。

### GET `/v2/api/cryptoBeauty/getAnlayzer`

<a id="get-v2-api-cryptobeauty-getanlayzer-19"></a>

- 路由键：`cryptoBeautyAnalyzer`
- 鉴权：需要 x-api-key，免登录
- v1 镜像：`GET /v1/api/cryptoBeauty/getAnlayzer`（同一 handler；v1 不校验 `x-api-key`）
- 实现：`ml4gp/ml4gp/controller/cryptobeauty.py:63` `ml4gp.controller.cryptobeauty.get_analyzer`
- 响应：JSON 信封 `{code,message,status,data}`

**Query**

| 字段 | 读取方式 | 默认值 |
| --- | --- | --- |
| `id` | `.get` | 无 |

### POST `/mpcbot/sendchat_gpt4`

<a id="post-mpcbot-sendchat-gpt4-20"></a>

- 路由键：`http4gpt4`
- 鉴权：免 x-api-key，需登录
- 实现：`GenAI/genaipf/controller/gpt.py:27` `genaipf.controller.gpt.http4gpt4`
- 响应：JSON 信封 `{code,message,status,data}`

无额外 query/body 字段（或参数在更下游动态拼装）。

### POST `/v2/api/messages/add`

<a id="post-v2-api-messages-add-21"></a>

- 路由键：`add_message`
- 鉴权：需要 x-api-key，需登录
- 实现：`GenAI/genaipf/controller/gpt.py:81` `genaipf.controller.gpt.add_message`
- 响应：JSON 信封 `{code,message,status,data}`

**JSON Body**

| 字段 | 读取方式 | 默认值 |
| --- | --- | --- |
| `messages` | `.get` | 无 |

### GET `/v2/api/getMessageList`

<a id="get-v2-api-getmessagelist-22"></a>

- 路由键：`get_message_list`
- 鉴权：需要 x-api-key，免登录
- 实现：`GenAI/genaipf/controller/gpt.py:32` `genaipf.controller.gpt.get_message_list`
- 响应：JSON 信封 `{code,message,status,data}`

**Query**

| 字段 | 读取方式 | 默认值 |
| --- | --- | --- |
| `msggroup` | `.get` | `` |

### GET `/v2/api/getMsgGroupList`

<a id="get-v2-api-getmsggrouplist-23"></a>

- 路由键：`get_msggroup_list`
- 鉴权：需要 x-api-key，免登录
- 实现：`GenAI/genaipf/controller/gpt.py:119` `genaipf.controller.gpt.get_msggroup_list`
- 响应：JSON 信封 `{code,message,status,data}`
- `data` 字面量键：`messageList`

**Query**

| 字段 | 读取方式 | 默认值 |
| --- | --- | --- |
| `fixedSource` | `.get` | `` |

### POST `/v2/api/delMsgGroupList`

<a id="post-v2-api-delmsggrouplist-24"></a>

- 路由键：`del_msggroup_list`
- 鉴权：需要 x-api-key，需登录
- 实现：`GenAI/genaipf/controller/gpt.py:167` `genaipf.controller.gpt.del_msggroup_list`
- 响应：JSON 信封 `{code,message,status,data}`
- 显式错误码：`PARAMS_ERROR`

**JSON Body**

| 字段 | 读取方式 | 默认值 |
| --- | --- | --- |
| `msggroup` | 下标，缺失会抛错 | 必有 |

### POST `/v2/api/sendStreamChat`

<a id="post-v2-api-sendstreamchat-25"></a>

- 路由键：`send_stream_chat`
- 鉴权：需要 x-api-key，免登录
- 实现：`GenAI/genaipf/controller/gptstream.py:106` `genaipf.controller.gptstream.send_stream_chat`
- 响应：流式（SSE / chunk）

**JSON Body**

| 字段 | 读取方式 | 默认值 |
| --- | --- | --- |
| `language` | `.get` | `en` |
| `msggroup` | `.get` | 无 |
| `messages` | `.get` | `[]` |
| `code` | `.get` | `` |
| `model` | `.get` | `` |
| `source` | `.get` | `v001` |
| `chain_id` | `.get` | `` |
| `owner` | `.get` | `Mlion.ai` |
| `agent_id` | `.get` | `null` |
| `output_type` | `.get` | `text` |
| `llm_model` | `.get` | `openai` |
| `wallet_type` | `.get` | `AI` |
| `visitor_id` | `.get` | `` |
| `without_minus` | `.get` | `0` |
| `regenerate_response` | `.get` | `null` |
| `search_type` | `.get` | `null` |
| `trade_signal_text` | `.get` | 无 |
| `content` | `.get` | 无 |

### POST `/v2/api/sendStylizedRequest`

<a id="post-v2-api-sendstylizedrequest-26"></a>

- 路由键：`send_stylized_request`
- 鉴权：需要 x-api-key，免登录
- 实现：`GenAI/genaipf/controller/gpt_oneshot.py:115` `genaipf.controller.gpt_oneshot.send_stylized_request`
- 响应：流式（SSE / chunk）

**JSON Body**

| 字段 | 读取方式 | 默认值 |
| --- | --- | --- |
| `type` | `.get` | 无 |

### POST `/v2/api/userRate`

<a id="post-v2-api-userrate-27"></a>

- 路由键：`user_rate`
- 鉴权：需要 x-api-key，需登录
- 实现：`GenAI/genaipf/controller/userRate.py:12` `genaipf.controller.userRate.user_rate`
- 响应：JSON 信封 `{code,message,status,data}`
- 显式错误码：`PARAMS_ERROR`

**Query**

| 字段 | 读取方式 | 默认值 |
| --- | --- | --- |
| `code` | 下标，缺失会抛错 | 必有 |
| `rate` | 下标，缺失会抛错 | 必有 |
| `comment` | `.get` | `` |

### POST `/v2/api/delMessages`

<a id="post-v2-api-delmessages-28"></a>

- 路由键：`del_message_by_codes`
- 鉴权：需要 x-api-key，需登录
- 实现：`GenAI/genaipf/controller/userRate.py:100` `genaipf.controller.userRate.del_message_by_codes`
- 响应：JSON 信封 `{code,message,status,data}`
- 显式错误码：`PARAMS_ERROR`

**JSON Body**

| 字段 | 读取方式 | 默认值 |
| --- | --- | --- |
| `code` | 下标，缺失会抛错 | 必有 |

### POST `/v2/api/shareMessages`

<a id="post-v2-api-sharemessages-29"></a>

- 路由键：`share_message`
- 鉴权：需要 x-api-key，免登录
- 实现：`GenAI/genaipf/controller/userRate.py:53` `genaipf.controller.userRate.share_message`
- 响应：JSON 信封 `{code,message,status,data}`

**JSON Body**

| 字段 | 读取方式 | 默认值 |
| --- | --- | --- |
| `code` | `.get` | 无 |
| `messages` | `.get` | 无 |
| `language` | `.get` | `cn` |
| `qrcode_url` | `.get` | `` |
| `summary` | `.get` | `0` |

### POST `/v2/api/getShareMessages`

<a id="post-v2-api-getsharemessages-30"></a>

- 路由键：`get_share_message`
- 鉴权：需要 x-api-key，免登录
- 实现：`GenAI/genaipf/controller/userRate.py:87` `genaipf.controller.userRate.get_share_message`
- 响应：JSON 信封 `{code,message,status,data}`
- 显式错误码：`PARAMS_ERROR`

**JSON Body**

| 字段 | 读取方式 | 默认值 |
| --- | --- | --- |
| `code` | `.get` | 无 |

### POST `/v2/api/tw/feedback`

<a id="post-v2-api-tw-feedback-31"></a>

- 路由键：`user_opinion_for_tw`
- 鉴权：需要 x-api-key，免登录
- 实现：`GenAI/genaipf/controller/userRate.py:32` `genaipf.controller.userRate.user_opinion_for_tw`
- 响应：JSON 信封 `{code,message,status,data}`
- 显式错误码：`PARAMS_ERROR`

**JSON Body**

| 字段 | 读取方式 | 默认值 |
| --- | --- | --- |
| `code` | `.get` | `` |
| `opinion` | `.get` | `` |
| `comment` | `.get` | `` |

### POST `/v2/api/assistantChat`

<a id="post-v2-api-assistantchat-32"></a>

INPUT:

- 路由键：`assistant_chat`
- 鉴权：需要 x-api-key，免登录
- 实现：`GenAI/genaipf/controller/assistant_api.py:68` `genaipf.controller.assistant_api.assistant_chat`
- 响应：JSON 信封 `{code,message,status,data}`

**JSON Body**

| 字段 | 读取方式 | 默认值 |
| --- | --- | --- |
| `outer_user_id` | `.get` | `` |
| `biz_id` | `.get` | `` |
| `source` | `.get` | `` |
| `content` | `.get` | `[]` |
| `access_token` | `.get` | `` |

### POST `/v2/api/getAssistantHistory`

<a id="post-v2-api-getassistanthistory-33"></a>

- 路由键：`get_user_history`
- 鉴权：需要 x-api-key，免登录
- 实现：`GenAI/genaipf/controller/assistant_api.py:140` `genaipf.controller.assistant_api.get_user_history`
- 响应：JSON 信封 `{code,message,status,data}`

**JSON Body**

| 字段 | 读取方式 | 默认值 |
| --- | --- | --- |
| `outer_user_id` | `.get` | `` |
| `biz_id` | `.get` | `` |
| `source` | `.get` | `` |
| `num_limit` | `.get` | `10` |
| `access_token` | `.get` | `` |
