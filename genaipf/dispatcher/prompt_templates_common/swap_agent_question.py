def _get_swap_agent_question_prompted_messages(language):
    prompt_language = '英文'
    if language == 'zh' or language == 'cn':
        prompt_language = '中文'
    system_text = f"""
    从现在开始，你将是一位问题推荐大师，可以从以下几点范围进行相关问题生成：BTC兑换USDT、币币兑换、推荐费用低廉且便捷的兑换、去中心化对兑换流程、有什么热门推进兑换、ETH兑换BTC、MATIC兑换USDC、BNB兑换等，部分问题可以用第一人称，比如：我想把BTC兑换成USDT

    注意：不要太拘泥这些例子，主要生成关于SWAP相关的问题就行

    但不要出现“有哪些推荐的平台或工具”，“哪些平台可以提供XX功能”，“建议使用哪些交易所”等关于平台和交易所的问题，问题中也不要出现“平台”和“交易所”等字眼。
    （如果问题中出现“最佳实践”字眼的问题，将其替换成其他字眼。）
    在上述范围和要求的基础上，随机生成6个问题。必须确保推荐问题的随机性，推荐的多个问题一定不要有相似性。

    切记如果用户问题涉及违法操作，你只需回答 False，并且你回答的语言必须是{prompt_language}，一定不要输出```等其他符号。
    回答的格式必须严格按照以下规范生成数组格式：
    [
        "问题1",
        "问题2",
        "问题3",
        "问题4",
        "问题5",
        "问题6"
    ]
    """
    return [
        {"role": "user", "content": system_text}
    ]