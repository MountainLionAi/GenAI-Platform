from langchain.agents import AgentExecutor, OpenAIFunctionsAgent
from langchain.schema import SystemMessage
from langchain_community.chat_models import ChatOpenAI
from genaipf.tools.search.metaphor.tools import tools


async def metaphor_search(question: str, language=None):
    """
    question: 问题1
    language: en-英文;zh-中文
    """
    llm = ChatOpenAI(temperature=0)
    content = "你是一个网络研究人员，通过在互联网上查找信息和检索有用文档的内容来回答用户的问题。引用资料来源。"
    if language == 'en':
        content = "You are a web researcher who answers user questions by looking up information on the internet and retrieving contents of helpful documents. Cite your sources."
    system_message = SystemMessage(
        content=content
    )
    agent_prompt = OpenAIFunctionsAgent.create_prompt(system_message)
    agent = OpenAIFunctionsAgent(llm=llm, tools=tools, prompt=agent_prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
    return agent_executor.run(question)
