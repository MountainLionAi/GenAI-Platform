from genaipf.tools.search.metaphor import metaphor_search_agent
from llama_index.llms import OpenAI, ChatMessage
from genaipf.agent.llama_index import LlamaIndexAgent
from genaipf.tools.search.metaphor.llamaindex_tools import tools
from genaipf.utils.log_utils import logger
from openai import OpenAI
client = OpenAI()

system_prompt = """
你是个工具人，你既能联网，也能给用户推荐其他感兴趣的问题，必须调用工具 function，有 2 种情况：
### 情况 1
用户问的问题最好联网搜索才能回答更好，
用户问的问题可能是比较简单的表述，直接网络搜索的结果不好，
你扩充丰富一下形成一个全面完整的问题再触发 search 工具 function。
然后再生成 5 个用户可能感兴趣的问题，调用 show_related_questions。
### 情况 2
直接生成 5 个用户可能感兴趣的问题，调用 show_related_questions。

记住不论是否调用，一定要在最后调用 show_related_questions。
"""


# dict sources: [{'title': '', 'url': ''}]
# str content
async def other_search(question: str, related_qa=[], language=None):
    # -------- metaphor --------
    sources, metaphor_result = await metaphor_search_agent.metaphor_search2(question)
    if len(sources) > 0:
        related_qa.append(question + ' : ' + metaphor_result)

    # -------- other --------
    return sources, related_qa


async def premise_search(newest_question, message_history, related_qa=None):
    if related_qa is None:
        related_qa = []
    chat_history = []
    if message_history is not None:
        for question in message_history:
            chat_message = ChatMessage(role="user", content=question)
            chat_history.append(chat_message)
    agent = LlamaIndexAgent(tools, system_prompt=system_prompt, chat_history=chat_history, verbose=True)
    agent.metaphor_query = ""
    agent.metaphor_results = None
    agent.related_questions = []
    agent.start_chat(newest_question)

    async for x in agent.async_response_gen():
        # print(x)
        pass
    related_questions = []
    if agent.related_questions is not None:
        for r_question in agent.related_questions:
            related_questions.append({"title": r_question})
    sources = []
    if agent.metaphor_results and len(agent.metaphor_results.contents) != 0:
        sources, content = get_contents(agent.metaphor_results.contents)
        related_qa.append(newest_question + ':' + content)
    logger.info(f'>>>>> 扩充后的问题: {agent.metaphor_query}')
    logger.info(f'>>>>> 相关话题推荐: {agent.related_questions}')
    return sources, related_qa, related_questions


# format content to str
def get_contents(contents):
    sources = []
    formatted_string = ''
    for index, news_item in enumerate(contents, start=1):
        sources.append({"title": news_item.title, "url": news_item.url})
        formatted_string += f"{news_item.extract}\n引用地址: {news_item.url}\n"
    return sources, formatted_string


async def related_search(question: str, language=None):
    messages = [
        {"role": "system",
         "content": "你是个工具人，生成 5 个用户可能感兴趣的问题，调用 show_related_questions。"},
        {"role": "user", "content": question}
    ]
    if language == 'en':
        messages = [
            {"role": "system",
             "content": "You are a tool person, generate 5 questions that users may be interested in, and call "
                        "show_related_questions."},
            {"role": "user", "content": question}
        ]
    completion = client.chat.completions.create(
        model="gpt-4-1106-preview",
        messages=messages,
        tools=tools
    )
    print(completion.choices[0].message.content)
