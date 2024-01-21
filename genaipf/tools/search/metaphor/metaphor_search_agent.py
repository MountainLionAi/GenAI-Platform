from langchain.agents import AgentExecutor, OpenAIFunctionsAgent, create_openai_functions_agent
from langchain.schema import SystemMessage
from langchain_openai import ChatOpenAI
from genaipf.tools.search.metaphor.tools import tools
from genaipf.utils.log_utils import logger
import json
async def metaphor_search(question: str, language=None):
    """
    question: 问题1
    language: en-英文;zh-中文
    """
    llm = ChatOpenAI(temperature=0, model='gpt-4')
    question += " 将metaphor的search执行的5个结果参考{'search': [{'title': '', 'url': '', 'publishedDate': '', 'extract': '', 'author': ''}]}格式，find_similar执行的5个结果参考{'find_similar': [{'title': '', 'url': '', 'publishedDate': '', 'extract': '', 'author': ''}]}格式，get_contents执行的1个结果参考{'get_contents': [{'title': '', 'url': '', 'publishedDate': '', 'extract': '', 'author': ''}]}格式，并且将title，extract属性翻译成中文，返回例如: {'data': {'search': [],'find_similar': [],'get_contents': []}}格式的json字符串。"
    content = "你是一个网络研究人员，通过在互联网上查找信息和检索有用文档的内容来回答用户的问题。引用资料来源。"
    if language == 'en':
        content = "You are a web researcher who answers user questions by looking up information on the internet and retrieving contents of helpful documents. Cite your sources."
        question += " Return a JSON string in the format: {'data': {'search': [], 'find_similar': [], 'get_contents': []}}, with references to the results of the 'search' operation in the format {'search': [{'title': '', 'url': '', 'publishedDate': '', 'extract': '', 'author': ''}]}, the 'find_similar' operation in the format {'find_similar': [{'title': '', 'url': '', 'publishedDate': '', 'extract': '', 'author': ''}]}, and the 'get_contents' operation in the format {'get_contents': [{'title': '', 'url': '', 'publishedDate': '', 'extract': '', 'author': ''}]}. For example: {'data': {'search': [], 'find_similar': [], 'get_contents': []}}."
    system_message = SystemMessage(
        content=content
    )
    agent_prompt = OpenAIFunctionsAgent.create_prompt(system_message)
    agent = OpenAIFunctionsAgent(llm=llm, tools=tools, prompt=agent_prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
    result = agent_executor.run(question)
    try:
        data_p = json.loads(result)
        return data_p['data']['search'], data_p['data']['find_similar'], format_contents(data_p['data']['get_contents'])
    except Exception as e:
        logger.error(str(e))
        return [], [], ''

def format_contents(contents):
    formatted_string = ''
    for index, news_item in enumerate(contents, start=1):
        formatted_string += f"{index}. {news_item['extract']}\n引用地址: {news_item['url']}\n"
    return formatted_string
