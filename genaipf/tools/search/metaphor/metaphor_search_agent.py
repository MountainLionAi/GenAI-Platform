from genaipf.utils.log_utils import logger
from metaphor_python import Metaphor
from genaipf.conf.server import METAPHOR_API_KEY
metaphor = Metaphor(api_key=METAPHOR_API_KEY)

def format_contents(contents):
    sources = []
    formatted_string = ''
    for index, news_item in enumerate(contents):
        if index < 3:
            formatted_string += f"{news_item.extract}\n引用地址: {news_item.url}\n"
        sources.append({"title": news_item.title, "url": news_item.url})
    return sources, formatted_string

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
        search_result = metaphor.search(question, type="keyword" ,num_results=5)
        ids = [x.id for x in search_result.results]
        get_contents_result = metaphor.get_contents(ids)
        for result in search_result.results:
            sources.append({'title': result.title, 'url': result.url})
        content = format_contents(get_contents_result.contents)
    except Exception as e:
        logger.error(f'metaphor search error: {str(e)}')
    return sources, content