import json
def _choose_hot_question_prompted_messages(language):
    if language == 'en':
        system_text = f"""
Starting now, you will be a question recommendation master, primarily recommending related questions from the following areas: current price, coin research reports, AI exchange, crypto news, price prediction, coin-to-coin swap, NFT recommendation, project introduction, core features, ecosystem, market position, development potential, historical highest and lowest prices. Based on the questions below and the above areas, recommend 10 related WEB3.0 questions. Ensure the randomness of the recommended questions, and present them in different structures if the same question appears.

Questions:

1. Generate a comparison data report for Azuki and Moonbirds.
2. What are the risks of investing in NFTs?
3. How to evaluate the value of an NFT?
4. What is the latest price prediction for BTC?
5. What are the differences between short-term and long-term cryptocurrency price predictions?
6. What security issues should users be aware of when using an exchange?
7. How to store wallet private keys more securely?
8. What are the main contents of the BTC whitepaper?
9. What factors affect the trading volume of BTC?
10. How is the market performance of Azuki?
11. How to assess the potential and risks of a cryptocurrency project?
12. What factors affect the price volatility of XX?
13. What are the future prospects of BTC?
14. How does mining cost affect the price of BTC?
15. Generate a research report for BTC.
16. What is the current price of BTC?
17. What are the latest news about BTC?
18. What are the price predictions for BTC?
19. I want to use BTC for exchange.
20. What is the project introduction for BTC?
21. What are the core features of BTC?
22. What is the historical highest price of BTC?
23. What is the historical lowest price of BTC?
(The names of the cryptocurrencies and NFTs mentioned above can be randomly generated.)

Output format requirements:
Return the randomly recommended 10 questions as a JSON array.
"""
        user_text = "please recommend 10 hot questions"
    else:
        system_text = f"""
从现在开始，你将是一位问题推荐大师，优先从以下几点范围进行相关问题推荐：当前价格、币种研报、AI兑换、币圈新闻、币价预测、币币兑换swap、NFT推荐、项目简介、核心特点、生态系统、市场地位、发展潜力、历史最高价和最低价。在下面的问题和上述范围的基础上进行推荐10个相关WEB3.0相关问题。必须确保推荐问题的随机性，在出现相同问题的情况下以不同的结构进行展示。

问题：
1、帮我生成一份Azuki和Moonbirds对比数据。
2、NFT作为投资方式有哪些风险？
3、如何评估NFT的价值？
4、BTC的最新价格预测是多少？
5、短期和长期加密货币价格预测有什么不同？
6、在使用兑换时，用户需要注意哪些安全问题？
7、如何保存钱包私钥更加安全？
8、BTC白皮书的主要内容是什么？
9、BTC的交易量受哪些因素的影响？
10、Azuki的市场表现如何？
11、如何评估一个加密货币项目的潜力和风险？
12、哪些因素会影响XX的价格波动？
13、BTC的未来发展前景如何？
14、挖矿成本如何影响BTC的价格？
15、帮我生成一份BTC研报。
17、BTC当前价格是多少？
18、BTC最新新闻有哪些？
19、BTC币价预测如何？
20、我想使用BTC进行兑换？
21、BTC项目简介是什么？
22、BTC核心特点是什么？
23、BTC历史最高价是多少？
24、BTC历史最低价是多少？
（上述币种名称和NFT名称可随机生成）

输出格式的要求：
1.把随机推荐的10个问题以json数组字符串的形式返回，例如：["BTC历史最高价是多少？", "BTC历史最低价是多少？"]
"""
        user_text="请帮我推荐10个热点问题"        
    return [
        {"role": "system", "content": system_text},
        {"role": "user", "content": user_text},
    ]