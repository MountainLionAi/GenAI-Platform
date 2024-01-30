def _get_if_need_search_prompted_messages(data):
    messages = data["messages"]
    system_text = """
你是一个大语言模型，你懂得很多，有些问题，你直接能回答，但是有些问题需要网络搜索才能答好。
你需要判断用户最后一个问题是否需要网络搜索，你只需要回答 True 或 False

例如：
输入：
user: 推荐买什么币？
assistant: BTC
user: 它最近有什么新闻
输出：
True

输入：
user: 推荐买什么币？
assistant: BTC
user: 你好
输出：
False

输入：
user: 你是谁？
输出：
False

输入：
user: 美国的首都是哪个城市？
输出：
False

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