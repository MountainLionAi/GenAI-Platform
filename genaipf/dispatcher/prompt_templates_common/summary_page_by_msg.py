

def _get_summary_page_by_msg_prompted_messages(data, language):
    prompt_language = '英文'
    if language == 'zh':
        prompt_language = '中文'
    messages = data["messages"]
    article_text = data["article_text"]
    system_text = f"""
你是一个善于总结的语言专家，也是顶级的程序员，能从混乱的 html 内容中找到重要的信息，你可以根据 user 的历史对话和提供的参考文章内容总结，总结整个文章的内容摘要，另外从参考文章中提取 user 可能关心的内容，特别是重要的数字如价格、比例等
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
总结整个文章的内容摘要，另外从参考文章中提取 user 可能关心的内容
以上是 user 和 assistant 的历史对话，从以下文章内容中总结整个文章的内容摘要，并总结出 user 可能关心的内容
=====
{article_text}
=====
"""
    return [
        {"role": "system", "content": system_text},
        {"role": "user", "content": last_msg},
    ]
    
# 以上是 user 和 assistant 的历史对话，从以下文章内容中总结出 user 可能关心的摘要内容，摘要内容要准确精炼