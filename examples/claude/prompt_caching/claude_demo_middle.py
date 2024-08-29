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
                    "text": "忘记密码怎么办"
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

cached_response, cached_time = make_cached_api_call()

print(cached_response.usage)

print(f"Cached API call time: {cached_time:.2f} seconds")
print(f"Cached API call input tokens: {cached_response.usage.input_tokens}")
print(f"Cached API call output tokens: {cached_response.usage.output_tokens}")

print("\nSummary (cached):")
print(cached_response.content)


"""
Usage(input_tokens=432, output_tokens=314, cache_creation_input_tokens=4819, cache_read_input_tokens=0)
Cached API call time: 4.98 seconds
Cached API call input tokens: 432
Cached API call output tokens: 314

Summary (cached):
[TextBlock(text='对于忘记Trust Wallet密码的情况，以下是关键信息和解决方案：\n\n1. 密码用途：Trust Wallet的密码用于保护应用程序和管理钱包，在登录和转账时需要输入。\n\n2. 密码无法找回：作为去中心化钱包，Trust Wallet不存储用户密码，也无法帮助找回。\n\n3. 解决方法：通过重新导入助记词或私钥来重置钱包密码。\n\n4. 重要提示：务必提前备份助记词或私钥。如果没有备份，忘记密码可能导致资产永久丢失。\n\n5. 重置步骤：\n   - 卸载并重新安装Trust Wallet应用\n   - 选择"添加已有钱包"\n   - 使用之前备份的助记词或私钥导入\n   - 设置新的密码\n\n请记住，保管好助记词是极其重要的。它是恢复钱包访问权限的唯一方法，应当安全存储在离线环境中。', type='text')]


Usage(input_tokens=432, output_tokens=475, cache_creation_input_tokens=0, cache_read_input_tokens=4819)
Cached API call time: 6.89 seconds
Cached API call input tokens: 432
Cached API call output tokens: 475

Summary (cached):
[TextBlock(text='对于忘记密码的情况，我理解这可能会让您感到焦虑，但请不用太过担心。以下是关于Trust Wallet密码和解决方案的重要信息：\n\n1. 密码的作用：\n   Trust Wallet的密码主要用于保护应用程序和管理钱包。您在创建或导入钱包时设置的密码，后续用于登录和转账等操作。\n\n2. 密码存储：\n   作为非托管、去中心化的多链钱包，Trust Wallet不会存储用户的钱包密码，也无法帮助找回密码。\n\n3. 重置密码的方法：\n   您可以通过重新导入助记词或私钥来重置钱包密码。这就是为什么备份助记词或私钥如此重要。\n\n4. 如果没有备份：\n   很遗憾，如果您既忘记了密码，又没有备份助记词或私钥，这意味着您的资产可能永久丢失。\n\n5. 建议：\n   - 如果您还记得助记词，请立即使用它重新导入钱包并设置新密码。\n   - 未来务必妥善保管您的助记词，将其存储在安全的地方。\n   - 考虑使用多重备份方式，如纸质记录和加密存储等。\n\n记住，保护好您的助记词比保护密码更为重要，因为有了助记词，您随时可以恢复对钱包的访问权限。如果您有任何其他问题或需要进一步的指导，请随时告诉我。', type='text')]
"""