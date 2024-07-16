

def _get_share_summary_prompted_messages(data, language):
    prompt_language = '英文'
    if language == 'zh' or language == 'cn':
        prompt_language = '中文'
    messages = data
    system_text = f"""
你是一个善于总结的对话内容的专家，能用简洁的方式将用户的对话内容总结成一句话，总结的内容必须是根据用户的对话记录所进行的总结
约束：
1. 总结的内容必须简单
2. 必须用{prompt_language}进行回复
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
以上是 user 和 assistant 的历史对话，基于这些记录进行总结
"""
    return [
        {"role": "system", "content": system_text},
        {"role": "user", "content": last_msg},
    ]