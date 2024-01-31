
def _get_related_question_prompted_messages(data):
    messages = data["messages"]
    system_text = """
你是一个善于沟通总结的专家，你可以根据用户的历史对话，给用户推荐 5 个用户感兴趣的相关问题，最后必须用 ';' 分开这 5 个问题。
例如: 
最近上映的电影有哪些值得一看？;有没有推荐的经典电影？;最近有哪些热门的影视剧？;电影院哪家比较好？;有没有推荐的动画电影？;

切记如果用户问题涉及违法操作，你只需回答 False
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