import asyncio
from genaipf.dispatcher.prompts_common import LionPromptCommon
from genaipf.dispatcher.utils import simple_achat

msgs = [
    {"role": "user", "content": "推荐买股票？"},
    {"role": "assistant", "content": "MSFT"},
    {"role": "user", "content": "他的ceo是谁？"}
]
data = {}
data["messages"] = msgs

async def main():
    msgs1 = LionPromptCommon.get_prompted_messages("if_need_search", data)
    msgs2 = LionPromptCommon.get_prompted_messages("enrich_question", data)
    msgs3 = LionPromptCommon.get_prompted_messages("related_question", data)
    t1 = asyncio.create_task(simple_achat(msgs1))
    t2 = asyncio.create_task(simple_achat(msgs2))
    t3 = asyncio.create_task(simple_achat(msgs3))
    # t1t2t3 并发运行的；
    # 另外如果不需要搜索（t1 的结果是 False），不用等待 t2 和 网络搜索
    await t1
    need_search = t1.result()
    if need_search in "True":
        print(f"need search: {need_search}")
        await t2
        print(f"enriched question: {t2.result()}")
    await t3
    print(f"related_question: {t3.result()}")

asyncio.run(main())