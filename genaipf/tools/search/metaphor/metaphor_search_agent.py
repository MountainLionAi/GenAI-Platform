import random
from genaipf.utils.log_utils import logger
from genaipf.tools.search.metaphor.metaphor_client import MetaphorClient, include_domains_zh, include_domains_en

def format_contents(contents):
    formatted_string = ''
    for index, news_item in enumerate(contents):
        formatted_string += f"{news_item.extract}\n引用地址: {news_item.url}\n"
    return formatted_string

# dict sources: [{'title': '', 'url': ''}]
# str content
async def other_search(question: str, related_qa=[], language=None):
    # -------- metaphor --------
    sources, metaphor_result = await metaphor_search2(question, language)
    if len(sources) > 0:
        related_qa.append(question + ' : ' + metaphor_result)

    # -------- other --------
    return sources, related_qa

# dict sources: [{'title': '', 'url': ''}]
# str content
async def metaphor_search2(question: str, language=None):
    sources = []
    content = ''
    metaphor_client = MetaphorClient()
    try:
        include_domains = []
        if language == 'zh':
            include_domains.extend(include_domains_zh)
            random_three = random.sample(include_domains_en, 3)
            include_domains.extend(random_three)
            # include_domains.extend(include_domains_en)
        elif language == 'en':
            include_domains.extend(include_domains_en)
        search_result = await metaphor_client.exa_search(question, num_results=5, use_autoprompt=True)
        if search_result and len(search_result.results) != 0:
            for result in search_result.results:
                sources.append({'title': result.title, 'url': result.url})
            ids = [x.id for x in search_result.results]
            content = await metaphor_client.exa_get_contents(ids[:3])
    except Exception as e:
        logger.error(f'metaphor search error: {str(e)}')
    return sources, content