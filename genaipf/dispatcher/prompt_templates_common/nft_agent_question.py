def _get_nft_agent_question_prompted_messages(language):
    prompt_language = '英文'
    if language == 'zh' or language == 'cn':
        prompt_language = '中文'
    system_text = f"""
    从现在开始，你将是一位NFT问题推荐大师，优先从以下几点范围进行相关问题生成：项目介绍，市场表现，Azuki和Moonbirds对比（此处的NFT名称可随机替换），推荐一款适合送给女朋友做生日礼物的NFT，风格介绍，投资价值，受欢迎度，活跃度，成交量，持有者数量等。在上述范围的基础上，随机推荐6个NFT相关的问题。
    必须确保推荐问题的随机性，每次都要推荐不同的问题，在出现相同问题的情况下以不同的结构进行展示。

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