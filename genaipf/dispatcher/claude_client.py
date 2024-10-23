from anthropic import AsyncAnthropic
import os
from genaipf.utils.log_utils import logger
from genaipf.utils.common_utils import contains_chinese

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
    if contains_chinese(system_prompt):
        system_prompt = system_prompt + "\n" + "输出格式要求：尽量使用两三个markdown的表格对分析进行描述或者总结。\n输出语言要求：以系统提示词的语言返回，不要以用户输入的语言返回，切记切记！！！"
    else:
        system_prompt = system_prompt + "\n" + "Output format requirements: Try to use two or three markdown tables to describe or summarize the analysis.\nOutput language requirement: Return in the language of the system prompt, do not return in the user's input language, remember, remember!!!"
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
    else:
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


