from langchain.agents import AgentExecutor, OpenAIFunctionsAgent, create_openai_functions_agent
from langchain.schema import SystemMessage
from langchain_openai import ChatOpenAI
from genaipf.tools.search.metaphor.tools import tools
from genaipf.utils.log_utils import logger
from metaphor_python import Metaphor
from genaipf.conf.server import METAPHOR_API_KEY
metaphor = Metaphor(api_key=METAPHOR_API_KEY)

import json
async def metaphor_search(question: str, language=None):
    """
    question: 问题1
    language: en-英文;zh-中文
    """
    llm = ChatOpenAI(temperature=0, model='gpt-4-1106-preview')
    content = "你是一个网络研究人员，通过在互联网上查找信息和检索有用文档的内容来回答用户的问题。引用资料来源。"
    if language == 'en':
        content = "You are a web researcher who answers user questions by looking up information on the internet and retrieving contents of helpful documents. Cite your sources."
    system_message = SystemMessage(
        content=content
    )
    agent_prompt = OpenAIFunctionsAgent.create_prompt(system_message)
    agent = create_openai_functions_agent(llm=llm, tools=tools, prompt=agent_prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
    result = agent_executor.invoke({'input': question})
    try:
        data_p = json.loads(result)
        return data_p['data']['search'], data_p['data']['find_similar'], format_contents(data_p['data']['get_contents'])
    except Exception as e:
        logger.error(str(e))
        return [], [], ''

def format_contents(contents):
    formatted_string = ''
    for index, news_item in enumerate(contents, start=1):
        formatted_string += f"{news_item.extract}\n引用地址: {news_item.url}\n"
    return formatted_string

async def metaphor_search2(question: str):
    search_result = metaphor.search(question, type="keyword" ,num_results=5)
    get_contents_result = metaphor.get_contents(search_result.results[0].id)
    sources = []
    for result in search_result.results:
        sources.append({'title': result.title, 'url': result.url})
    content = format_contents(get_contents_result.contents)
    return sources, content