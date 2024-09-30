from zhipuai import ZhipuAI


client = ZhipuAI(api_key="ebfdabc3d2e6880623b093baaf388a11.1DgMT57pYD8Fx8Dt")  # 请填写您自己的APIKey
response = client.chat.asyncCompletions.create(
    model="glm-4",  # 请填写您要调用的模型名称
    messages=[
        {"role": "system", "content": "你是一个乐于回答各种问题的小助手，你的任务是提供专业、准确、有洞察力的建议。"},
        {"role": "user", "content": "我对太阳系的行星非常感兴趣，尤其是土星。请提供关于土星的基本信息，包括它的大小、组成、环系统以及任何独特的天文现象。"},
    ],
    stream=True,
)

for chunk in response:
    print(chunk.choices[0].delta)