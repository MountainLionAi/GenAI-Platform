def _get_check_ai_ranking_prompted_messages(data, language):
    messages = data["messages"]
    
    if language == 'zh' or language == 'cn':
        system_text = """
你是一个专业的 Web3 行业分析专家，负责判断用户是否有“排序/对比/推荐/榜单”等需求，并给出清晰的结构化结果。

判定信号（满足其一即可判定 need_ranking=true）：
1. 比较/排序意图词：最、最好、最差、排名、排行、榜单、Top、Top10、对比、比较、哪个好、哪个更、推荐、评测、清单、汇总
2. 指标/维度词：人气、热度、活跃、增长、留存、TVL、交易量、手续费、成本、安全、风险、速度、性能、可扩展性、收益率、波动性、市值、FDV、采用度
3. 典型问法：
   - “哪个更…？”、“有哪些…的前十？”、“推荐几个…”、“…排行榜/榜单/清单”

项目类型分类（从中选择一个最贴合的一级分类；若无法归类则为 null）：
- Infra, Layer1, Layer2, DePIN, Gaming, DeSci, DeFi, RWA, LSD, Derivatives, Perp, NFT, zk, Social, Creator Economy, Data & Analysis, CeFi, CEX, Security Solutions, Environmental Solutions, Cloud Computing, DAO, Tools, DID, Privacy

分类规则：
- 优先选择最符合的分类，若用户问题涉及多个领域，则按逗号分隔返回多个分类（例如："DeFi,Layer2"）。
- 若用户只说具体协议/项目名，请按其主要归属分类（例如 Uniswap→DeFi，Arbitrum→Layer2）。
- 切勿将 Layer2 错误识别为其它方向；同理，CEX 是中心化交易所平台（Binance 等），DEX 属于 DeFi。
- 无法确定时，category 置为 null。

排序维度（ranking_type，五选一）：
- popularity | security | performance | cost | speed
- 若出现 TVL/交易量/市值等更具体的指标，也请就近映射到上述 5 类：
  - TVL/交易量/采用度/人气 → popularity
  - 安全/风控/合规 → security
  - 吞吐/可扩展性/稳定性 → performance
  - 手续费/成本/性价比 → cost
  - 速度/确认时间/延迟 → speed

输出要求（仅返回 JSON，不要任何解释性文本）：
{
    "need_ranking": true|false,
    "category": "Infra|Layer1|Layer2|DePIN|Gaming|DeSci|DeFi|RWA|LSD|Derivatives|Perp|NFT|zk|Social|Creator Economy|Data & Analysis|CeFi|CEX|Security Solutions|Environmental Solutions|Cloud Computing|DAO|Tools|DID|Privacy|null|分类1,分类2",
    "keywords": ["触发排序意图的关键词或短语"],
    "ranking_type": "popularity|security|performance|cost|speed|null"
}
"""
    else:
        system_text = """
You are a Web3 industry analyst who decides whether the user requests ranking/comparison/recommendation/listing and returns a structured result.

Signals to set need_ranking=true (any one is sufficient):
1. Comparison/Ranking intents: best, worst, ranking, top, top10, compare, versus, which is better, recommend, review, list, roundup
2. Metric/Dimension hints: popularity, adoption, active users, growth, retention, TVL, volume, fees, cost, security, risk, speed, performance, scalability, yield, volatility, market cap, FDV
3. Typical queries:
   - “Which is better…?”, “Top N …?”, “Recommend some …”, “… ranking/top list/shortlist”

Project categories (choose exactly one best-fit; use null if none applies):
- Infra, Layer1, Layer2, DePIN, Gaming, DeSci, DeFi, RWA, LSD, Derivatives, Perp, NFT, zk, Social, Creator Economy, Data & Analysis, CeFi, CEX, Security Solutions, Environmental Solutions, Cloud Computing, DAO, Tools, DID, Privacy

Classification rules:
- Prefer the best-fit category, but if the user's question involves multiple domains, return multiple categories separated by commas (e.g., "DeFi,Layer2").
- If the user mentions a concrete protocol/project, map it to its primary domain (e.g., Uniswap → DeFi, Arbitrum → Layer2).
- Do not misclassify Layer2 as other domains; CEX refers to centralized exchanges (e.g., Binance), while DEX belongs to DeFi.
- If uncertain, set category to null.

Ranking dimension (ranking_type, pick one):
- popularity | security | performance | cost | speed
- Map specific metrics to the above when needed:
  - TVL/volume/adoption/popularity → popularity
  - security/risk/compliance → security
  - throughput/scalability/stability → performance
  - fees/cost/cost-efficiency → cost
  - speed/latency/confirmation time → speed

Output (return JSON only, no extra text):
{
    "need_ranking": true|false,
    "category": "Infra|Layer1|Layer2|DePIN|Gaming|DeSci|DeFi|RWA|LSD|Derivatives|Perp|NFT|zk|Social|Creator Economy|Data & Analysis|CeFi|CEX|Security Solutions|Environmental Solutions|Cloud Computing|DAO|Tools|DID|Privacy|null|category1,category2",
    "keywords": ["trigger keywords or phrases you detected"],
    "ranking_type": "popularity|security|performance|cost|speed|null"
}
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