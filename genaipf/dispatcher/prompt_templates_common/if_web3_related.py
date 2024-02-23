
def _get_is_web3_related_prompted_messages(data):
    messages = data["messages"]
    system_text = f"""
    你是一个web3领域的专家，通过用户的问题描述，请根据以下关键词和概念判断该问题是否属于Web3行业。如果问题描述中包含以下任何关键词或概念，请返回True，否则返回False。
    关键词和概念列表:
- 区块链
- 智能合约
- 去中心化应用（DApp）
- 加密货币
- 非同质化代币（NFT）
- 去中心化金融（DeFi）
- 元宇宙
- Web3技术栈
- 链上治理
- 加密钱包
判断结果: [True/False]

例如：
输入：
user: 推荐买什么币？
assistant: BTC
user: 它最近有什么新闻
输出：
True

输入：
user: 推荐买什么币？
assistant: BTC
user: 你好
输出：
True

输入：
user: 哪个NFT值得买？
输出：
True

输入：
user: 美国的首都是哪个城市？
输出：
False
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