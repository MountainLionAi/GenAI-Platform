from langchain.agents import tool
from metaphor_python import Metaphor
from genaipf.conf.server import METAPHOR_API_KEY, OPENAI_API_KEY

metaphor = Metaphor(api_key=METAPHOR_API_KEY)


@tool
def search(query: str):
    """Search for a webpage based on the query."""
    return metaphor.search(f"{query}", use_autoprompt=True, num_results=5)


@tool
def find_similar(url: str):
    """Search for webpages similar to a given URL.
    The url passed in should be a URL returned from `search`.
    """
    return metaphor.find_similar(url, num_results=5)


@tool
def get_contents(ids: list[str]):
    """Get the contents of a webpage.
    The ids passed in should be a list of ids returned from `search`.
    """
    return metaphor.get_contents(ids)


tools = [search, get_contents, find_similar]