import anthropic
import time
from examples.claude.prompt_caching.system_prompt_storage import system_prompts
import asyncio

async_client = anthropic.AsyncAnthropic(api_key='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')
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
    response = await async_client.messages.create(
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
    )
    end_time = time.time()
    return response, end_time - start_time

cached_response, cached_time = asyncio.run(make_cached_api_call())

print(cached_response.usage)

print(f"Cached API call time: {cached_time:.2f} seconds")
print(f"Cached API call input tokens: {cached_response.usage.input_tokens}")
print(f"Cached API call output tokens: {cached_response.usage.output_tokens}")

print("\nSummary (cached):")
print(cached_response.content)

"""
Usage(input_tokens=432, output_tokens=451, cache_creation_input_tokens=4819, cache_read_input_tokens=0)
Cached API call time: 6.58 seconds
Cached API call input tokens: 432
Cached API call output tokens: 451

Summary (cached):
[TextBlock(text='对于Trust Wallet来说，忘记密码确实是一个严重的问题，但不用过于担心，我来为您解释一下具体情况和解决方法：\n\n1. 密码的作用：\n   Trust Wallet使用密码主要是为了保护应用程序本身和管理钱包。您在创建或导入钱包时设置的密码，后续在登录、转账等操作时都需要输入。\n\n2. 密码无法找回：\n   作为非托管、去中心化的多链钱包，Trust Wallet不会存储用户的钱包密码，也无法帮您找回密码。\n\n3. 解决方法：\n   您可以通过重新导入助记词或私钥来重置钱包密码。这就是为什么我们一再强调备份助记词或私钥的重要性。\n\n4. 重要提醒：\n   如果您没有备份助记词或私钥，忘记钱包密码可能意味着您的资产将永久丢失。\n\n5. 预防措施：\n   为了避免这种情况发生，请务必将您的助记词或私钥安全备份，并存储在安全的地方。\n\n如果您有备份助记词，我可以指导您如何重新导入钱包并设置新密码。如果没有，我强烈建议您立即备份当前钱包的助记词，以防将来出现类似情况。\n\n您现在是否已经备份了助记词？需要我指导您如何重新导入钱包吗？', type='text')]

Usage(input_tokens=432, output_tokens=430, cache_creation_input_tokens=0, cache_read_input_tokens=4819)
Cached API call time: 6.24 seconds
Cached API call input tokens: 432
Cached API call output tokens: 430

Summary (cached):
[TextBlock(text='我理解忘记密码可能会让您感到焦虑，但请不用太担心。让我为您解释一下Trust Wallet的密码机制和解决方案:\n\n1. 密码的作用:\nTrust Wallet的密码主要用于保护应用程序和管理钱包。您在创建或导入钱包时设置的密码，后续用于登录和转账等操作。\n\n2. 密码无法找回:\n作为非托管、去中心化的多链钱包，Trust Wallet不会存储用户的密码，也无法帮您找回密码。\n\n3. 解决方法:\n您可以通过重新导入助记词或私钥来重置钱包密码。这就是为什么我们一再强调备份助记词的重要性。\n\n4. 如果没有备份:\n很遗憾，如果您既忘记了密码又没有备份助记词或私钥，这意味着您的资产可能永久丢失。\n\n5. 建议:\n- 如果您还记得助记词，请立即使用它重新导入钱包并设置新密码。\n- 今后请务必妥善保管好您的助记词，将其存储在安全的地方。\n- 考虑使用多重备份方式，如纸质记录和加密存储等。\n\n记住，保护好您的助记词比保护密码更加重要。有了助记词，您随时可以恢复对钱包的访问权限。', type='text')]
"""
