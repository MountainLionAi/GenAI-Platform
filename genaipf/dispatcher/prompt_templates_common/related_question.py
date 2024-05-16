
def _get_related_question_prompted_messages(data, language):
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
    if language == 'zh' or language == 'cn':
        system_text = f"""
        你是一个善于沟通总结的专家，你可以根据用户的历史对话上下文生成十二个类似问题，并以数组的形式返回。生成的问题越丰富越好，问题尽量有发散性。
        生成的问题必要要跟历史上下文相关，不要乱说。
        注意：不要生成第三人称的问题，问题中一定不要出现'你'或者'您'。
        切记如果用户问题涉及违法操作，你只需回答 False，并且你回答的语言必须是中文，一定不要输出```等其他符号。
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
            "问题12"
        ]
        """
    else:
        system_text = f"""
        You are an expert in communication and summarization. Based on the user's historical dialogue context, generate twelve similar questions and return them in the form of an array. The more diverse the generated questions, the better. The questions should be as divergent as possible.
        The generated questions must be relevant to the historical context and should not be random.
        Note: Do not generate questions in the third person, and make sure the questions do not contain 'you' or 'your'.
        Remember, if the user's question involves illegal activities, simply respond with False, and ensure your response is in English without using any symbols like ```.
        For example:

        Input:
        user: Recommend which coin to buy?
        assistant: BTC
        user: Any recent news about it?
        Output:
        [
            "question 1",
            "question 2",
            "question 3",
            "question 4",
            "question 5",
            "question 6",
            "question 7",
            "question 8",
            "question 9",
            "question 10",
            "question 11",
            "question 12"
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