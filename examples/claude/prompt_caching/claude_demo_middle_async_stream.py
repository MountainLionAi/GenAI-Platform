import anthropic
import time
from examples.claude.prompt_caching.system_prompt_storage import system_prompts
import asyncio

async_client = anthropic.AsyncAnthropic(api_key='')
MODEL_NAME = "claude-3-5-sonnet-20240620"


async def make_cached_api_call():
    messages = [
        {
            "role": "user",
            "content": [
                # {
                #     "type": "text",
                #     "text": "<book>" + book_content + "</book>",
                #     "cache_control": {"type": "ephemeral"}
                # },
                {
                    "type": "text",
                    "text": "忘记密码怎么办"
                }
            ]
        }
    ]

    start_time = time.time()
    async with async_client.messages.stream(
        model=MODEL_NAME,
        extra_headers={"anthropic-beta": "prompt-caching-2024-07-31"},
        max_tokens=1000,
        system=[
            {
                "type": "text",
                "text": system_prompts.get("SOURCE005"),
                "cache_control": {"type": "ephemeral"}
            },
            {
                "type": "text",
                "text": system_prompts.get("SOURCE005_REF"),
            }
        ],
        messages=messages,
    ) as stream:
        async for event in stream:
            if event.type == 'text':
                yield event.text
        end_time = time.time()
        yield end_time - start_time
    
async def main():
    async for text in make_cached_api_call():
        print(text)

# 使用 asyncio.run() 来运行 main 函数
asyncio.run(main())
