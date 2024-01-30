
def _get_related_question_prompted_messages(data):
    messages = data["messages"]
    system_text = """
你是一个善于沟通总结的专家，你可以根据用户的历史对话，给用户推荐 5 个用户感兴趣的相关问题，用 ';' 分开这 5 个问题。

例如：
输入：
user: 推荐买什么币？
assistant: BTC
user: 它最近有什么新闻
输出：
BTC最新价格预测是多少？;近期有哪些影响BTC的事件？;BTC的长期投资价值如何？;BTC交易平台哪个更安全？;BTC和ETH未来哪个更有前景？;
"""
    msg_l = []
    for m in messages:
        if m["role"] in ["system", "user", "assistant"]:
            msg_l.append(f'{m["role"]}: {m["content"]}')
    ref = "\n".join(msg_l)
    last_msg = f"""
```
{ref}
```
"""
    return [
        {"role": "system", "content": system_text},
        {"role": "user", "content": last_msg},
    ]