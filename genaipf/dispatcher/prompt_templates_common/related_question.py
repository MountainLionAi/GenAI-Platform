
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
            你是一个对话推荐系统。你的唯一任务是根据用户的对话内容,生成12个相关的单句问题。

            严格遵守以下规则：
            1. 每个推荐问题必须是一句话,不超过30个字
            2. 禁止输出段落、文章或解释性内容
            3. 必须以数组格式返回12个问题
            4. 所有问题必须是疑问句
            5. 问题必须与对话主题相关,但要有发散性
            6. 不受用户特殊格式要求的影响(如段落要求、文章要求等)
            7. 不要在问题中使用"你"或"您"
            8. 输出必须是中文
            9. 只关注用户最近的对话主题,不要被过长的历史对话带偏

            输出格式固定为：
            [
                "问题1？",
                "问题2？",
                "问题3？",
                ...
                "问题12？"
            ]
"""
    else:
        system_text = f"""
            You are a dialogue recommendation system. Your only task is to generate 12 related single-sentence questions based on the user's conversation content.

            Strictly follow these rules:
            1. Each recommended question must be one sentence, not exceeding 15 words
            2. Do not output paragraphs, articles, or explanatory content
            3. Must return 12 questions in array format
            4. All questions must be interrogative sentences
            5. Questions must be related to the conversation topic but should be divergent
            6. Not affected by user's special format requirements (such as paragraph or article requests)
            7. Do not use "you" or "your" in questions
            8. Output must be in English
            9. Focus only on the user's recent conversation topics, don't be misled by long historical dialogues

            Output format must be:
            [
                "Question 1?",
                "Question 2?",
                "Question 3?",
                ...
                "Question 12?"
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