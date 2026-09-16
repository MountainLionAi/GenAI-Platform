# Agent 架构与扩展指南

本文档描述 **GenAI-Platform（平台框架层）** 与 **ml4gp（业务插件层）** 中 Agent 体系的完整架构、请求处理流程、关键组件实现，以及新业务功能的扩展步骤。

> 运行关系：通过环境变量 `PLUGIN_NAME=ml4gp`，GenAI-Platform 在运行时动态加载 ml4gp 的 functions、preset、prompt、tool_agent 等实现，覆盖平台默认配置。

---

## 目录

1. [整体架构](#1-整体架构)
2. [Agent 的三种含义](#2-agent-的三种含义)
3. [主链路：Function Calling 驱动的路由](#3-主链路function-calling-驱动的路由)
4. [Function / Preset / Prompt 三者关系](#4-function--preset--prompt-三者关系)
5. [意图识别与二次意图](#5-意图识别与二次意图)
6. [现有 Tool 与 Function 清单](#6-现有-tool-与-function-清单)
7. [其他 Agent 实现](#7-其他-agent-实现)
8. [插件扩展机制](#8-插件扩展机制)
9. [实例流程](#9-实例流程)
10. [添加新功能步骤](#10-添加新功能步骤)
11. [相关代码索引](#11-相关代码索引)

---

## 1. 整体架构

```
用户请求 (sendStreamChat)
        │
        ▼
┌───────────────────────────────────────────────────────────┐
│              GenAI-Platform (genaipf)                      │
│  gptstream.py → afunc_gpt_generator → converter.py        │
│  agent/autogen.py  agent/llama_index.py  tools/search/*   │
└───────────────────────────┬───────────────────────────────┘
                            │ PLUGIN_NAME=ml4gp
┌───────────────────────────▼───────────────────────────────┐
│                    ml4gp (业务插件)                         │
│  functions.py      → 意图 catalog + VDB 筛选               │
│  preset_entry.py   → 数据层 (DB/API/链上)                  │
│  prompt_templates  → 回答模板                               │
│  tool_agent.py     → LangChain 多步 Agent                  │
│  intent_recog.py   → 二次意图                              │
│  agentic_rag_*     → 新闻分析专用流水线                     │
└───────────────────────────────────────────────────────────┘
```

### 设计特点

| 特点 | 说明 |
|------|------|
| Function Calling 为主路径 | 大部分业务走「GPT 选 function → 拉数据 → LLM 生成」 |
| Tool Agent 为增强路径 | 复杂多步推理走 LangChain `AgentExecutor`（默认未启用） |
| 插件化扩展 | 新业务主要在 ml4gp 增加 function + preset + prompt |
| 统一命名规范 | `func_name_____sub_func_name` 贯穿 function、VDB、prompt、tool agent |

---

## 2. Agent 的三种含义

系统中「Agent」在不同层次有不同含义，避免混淆：

| 层次 | 含义 | 实现位置 | 作用 |
|------|------|----------|------|
| **产品层 Agent** | 前端展示的 AI Agent 列表（头像、标题、标签） | `ml4gp/controller/ai_agent.py` + DB 表 `ai_agent_en/zh` | 聊天记录关联、`agent_id` 用于「最近使用」排序 |
| **Function Agent** | GPT Function Calling 驱动的意图路由 | `functions.py` → `converter.py` → `preset_entry.py` | **主路径**，处理绝大多数业务 |
| **Tool/Multi Agent** | LangChain / AutoGen 多步推理 | `tool_agent.py`、`agent/autogen.py` | 增强路径，需显式启用 |

> 产品层的 `agent_id` 不参与核心路由逻辑，仅用于消息存储与列表展示。

---

## 3. 主链路：Function Calling 驱动的路由

### 3.1 流程图

```
用户消息
   │
   ▼
getAnswerAndCallGpt (gptstream.py)
   │
   ├── 并行: RAG 搜索 / 相关问题 / AI Ranking
   │
   ▼
afunc_gpt_generator (api.py)
   │  System: get_afunc_prompt() — 引导 GPT 选择 function
   │  VDB: gpt_function_filter() — 向量库预筛选候选 functions
   │
   ▼
GPT 返回 function call 或纯文本
   │
   ├── route_mode = "text"
   │       └── aref_answer_gpt_generator — 直接 LLM + RAG 回答
   │
   └── route_mode = "function"
           │
           ├── func_name ∈ need_tool_agent_l ?
           │       └── run_tool_agent — LangChain Agent（默认未启用）
           │
           └── convert_func_out_to_stream
                   ├── intent_recog — 二次意图（可选）
                   ├── preset_entry — 拉取结构化数据
                   └── aref_answer_gpt_generator — 生成最终回答
```

### 3.2 关键步骤

**Step 1 — 意图识别（Function Filter + Function Choice）**

- `gpt_function_filter()`：用向量库从大量 function 中筛选候选（解决 OpenAI function 数量限制）
- `afunc_gpt_generator()`：将候选 functions 发给 GPT，由模型决定调用哪个
- Function 命名：`{func_name}_____{sub_func_name}`，例如 `coin_price_____info`

**Step 2 — Function 参数解析**（`api.py`）

```python
big_func_name = tool_call.function.name          # "coin_price_____trend"
func_name, sub_func_name = big_func_name.split("_____")
_param = json.loads(arguments)
_param["func_name"] = func_name                  # "coin_price"
_param["sub_func_name"] = sub_func_name          # "trend"
yield get_format_output("inner_____func_param", _param)
```

**Step 3 — 执行分支**（`gptstream.py`）

```python
if func_name in need_tool_agent_l or whole_func_name in need_tool_agent_l:
    stream_gen = run_tool_agent(...)           # LangChain 路径
else:
    stream_gen = convert_func_out_to_stream(...)  # 标准路径
```

---

## 4. Function / Preset / Prompt 三者关系

### 4.1 流水线分工

```
用户问题
   │
   ▼
┌─────────────┐   「认场景 + 抽参数」
│  Function   │   GPT Function Calling 的 JSON Schema
└──────┬──────┘
       │ func_name + sub_func_name + {symbol, address, ...}
       ▼
┌─────────────┐   「拿数据」
│   Preset    │   调 DB/API，产出 picked_content + presetContent
└──────┬──────┘
       │ picked_content（给 LLM 的文本上下文）
       │ presetContent（给前端的结构化卡片）
       ▼
┌─────────────┐   「怎么说」
│   Prompt    │   system prompt 模板，控制语气、格式、引用方式
└──────┬──────┘
       ▼
   流式回答 + 可选 UI 卡片
```

### 4.2 各组件职责

| 组件 | 文件位置 | 职责 |
|------|----------|------|
| **Function** | `ml4gp/dispatcher/functions.py` | 定义触发场景 + 参数 schema |
| **Preset** | `ml4gp/controller/preset_entry.py` | 根据参数拉取真实数据 |
| **Prompt** | `ml4gp/dispatcher/prompt_templates_v001/*.py` | 控制 LLM 如何组织回答 |

### 4.3 命名关联规则

```
Function 全名:  coin_price_____trend
                 │              │
                 │              └── sub_func_name（子场景）
                 └── func_name（主场景）

Preset 按 func_name 查:   preset_entry_mapping["coin_price"]
Prompt 按 preset.type 查: preset_name="preset1" → prompts_v001.py 选模板
```

### 4.4 业务对应表

| func_name | sub_func 举例 | preset.type | prompt 模板文件 |
|-----------|---------------|-------------|-----------------|
| `coin_price` | info, trend, analyze... | `preset1` | default（兜底） |
| `coin_info` | info, holdAddress... | `preset2` | coin_info.py |
| `good_news` | team, history... | `preset3` | good_news.py |
| `coin_predict` | coin_predict | `preset4` | coin_predict.py |
| `coin_swap` | coin_swap | `coin_swap` | coin_swap.py |
| `check_address` | check_address | `check_address` | onchain_data.py |
| `generate_report` | generate_report | `generate_report` | generate_report.py |
| `currency_comparison` | coin | `currency_comparison` | currency_comparison.py |
| `purchase_recommendation` | nft | `purchase_recommendation` | purchase_recommendation.py |

### 4.5 Prompt 的两套用法

| 阶段 | 方法 | 调用时机 | 作用 |
|------|------|----------|------|
| **意图识别** | `get_afunc_prompt()` | `afunc_gpt_generator` 阶段 | 引导 GPT 选择 function |
| **最终回答** | `get_aref_answer_prompt(preset_name=...)` | `aref_answer_gpt_generator` 阶段 | 控制拿到数据后如何生成回答 |

`preset.type` 主要影响第二套 prompt 的模板选择，在 `ml4gp/dispatcher/prompts_v001.py` 的 `LionPrompt.get_aref_answer_prompt()` 中按 `preset_name` 分支。

---

## 5. 意图识别与二次意图

### 5.1 一次意图（Primary Intent）

| 项目 | 说明 |
|------|------|
| **执行者** | GPT Function Calling（`afunc_gpt_generator`） |
| **粒度** | 业务场景级别（coin_price / check_address / coin_swap 等） |
| **实现** | `functions.py` + `vdb_pairs/gpt_func.py` 向量映射 |
| **输出** | `func_name`、`sub_func_name`、结构化参数 |

示例：

```
用户: "BTC 现在趋势怎么样"
  → GPT 选择: coin_price_____trend
  → 参数: { "symbol": "BTC", "need_chart": 1 }
```

### 5.2 二次意图（Secondary Intent）

| 项目 | 说明 |
|------|------|
| **执行者** | `intent_recog_mapping`（`converter.py` 中 function 触发后、preset 之前） |
| **粒度** | 同一 function 内的分支 |
| **实现** | `intent_recog.py` + 额外 LLM 判断 |
| **当前启用** | 仅 `check_address` |

与 `sub_func_name` 的区别：

- **sub_func_name**：GPT 选 function 时就确定的子场景（如 `trend` / `info`），影响 preset 取哪块数据
- **二次意图**：function 已确定后，再判断走特殊流水线还是常规模板

`check_address` 二次意图分支：

| 二次意图 | 条件 | 处理路径 |
|----------|------|----------|
| `address_analysis` | 对话意图为链上分析 + 地址格式合法 + 链支持 | `async_spec_address_analyse` → 链上分析卡片，跳过常规 preset+prompt |
| `customer_support` | 对话意图为客服求助 | 走常规 `preset_entry` + `onchain_data` prompt + GPT 回答 |

配置位置：`ml4gp/controller/preset_entry.py` → `intent_recog_mapping`

---

## 6. 现有 Tool 与 Function 清单

### 6.1 GPT Functions（主路径，约 45 个）

定义于 `ml4gp/dispatcher/functions.py`，由 GPT Function Calling 触发。

**币价 / 行情**

- `coin_price_____*`：info, trend, analyze, flow, order, trade, historyOneDay, historyHighPrice, tradeRatio, tradeHistory

**币种信息**

- `coin_info_____*`：info, holdAddress, transfer, markets

**资讯 / 预测**

- `good_news_____*`：team, Investors, history, good_news, social_media
- `coin_predict_____coin_predict`
- `multi_coin_price_____multi_coin_price`
- `multi_coin_predict_____multi_coin_predict`
- `generate_report_____generate_report`

**Swap / 钱包 / 链上**

- `coin_swap_____coin_swap`
- `wallet_balance_____wallet_balance`
- `token_transfer_____token_transfer`
- `qrcode_address_____qrcode_address`
- `check_address_____check_address`
- `check_hash_____check_hash`
- `get_gas_____get_gas`
- `check_order_____check_order`
- `buy_but_not_receive_____buy_but_not_receive`
- `why_can_not_transfer_out_____why_can_not_transfer_out`
- `transfer_was_stolen_____base_question`
- `transfer_wrong_chain_____transfer_wrong_chain`

**NFT**

- `nft_list_____*`：collection, saleHistory
- `nft_info_____*`：detail, detailSaleHistory, detailPriceHistory, detailInfo
- `purchase_recommendation_____nft`
- `nft_comparison_____nft`

**其他**

- `currency_comparison_____coin`
- `url_search_____url_search`

> 部分 function 在代码中被注释（如 `black_address`、`transfer_only`），未上线。

### 6.2 LangChain Tool Agent（已实现，默认未启用）

| 配置项 | 位置 | 说明 |
|--------|------|------|
| Tool 实现 | `ml4gp/dispatcher/tool_agent_templates/langchain_event_v001.py` | `get_crypto_coin_price` |
| 路由映射 | `ml4gp/dispatcher/tool_agent.py` | `coin_price` → `coin_price_tool_agent_demo` |
| 启用开关 | `ml4gp/dispatcher/functions.py` | `need_tool_agent_l`（当前被注释） |

取消注释 `need_tool_agent_l` 后，`coin_price` 相关请求会走 LangChain `AgentExecutor` 多步推理路径。

### 6.3 Search Agent Tools（RAG 搜索阶段）

LlamaIndex Agent 工具（`genaipf/tools/search/metaphor/llamaindex_tools.py`）：

- `metaphor_search` — 联网搜索
- `show_related_questions` — 生成相关问题

底层搜索引擎适配：

| 引擎 | 文件 |
|------|------|
| Metaphor (Exa) | `metaphor_search_agent.py` |
| Google Serper | `google_serper_agent.py` |
| Bing | `bing_search_agent.py` |
| Perplexity | `perplexity_search_agent.py` |

### 6.4 AutoGen Multi-Agent（实验性）

- 封装：`genaipf/agent/autogen.py` → `AutoGenMultiAgent`
- 示例：`examples/multi_agent_t001.py`（Planner / Packer / Courier 协作）
- 状态：未接入主聊天链路

### 6.5 Agentic RAG News Insight（独立流水线）

- 文件：`ml4gp/controller/agentic_rag_news_insight.py`
- 用途：新闻深度解读（情感分析 → 生成搜索问题 → 并行搜索 → 综合分析）
- 与主聊天链路独立，不经过 `gptstream` 的 function calling 流程

---

## 7. 其他 Agent 实现

### 7.1 LlamaIndex Agent

`genaipf/agent/llama_index.py` 封装 `OpenAIAgent`，用于 RAG 搜索场景的查询转换与工具调用，支持工具执行事件的流式输出。

### 7.2 AutoGen Multi-Agent

`genaipf/agent/autogen.py` 基于微软 AutoGen，支持：

- `UserProxyAgent` + 多个 `AssistantAgent`
- `GroupChat` + `GroupChatManager` 多轮协作
- 通过 `func_configs` 为每个 Agent 注册工具函数

### 7.3 工具包装

`genaipf/agent/utils.py` 提供：

- `_wrap()` — 将实例方法包装为 LangChain/AutoGen 可用的 async 工具
- `merge_async_generators()` — 合并多个异步生成器输出
- `create_function_from_method()` — 去除 `self` 参数创建独立函数

---

## 8. 插件扩展机制

GenAI-Platform 通过 `PLUGIN_NAME` 环境变量动态 import ml4gp 模块，覆盖平台默认实现：

| 模块 | 平台默认 | ml4gp 插件覆盖 |
|------|----------|----------------|
| `dispatcher/functions.py` | 示例 weather/medical | 全部业务 functions |
| `dispatcher/tool_agent.py` | fake_example_func | coin_price LangChain agent |
| `controller/preset_entry.py` | 空/基础 | 全部数据获取逻辑 |
| `dispatcher/vdb_pairs/gpt_func.py` | 向量库映射 | 业务 QA → function 映射 |
| `dispatcher/prompt_templates_v001/` | default | 各业务 prompt |
| `routers/entry.py` | 基础路由 | AI Agent 列表等 API |

加载逻辑示例（`genaipf/dispatcher/functions.py`）：

```python
if PLUGIN_NAME:
    plugin_submodule = import_module(f'{PLUGIN_NAME}.dispatcher.functions')
    gpt_functions_mapping = plugin_submodule.gpt_functions_mapping
    need_tool_agent_l = getattr(plugin_submodule, "need_tool_agent_l", [])
```

---

## 9. 实例流程

### 9.1 标准路径：「BTC 现在趋势怎么样」

```
① 用户发消息 → POST /api/v1/sendStreamChat

② 并行准备（gptstream.py）
   - RAG 搜索任务 sources_task
   - 相关问题任务
   - gpt_function_filter() 向量库筛选候选 functions

③ 一次意图识别（afunc_gpt_generator）
   GPT 返回:
     name: coin_price_____trend
     arguments: {"symbol": "BTC", "need_chart": 1}

④ 解析参数（api.py）
   func_name = "coin_price", sub_func_name = "trend"

⑤ convert_func_out_to_stream
   a) intent_recog: coin_price 不在 mapping → 跳过
   b) preset_entry:
        getAndPickKlineInfoData("BTC", "cn", "trend")
        → presetContent = { coinName, trend图表数据, ... }
        → picked_content = "BTC 当前价格 $xxx，24h涨跌 +2.3%..."
   c) aref_answer_gpt_generator:
        preset_name = "preset1" → default prompt
        → 流式输出 gpt token
   d) need_chart=1 → yield inner_____preset（前端图表卡片）

⑥ 前端收到: sources + gpt 流式文字 + preset 图表卡片
```

### 9.2 二次意图：「帮我分析地址 0xABC...」

```
① 一次意图
   GPT → check_address_____check_address
   参数: { address: "0x3Ddf...5296", chain: "ETH" }

② 二次意图（converter.py）
   _async_get_check_address_intent()
   → LLM 判断: "address_analysis"
   → 地址合法 + 链支持 → need_spec = True

③ 特殊分支（不走常规 preset + prompt）
   async_spec_address_analyse()
   → 链上标签分析、交易历史
   → yield inner_____preset_top（前端分析卡片）
   → return（结束）

对比 — 若用户说「钱包收不到 USDT，地址是 0x3Ddf...」:
   → 二次意图: "customer_support"
   → need_spec = False
   → 走常规 preset_entry + onchain prompt + GPT 客服回答
```

### 9.3 带 UI 卡片：「把 1 ETH 换成 USDT」

```
① 一次意图: coin_swap_____coin_swap
   { from_token: "ETH", to_token: "USDT", from_token_amount: "1", ... }

② Preset: getTokenSwapInfo() → presetContent（兑换路径、汇率、手续费）

③ yield inner_____preset_top → 前端渲染 Swap 卡片

④ Prompt: get_aref_answer_prompt("coin_swap") → 简短文字说明

⑤ yield inner_____preset → 补充完整 preset 数据
```

---

## 10. 添加新功能步骤

### 10.1 场景 A：标准 Function 路径（推荐）

以新增「查询 DeFi 协议 TVL」为例。

#### Step 1 — 定义 Function（必须）

文件：`ml4gp/dispatcher/functions.py`

```python
"defi_tvl_____protocol": {
    "name": "defi_tvl_____protocol",
    "description": "查询某 DeFi 协议的 TVL、锁仓量",
    "parameters": {
        "type": "object",
        "properties": {
            "protocol": {
                "type": "string",
                "description": "协议名称，如 Uniswap, Aave"
            },
            "need_chart": {
                "type": "integer",
                "description": "直接返回 1"
            },
        },
        "required": ["protocol", "need_chart"]
    }
}
```

#### Step 2 — 添加 VDB 映射（建议）

文件：`ml4gp/dispatcher/vdb_pairs/gpt_func.py`

```python
"某 DeFi 协议的 TVL": "defi_tvl_____protocol",
"查询 Uniswap 锁仓量": "defi_tvl_____protocol",
```

使 `gpt_function_filter()` 能从用户说法中检索到该 function。

#### Step 3 — 实现 Preset 数据层（必须）

文件：`ml4gp/controller/preset_entry.py`

```python
async def getAndPickDefiTvlData(protocol, language, subtype=None):
    # 调用 DeFi API，返回 (presetContent, picked_content)
    ...

preset_entry_mapping["defi_tvl"] = {
    "type": "defi_tvl",
    "has_preset_content": True,       # 若需前端卡片
    "need_preset": True,
    "param_names": ["protocol", "language", "subtype"],
    "get_and_pick": getAndPickDefiTvlData,
}
```

#### Step 4 — 添加 Prompt 模板（按需）

若 default 模板不够用：

1. 新建 `ml4gp/dispatcher/prompt_templates_v001/defi_tvl.py`
2. 在 `ml4gp/dispatcher/prompts_v001.py` 的 `get_aref_answer_prompt()` 中添加分支：

```python
elif preset_name == "defi_tvl":
    return _get_defi_tvl_aref_answer_prompt(language, picked_content, related_qa, model, owner)
```

#### Step 5 — 前端卡片（可选）

- 设置 `has_preset_content: True`
- 在 `get_and_pick` 中返回结构化 `presetContent`
- 若需置顶展示，将 `func_name` 加入 `preset_entry_top_mapping`

#### 检查清单

- [ ] `functions.py` 添加 function 定义
- [ ] `vdb_pairs/gpt_func.py` 添加向量映射
- [ ] `preset_entry.py` 添加 `get_and_pick` + mapping
- [ ] `prompt_templates` 添加专用模板（或复用 default）
- [ ] `prompts_v001.py` 注册 prompt 分支（若新建模板）
- [ ] 运行 `python app.py -a` 重建向量库（若更新了 VDB 映射）
- [ ] 本地测试 function 触发与回答质量

---

### 10.2 场景 B：启用 Tool Agent（多步自主推理）

适用于 LLM 需自主决定调用多个工具、多轮推理的复杂场景。

#### Step 1 — 编写 LangChain Agent

文件：`ml4gp/dispatcher/tool_agent_templates/defi_tvl_agent.py`

```python
@tool
async def get_protocol_tvl(protocol: str) -> str:
    """Returns TVL info for a DeFi protocol."""
    ...

async def defi_tvl_tool_agent(messages, newest_question, ...):
    tools = [get_protocol_tvl]
    agent = create_openai_tools_agent(model, tools, prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools)
    async for event in agent_executor.astream_events(...):
        ...
```

#### Step 2 — 注册路由

文件：`ml4gp/dispatcher/tool_agent.py`

```python
tool_agent_mapping = {
    "defi_tvl": {"name": "defi_tvl", "func": defi_tvl_tool_agent}
}
```

#### Step 3 — 启用开关

文件：`ml4gp/dispatcher/functions.py`

```python
need_tool_agent_l = [
    "defi_tvl",
    "defi_tvl_____protocol",
]
```

---

### 10.3 场景 C：新增二次意图分支

适用于同一 function 需根据对话上下文走不同处理链路。

#### Step 1 — 编写意图判断

文件：`ml4gp/dispatcher/intent_recog.py`

```python
async def async_get_defi_tvl_intent(messages):
    # LLM 判断用户意图
    ...
```

#### Step 2 — 注册 mapping

文件：`ml4gp/controller/preset_entry.py`

```python
intent_recog_mapping["defi_tvl"] = {
    "func": _async_get_defi_tvl_intent,
    "need_spec_gen_l": ["deep_analysis"],
    "deep_analysis": async_spec_defi_analysis,
}
```

#### Step 3 — 实现特殊处理生成器

```python
async def async_spec_defi_analysis(params):
    # 特殊流水线，yield preset / gpt 流
    ...
```

---

### 10.4 场景 D：新增 Multi-Agent 协作

适用于多角色协作的复杂任务。

1. 在 `ml4gp/dispatcher/multi_agent.py`（新建）定义 `multi_agent_mapping`
2. 配置 `agents_config`（system_message + func_configs）
3. 使用 `AutoGenMultiAgent` 封装并调用（参考 `examples/multi_agent_t001.py`）

---

### 10.5 场景 E：新增前端 AI Agent 卡片

1. 在 DB 表 `ai_agent_en` / `ai_agent_zh` 插入记录
2. 前端聊天时传 `agent_id`，消息关联到该 Agent（用于「最近使用」排序）

---

### 10.6 扩展决策树

```
新业务需求
   │
   ├── 单步：识别场景 → 拉数据 → 生成回答？
   │       └── 场景 A（Function + Preset + Prompt）
   │
   ├── 需要 LLM 自主多步调工具？
   │       └── 场景 B（Tool Agent + need_tool_agent_l）
   │
   ├── 同一 function 内要分叉处理？
   │       └── 场景 C（二次意图 intent_recog_mapping）
   │
   ├── 多角色协作？
   │       └── 场景 D（AutoGen Multi-Agent）
   │
   └── 仅前端展示新 Agent？
           └── 场景 E（DB ai_agent 表）
```

---

## 11. 相关代码索引

### GenAI-Platform（平台框架）

| 文件 | 说明 |
|------|------|
| `genaipf/controller/gptstream.py` | 主聊天入口，`getAnswerAndCallGpt` |
| `genaipf/dispatcher/api.py` | `afunc_gpt_generator`、`aref_answer_gpt_generator` |
| `genaipf/dispatcher/converter.py` | `convert_func_out_to_stream`、`run_tool_agent` |
| `genaipf/dispatcher/functions.py` | 平台默认 functions + 插件加载 |
| `genaipf/dispatcher/tool_agent.py` | Tool Agent 路由 + 插件加载 |
| `genaipf/dispatcher/multi_agent.py` | Multi-Agent 配置 + 插件加载 |
| `genaipf/agent/autogen.py` | AutoGen 多 Agent 封装 |
| `genaipf/agent/llama_index.py` | LlamaIndex 搜索 Agent |
| `genaipf/agent/utils.py` | 工具函数包装 |
| `genaipf/tools/search/` | 搜索引擎适配 |
| `examples/multi_agent_t001.py` | AutoGen 示例 |
| `examples/tool_agent_t001.py` | LangChain Tool Agent 示例 |

### ml4gp（业务插件）

| 文件 | 说明 |
|------|------|
| `ml4gp/dispatcher/functions.py` | 全部业务 GPT Functions |
| `ml4gp/controller/preset_entry.py` | 数据层 + intent_recog_mapping |
| `ml4gp/dispatcher/prompts_v001.py` | Prompt 路由分发 |
| `ml4gp/dispatcher/prompt_templates_v001/` | 各业务 Prompt 模板 |
| `ml4gp/dispatcher/vdb_pairs/gpt_func.py` | 向量库 function 映射 |
| `ml4gp/dispatcher/tool_agent.py` | LangChain Tool Agent 注册 |
| `ml4gp/dispatcher/tool_agent_templates/` | Tool Agent 实现 |
| `ml4gp/dispatcher/intent_recog.py` | 二次意图判断 |
| `ml4gp/controller/ai_agent.py` | 产品层 Agent 列表 API |
| `ml4gp/services/ai_agent_service.py` | Agent 列表 DB 查询 |
| `ml4gp/controller/agentic_rag_news_insight.py` | 新闻分析 Agent 流水线 |

---

## 附录：输出格式约定

流式响应中常见的 `role` 类型：

| role | 说明 |
|------|------|
| `gpt` | LLM 流式文字 token |
| `inner_____func_param` | Function 调用参数（内部） |
| `inner_____gpt_whole_text` | 完整回答文本（内部，用于存储） |
| `inner_____preset` | 结构化 preset 数据（底部） |
| `inner_____preset_top` | 结构化 preset 数据（置顶，如 Swap 卡片） |
| `sources` | RAG 引用来源 |
| `step` | 处理步骤状态 |
| `rag_status` | RAG 检索进度 |
| `preset` | 前端展示的 preset 卡片 |

---

*文档版本：2026-06-29*
