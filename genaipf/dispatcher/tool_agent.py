from importlib import import_module
from genaipf.conf.server import PLUGIN_NAME
from genaipf.dispatcher.functions import need_tool_agent_l
from langchain.tools import tool


@tool
async def get_word_length(word: str) -> int:
    """Returns the length of a word."""
    return len(word)

@tool
async def multiply(a: int, b: int) -> int:
    """Multiple two integers and returns the result integer"""
    return a * b

@tool
async def add(a: int, b: int) -> int:
    """Add two integers and returns the result integer"""
    return a + b

async def fake_example_func(messages, newest_question, model, language, related_qa, source, owner, sources=[], is_need_search=False, sources_task=None, chain_id=''):
    from langchain import hub
    from langchain.agents import AgentExecutor, create_openai_tools_agent
    from langchain.tools import tool
    from langchain_core.callbacks import Callbacks
    from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
    from langchain_core.messages import AIMessage, HumanMessage
    from langchain_openai import ChatOpenAI
    
    from genaipf.conf.server import os
    from genaipf.dispatcher.api import get_format_output
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    model = ChatOpenAI(model="gpt-4-turbo", temperature=0, streaming=True, openai_api_key=OPENAI_API_KEY)
    
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are very powerful assistant, but don't know current events",
            ),
            MessagesPlaceholder(variable_name="chat_history"),
            ("user", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ]
    )
    
    tools = [get_word_length, multiply, add]
    agent = create_openai_tools_agent(
        model.with_config({"tags": ["agent_llm"]}), tools, prompt
    )
    agent_executor = AgentExecutor(agent=agent, tools=tools).with_config(
        {"run_name": "Agent"}
    )

    chat_history = []
    _last_input = ""
    # _last_input 保留用户问的最后一个问题
    for _m in messages:
        _m["content"] = _m["content"].replace('{', '(').replace('}', ')')
        if _m["role"] == "user":
            chat_history.append(HumanMessage(content=_m["content"]))
            _last_input = _m["content"]
        else:
            chat_history.append(AIMessage(content=_m["content"]))
    chat_history.pop() # 去掉最后一条，最后一条在 _last_input

    # 重点是 kind == "on_chat_model_stream" 这个分支是输出 gpt 的最终结果
    # 其他分支是调用工具等中间环节
    _tmp_text = ""
    async for event in agent_executor.astream_events(
        {
            # "input": "what is the result of 2 * 3 + 4",
            "input": _last_input,
            "chat_history": chat_history
        },
        version="v1",
    ):
        kind = event["event"]
        if kind == "on_chain_start":
            if (
                event["name"] == "Agent"
            ):  # Was assigned when creating the agent with `.with_config({"run_name": "Agent"})`
                print(
                    f"Starting agent: {event['name']} with input: {event['data'].get('input')}"
                )
        elif kind == "on_chain_end":
            if (
                event["name"] == "Agent"
            ):  # Was assigned when creating the agent with `.with_config({"run_name": "Agent"})`
                print()
                print("--")
                print(
                    f"Done agent: {event['name']} with output: {event['data'].get('output')['output']}"
                )
        if kind == "on_chat_model_stream":
            content = event["data"]["chunk"].content
            if content:
                # Empty content in the context of OpenAI means
                # that the model is asking for a tool to be invoked.
                # So we only print non-empty content
                print(content, end="|")
                _tmp_text += content
                yield get_format_output("gpt", content)
        elif kind == "on_tool_start":
            print("--")
            print(
                f"Starting tool: {event['name']} with inputs: {event['data'].get('input')}"
            )
        elif kind == "on_tool_end":
            print(f"Done tool: {event['name']}")
            print(f"Tool output was: {event['data'].get('output')}")
            print("--")
    yield get_format_output("inner_____gpt_whole_text", _tmp_text)


tool_agent_mapping = {
    "medical": {
        "name": "medical",
        "func": fake_example_func
    }
}

tool_agent_sub_mapping = {
    "medical_____treatment": {
        "name": "medical_____treatment",
        "func": fake_example_func
    }
}


if PLUGIN_NAME:
    plugin_submodule_name = f'{PLUGIN_NAME}.dispatcher.tool_agent'
    plugin_submodule = import_module(plugin_submodule_name)
    tool_agent_mapping = getattr(plugin_submodule, "tool_agent_mapping", dict())
    tool_agent_sub_mapping = getattr(plugin_submodule, "tool_agent_sub_mapping", dict())
    # assert set(need_tool_agent_l) == set(tool_agent_mapping.key())