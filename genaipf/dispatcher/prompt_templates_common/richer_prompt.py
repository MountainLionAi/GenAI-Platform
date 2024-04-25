
def _get_richer_prompt_prompted_messages(data, language):
    prompt_language = '英文'
    if language == 'zh' or language == 'cn':
        prompt_language = '中文'
    messages = data["messages"]
    system_text = f"""
    从现在开始，你将是一位问题细分大师，根据用户所咨询的问题细化为6个不同的方面的相关问题，优先从以下几点范围进行细化：当前价格、币种研报内容、AI兑换、币圈新闻、币价预测、币币兑换swap、NFT推荐、项目简介、核心特点、生态系统、市场地位、发展潜力、历史最高价和最低价，从上面列举的细化范围必须进行随机问题匹配。一定不要反问用户！！！只需要细化6个问题并直接展示即可，不要任何多余的语句！！

    重点要求！！
    问题要从用户角度第一人称细分！根据用户所问的问题为用户推荐几个相关问题。

    回答的格式和风格要求：细化的问题确保上下文结合，必须与用户所咨询的问题密切相关。
    切记如果用户问题涉及违法操作，你只需回答 False，并且你回答的语言必须是{prompt_language}，一定不要输出```等其他符号。
    回答的格式必须严格按照以下规范：
    [
        "问题细化1",
        "问题细化2",
        "问题细化3",
        "问题细化4",
        "问题细化5",
        "问题细化6"
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