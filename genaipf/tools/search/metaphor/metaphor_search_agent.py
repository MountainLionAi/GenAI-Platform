from genaipf.utils.log_utils import logger
from metaphor_python import Metaphor
from genaipf.utils.common_utils import sync_to_async

from genaipf.conf.server import METAPHOR_API_KEY
metaphor = Metaphor(api_key=METAPHOR_API_KEY)
search_of_metaphor = sync_to_async(metaphor.search)
aget_contents_of_metaphor = sync_to_async(metaphor.get_contents)

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
    try:
        search_result = await search_of_metaphor(question, num_results=5, use_autoprompt=True)
        ids = [x.id for x in search_result.results]
        get_contents_result = await aget_contents_of_metaphor(ids[:3])
        for result in search_result.results:
            sources.append({'title': result.title, 'url': result.url})
        content = format_contents(get_contents_result.contents)
    except Exception as e:
        logger.error(f'metaphor search error: {str(e)}')
    return sources, content