def _get_recent_search_prompted_messages(data):
    system_text = """
你需要判断用户最后一个问题是否是需要最近、近期、当下的一些信息，你只需要回答 True 或 False

例如：
输入：
user: 它最近有什么新闻
输出：
True

输入：
user: 几天天气怎么样
输出：
False

输入：
user: 你是谁？
输出：
False

输入：
user: 近期btc有什么新闻
输出：
True

"""
 
    return [
        {"role": "system", "content": system_text},
        {"role": "user", "content": data},
    ]