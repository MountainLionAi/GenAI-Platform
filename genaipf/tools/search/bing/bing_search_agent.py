from dotenv import load_dotenv
from langchain_community.utilities import BingSearchAPIWrapper

load_dotenv(override=True)


async def bing_search(question: str):
    """
    question: 问题
    """
    search = BingSearchAPIWrapper()
    return search.run(question)
