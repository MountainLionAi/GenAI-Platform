from anthropic import AsyncAnthropic
import os
import json
from genaipf.utils.log_utils import logger
import traceback
from genaipf.utils.interface_error_notice_tg_bot_util import send_notice_message

anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")
async_client = AsyncAnthropic(api_key=anthropic_api_key)

async def claude_cached_api_call(model_name="claude-3-5-sonnet-20241022", system_prompt="", system_prompt_ref="", ml_messages=[]):
    # messages = []
    # for _m in ml_messages:
    #     message = {
    #         "role": _m["role"],
    #         "content": [
    #             {
    #                 "type": "text",
    #                 "text": _m["content"],
    #                 "cache_control": {"type": "ephemeral"}
    #             }
    #         ]
    #     }
    #     messages.append(message)
    # if contains_chinese(system_prompt):
    #     system_prompt = system_prompt + "\n" + "输出格式要求：尽量使用两三个markdown的表格对分析进行描述或者总结。\n输出语言要求：以系统提示词的语言返回，不要以用户输入的语言返回，切记切记！！！"
    # else:
    #     system_prompt = system_prompt + "\n" + "Output format requirements: Try to use two or three markdown tables to describe or summarize the analysis.\nOutput language requirement: Return in the language of the system prompt, do not return in the user's input language, remember, remember!!!"
    logger.info(f"调用claude模型传入的消息列表:{ml_messages}")
    if system_prompt_ref:
        system = [
            {
                "type": "text",
                "text": system_prompt,
                "cache_control": {"type": "ephemeral"}
            },
            {
                "type": "text",
                "text": system_prompt_ref
            }
        ]
    if system_prompt_ref:
        try:
            async with async_client.messages.stream(
                model=model_name,
                max_tokens=2048,
                temperature=0,
                system=system,
                messages=ml_messages,
                extra_headers={"anthropic-beta": "prompt-caching-2024-07-31"}
            ) as stream:
                async for event in stream:
                    if event.type == 'text':
                        yield event.text
                if stream._AsyncMessageStream__final_message_snapshot:
                    usage = stream._AsyncMessageStream__final_message_snapshot.usage
                    logger.info(f"claude usage={usage}")
        except Exception as e:
            err_message = f"调用claude_cached_api_call带缓存api出现异常：{e}"
            logger.error(err_message)
            err_message = traceback.format_exc()
            logger.error(err_message)
            await send_notice_message('genai_claude_client', 'claude_cached_api_call', 0, err_message, 4)
            raise e
    else:
        try:
            async with async_client.messages.stream(
                model=model_name,
                max_tokens=2048,
                temperature=0,
                system=system_prompt,
                messages=ml_messages
            ) as stream:
                async for event in stream:
                    if event.type == 'text':
                        yield event.text
        except Exception as e:
            err_message = f"调用claude_cached_api_call无缓存api出现异常：{e}"
            logger.error(err_message)
            err_message = traceback.format_exc()
            logger.error(err_message)
            await send_notice_message('genai_claude_client', 'claude_cached_api_call', 0, err_message, 4)
            raise e

async def claude_tools_call(functions=None, system_prompt="", ml_messages=[]):
    from genaipf.dispatcher.api import get_format_output
    try:
        tools = []
        if functions:
            for function in functions:
                function['input_schema'] = function.pop('parameters')
        tool_name = ''
        _arguments = ''
        async with async_client.messages.stream(
            model="claude-3-5-sonnet-20241022",
            tools=functions,
            max_tokens=2048,
            temperature=0,
            system=system_prompt,
            messages=ml_messages
        ) as stream:
            async for event in stream:
                if event.type == 'content_block_start' and event.content_block.type == 'tool_use':
                    tool_name = event.content_block.name
                elif event.type == 'input_json':
                    _arguments += event.partial_json
        if tool_name:
            yield get_format_output("step", "agent_routing")
            func_name, sub_func_name = tool_name.split("_____")
            _param = json.loads(_arguments)
            _param["func_name"] = func_name
            _param["sub_func_name"] = sub_func_name
            _param["subtype"] = sub_func_name
            yield get_format_output("inner_____func_param", _param)
        else:
            yield get_format_output("step", "llm_yielding")
    except Exception as e:
        err_message = f"调用claude_tools_call api出现异常：{e}"
        logger.error(err_message)
        err_message = traceback.format_exc()
        logger.error(err_message)
        await send_notice_message('genai_claude_client', '调用claude_tools_call', 0, err_message, 4)
        raise e