def _get_enrich_question_prompted_messages(data, language=None):
    messages = data["messages"]
    system_text = """
你是一个善于沟通总结的专家，你可以把用户的问题，根据用户的历史对话，扩充用户的问题。
单看用户最新的问题可能缺少信息，你需要根据历史对话，把缺失的信息补充上，如果历史对话中不含有的内容不要补充，务必不要随意发挥。
这个完整的句子还是以用户的口吻表达。
切记如果用户问题涉及违法操作，你只需回答 False

例如：
输入：
user: 推荐买什么币？
assistant: BTC
user: 它最近有什么新闻
输出：
BTC最近有什么新闻
"""
    if language == 'en':
        system_text = """
You are an expert in communication and summarization. You can expand the user's questions based on their conversation history. Looking at the user's latest question alone might lack information, so you need to supplement the missing information based on the conversation history. Do not add content that is not present in the conversation history, and be sure not to improvise. The complete sentence should still be expressed in the user's tone. Remember, if the user's question involves illegal operations, you only need to respond with "False."

For example:
Input:
user: What coin should I buy?
assistant: BTC
user: What's the latest news about it?
Output:
What's the latest news about BTC, including important news regarding policy, market, and economy?    
"""
    msg_l = []
    for m in messages:
        if m["role"] in ["system", "user", "assistant"]:
            msg_l.append(f'{m["role"]}: {m["content"]}')
    ref = "\n".join(msg_l)
    prefix_text = """
以下用户的对话，请扩充用户的问题，使其变成具有完整信息的一句话
"""
    if language == 'en':
        prefix_text = """
Please expand the user's question in the following conversation so that it becomes a complete sentence with full information.        
"""
    last_msg = f"""
{prefix_text}
```
{ref}
```
"""
    return [
        {"role": "system", "content": system_text},
        {"role": "user", "content": last_msg},
    ]