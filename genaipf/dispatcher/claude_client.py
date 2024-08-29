from anthropic import AsyncAnthropic
import os
from genaipf.utils.log_utils import logger

anthropic_api_key = os.getenv("ANTHROPIC_API_KEY")
async_client = AsyncAnthropic(api_key=anthropic_api_key)

async def claude_cached_api_call(model_name="claude-3-5-sonnet-20240620", system_prompt="", ml_messages=[]):
    messages = []
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
    logger.info(f"调用claude模型传入的消息列表:{ml_messages}")
    async with async_client.messages.stream(
        model=model_name,
        max_tokens=1000,
        temperature=0,
        system=[
            {
                "type": "text",
                "text": system_prompt,
                "cache_control": {"type": "ephemeral"}
            }
        ],
        messages=ml_messages,
        extra_headers={"anthropic-beta": "prompt-caching-2024-07-31"}
    ) as stream:
        async for event in stream:
            if event.type == 'text':
                yield event.text


