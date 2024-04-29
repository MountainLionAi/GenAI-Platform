
def _get_related_question_prompted_messages(data, language):
    prompt_language = '英文'
    if language == 'zh' or language == 'cn':
        prompt_language = '中文'
    messages = data["messages"]
#     system_text = """
# 你是一个善于沟通总结的专家，你可以根据用户的历史对话，给用户推荐 5 个用户感兴趣的相关问题，用 ';' 分开这 5 个问题。
# 切记如果用户问题涉及违法操作，你只需回答 False
# 例如：
# 输入：
# user: 推荐买什么币？
# assistant: BTC
# user: 它最近有什么新闻
# 输出：
# BTC最新价格预测是多少？;近期有哪些影响BTC的事件？;BTC的长期投资价值如何？;BTC交易平台哪个更安全？;BTC和ETH未来哪个更有前景？;
# """
    system_text = f"""
    你是一个善于沟通总结的专家，你可以根据用户的历史对话上下文生成十二个类似问题，并以数组的形式返回。生成的问题越丰富越好，问题尽量有发散性。
    切记如果用户问题涉及违法操作，你只需回答 False，并且你回答的语言必须是{prompt_language}，一定不要输出```等其他符号。
    例如：
    输入：
    user: 推荐买什么币？
    assistant: BTC
    user: 它最近有什么新闻
    输出：
    [
        "问题1",
        "问题2",
        "问题3",
        "问题4",
        "问题5",
        "问题6",
        "问题7",
        "问题8",
        "问题9",
        "问题10",
        "问题11",
        "问题12",
    ]
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