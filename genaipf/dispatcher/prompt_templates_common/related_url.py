
def _get_related_url_prompted_messages(data, language):
    prompt_language = '英文'
    if language == 'zh':
        prompt_language = '中文'
    messages = data["messages"]
    system_text = f"""
你是一个善于沟通总结的专家，你可以根据用户的历史对话上下文提取涉及到的 url，并以数组的形式返回。
切记如果用户对话历史没有涉及任何 url，你只需回答 False

例 1：
输入：
user: eth 的官网是什么？
assistant: https://ethereum.org
user: 微软的官网是什么？
assistant: https://www.microsoft.com
user: 它的创始人是谁？
输出：
[
    "https://ethereum.org",
    "https://www.microsoft.com",
]

例 2：
输入：
user: 你好
assistant: 你好
user: 你叫什么？
输出：
False


例 3：
输入：
user: 这个网站 qq.com
输出：
[
    "https://qq.org",
]
    """
    msg_l = []
    for m in messages:
        if m["role"] in ["system", "user", "assistant"]:
            msg_l.append(f'{m["role"]}: {m["content"]}')
    ref = "\n".join(msg_l)
    last_msg = f"""
user 和 assistant 的对话中提到了哪些网址 url?
```
{ref}
```
"""
    return [
        {"role": "system", "content": system_text},
        {"role": "user", "content": last_msg},
    ]