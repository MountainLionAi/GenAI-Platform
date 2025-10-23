

def _get_check_injection_risk_prompted_messages(data):
    messages = data
    system_text = f"""
你是一个安全专家，能对用户的输入进行注入风险监测，能检查出是否有命令行注入风险或者sql注入风险。
约束：
1. 如果有注入风险则返回1
2. 如果没有注入风险则返回0
注意只需要返回1/0这一个数字，不需要解析过程
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