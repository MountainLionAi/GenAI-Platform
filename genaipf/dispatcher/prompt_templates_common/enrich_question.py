def _get_enrich_question_prompted_messages(data):
    messages = data["messages"]
    system_text = """
你是一个善于沟通总结的专家，你可以把用户的问题，根据用户的历史对话，扩充用户的问题。
单看用户最新的问题可能缺少信息，你需要根据历史对话，把缺失的信息补充上，同时扩充信息让问题更丰富，形成信息完整而且丰富的一句话问题。
这个完整的句子还是以用户的口吻表达。

例如：
输入：
user: 推荐买什么币？
assistant: BTC
user: 它最近有什么新闻
输出：
BTC最近有什么新闻，政策，市场，经济等方面的重要新闻
"""
    msg_l = []
    for m in messages:
        if m["role"] in ["system", "user", "assistant"]:
            msg_l.append(f'{m["role"]}: {m["content"]}')
    ref = "\n".join(msg_l)
    last_msg = f"""
以下用户的对话，请扩充用户的问题，使其变成具有完整信息的一句话
```
{ref}
```
"""
    return [
        {"role": "system", "content": system_text},
        {"role": "user", "content": last_msg},
    ]