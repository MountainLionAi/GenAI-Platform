from genaipf.utils.log_utils import logger
from metaphor_python import Metaphor
from genaipf.utils.common_utils import sync_to_async

from genaipf.conf.server import METAPHOR_API_KEY
from genaipf.tools.search.metaphor.metaphor_client import MetaphorClient

def format_contents(contents):
    formatted_string = ''
    for index, news_item in enumerate(contents):
        formatted_string += f"{news_item.extract}\n引用地址: {news_item.url}\n"
    return formatted_string

# dict sources: [{'title': '', 'url': ''}]
# str content
async def other_search(question: str, related_qa=[]):
    # -------- metaphor --------
    sources, metaphor_result = await metaphor_search2(question)
    if len(sources) > 0:
        related_qa.append(question + ' : ' + metaphor_result)

    # -------- other --------
    return sources, related_qa

# dict sources: [{'title': '', 'url': ''}]
# str content
async def metaphor_search2(question: str):
    sources = []
    content = ''
    metaphor_client = MetaphorClient()
    try:
        search_result = await metaphor_client.exa_search(question, num_results=5, use_autoprompt=True)
        for result in search_result.results:
            sources.append({'title': result.title, 'url': result.url})
        ids = [x.id for x in search_result.results]
        content = await metaphor_client.exa_get_contents(ids[:3])
    except Exception as e:
        logger.error(f'metaphor search error: {str(e)}')
    return sources, content