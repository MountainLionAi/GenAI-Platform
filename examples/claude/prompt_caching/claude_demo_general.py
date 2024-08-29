import anthropic
import time
from examples.claude.prompt_caching.system_prompt_storage import system_prompts

client = anthropic.Anthropic(api_key='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')
MODEL_NAME = "claude-3-5-sonnet-20240620"


def make_cached_api_call():
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
                    "text": "忘记钱包密码"
                }
            ]
        }
    ]

    start_time = time.time()
    response = client.messages.create(
        model=MODEL_NAME,
        extra_headers={"anthropic-beta": "prompt-caching-2024-07-31"},
        max_tokens=1000,
        system=[
            {
                "type": "text",
                "text": system_prompts.get("SOURCE005"),
                "cache_control": {"type": "ephemeral"}
            }
        ],
        messages=messages,
    )
    end_time = time.time()
    return response, end_time - start_time

cached_response, cached_time = make_cached_api_call()

print(cached_response.usage)

print(f"Cached API call time: {cached_time:.2f} seconds")
print(f"Cached API call input tokens: {cached_response.usage.input_tokens}")
print(f"Cached API call output tokens: {cached_response.usage.output_tokens}")

print("\nSummary (cached):")
print(cached_response.content)