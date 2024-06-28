'''
https://docs.llamaindex.ai/en/stable/examples/llm/openai.html
'''
import asyncio
from llama_index.llms import ChatMessage, OpenAI
from genaipf.conf.server import OPENAI_API_KEY

async def test1():
    messages = [
        ChatMessage(
            role="system", content="You are a pirate with a colorful personality"
        ),
        ChatMessage(role="user", content="What is your name"),
    ]
    resp = await OpenAI(api_key=OPENAI_API_KEY).achat(messages)
    type(resp.message.content)
    resp.message.content

    ##############
    msgs = [
        {"role": "user", "content": "推荐买什么币？"},
        {"role": "assistant", "content": "BTC"},
        {"role": "user", "content": "它最近有什么新闻"}
    ]
    msgs = [
        {"role": "user", "content": "推荐买股票？"},
        {"role": "assistant", "content": "MSFT"},
        {"role": "user", "content": "他的ceo是谁？"}
    ]
    data = {}
    data["messages"] = msgs
    from genaipf.dispatcher.prompt_templates_common.enrich_question import _get_enrich_question_prompted_messages
    from genaipf.dispatcher.utils import simple_achat
    m_l = _get_enrich_question_prompted_messages(data)
    x = await simple_achat(m_l)
    print(x)



    msgs = [
        {"role": "user", "content": "推荐买股票？"},
        {"role": "assistant", "content": "MSFT"},
        {"role": "user", "content": "他的ceo是谁？"}
    ]
    data = {}
    data["messages"] = msgs
    from genaipf.dispatcher.prompt_templates_common.related_question import _get_related_question_prompted_messages
    from genaipf.dispatcher.utils import simple_achat
    m_l = _get_related_question_prompted_messages(data, 'en')
    x = await simple_achat(m_l)
    print(x.strip(";").split(";"))




    msgs = [
        {"role": "user", "content": "推荐买股票？"},
        {"role": "assistant", "content": "MSFT"},
        {"role": "user", "content": "他的ceo是谁？"}
    ]
    data = {}
    data["messages"] = msgs
    from genaipf.dispatcher.prompt_templates_common.if_need_search import _get_if_need_search_prompted_messages
    from genaipf.dispatcher.utils import simple_achat
    m_l = _get_if_need_search_prompted_messages(data)
    x = await simple_achat(m_l)
    print(x)
    
asyncio.run(test1())