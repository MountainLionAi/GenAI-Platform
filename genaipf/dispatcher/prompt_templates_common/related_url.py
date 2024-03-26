
'''

以下是一些例子：
例 1：
输入：
user: eth 的官网是什么？
assistant: https://ethereum.org
user: 微软的官网是什么？
assistant: https://www.microsoft.com
user: 它的创始人是谁？
输出：
https://ethereum.org;https://www.microsoft.com


例 2：
输入：
user: 这个网站 qq.com
输出：
https://qq.org
'''

def _get_related_url_prompted_messages(data, language):
    prompt_language = '英文'
    if language == 'zh':
        prompt_language = '中文'
    messages = data["messages"]
    system_text = f"""
你是一个善于从对话中提取网址的专家，你可以根据多人的历史对话提取涉及到的网址, 并以 ";" 分割多个网址. 不论网址有没有意义，只要任何人提到了任何网址都提取出来. 如果你不能提取任何网址，就返回 "None"
    """
    msg_l = []
    for m in messages:
        if m["role"] in ["system", "user", "assistant"]:
            msg_l.append(f'{m["role"]}: {m["content"]}')
    ref = "\n".join(msg_l)
    last_msg = f"""
列出 user 和 assistant 的对话中提到了哪些网址，并以 ; 分割多个 url
```
{ref}
```
"""
    return [
        {"role": "system", "content": system_text},
        {"role": "user", "content": last_msg},
    ]