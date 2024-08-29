import anthropic
from examples.claude.prompt_caching.system_prompt_storage import system_prompts

client = anthropic.Anthropic(api_key='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')





response = client.beta.prompt_caching.messages.create(
    model="claude-3-5-sonnet-20240620",
    max_tokens=1024,
    system=[
        {
            "type": "text",
            "text": system_prompts.get("SOURCE005"),
            "cache_control": {"type": "ephemeral"}
        }
        # ,
        # {
        #     "type": "text",
        #     "text": "Here is the full text of a complex legal agreement: [Insert full text of a 50-page legal agreement here]",
        #     "cache_control": {"type": "ephemeral"}
        # }
    ],
    messages=[
        {
            "role": "user",
            "content": "联系方式"
        }
    ]
)
print(response)
