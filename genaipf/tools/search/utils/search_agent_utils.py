from genaipf.tools.search.metaphor import metaphor_search_agent
from genaipf.dispatcher.api import generate_unique_id, get_format_output, gpt_functions, afunc_gpt_generator


# dict sources: [{'title': '', 'url': ''}]
# str content
async def other_search(question: str, related_qa=[], language=None):
    # -------- metaphor --------
    sources, metaphor_result = await metaphor_search_agent.metaphor_search2(question)
    if len(sources) > 0:
        related_qa.append(question + ' : ' + metaphor_result)

    # -------- other --------
    return sources, related_qa


async def related_search(question: str, model: str, language=None, related_qa=[]):
    resp1 = await afunc_gpt_generator([question], gpt_functions, language, model, "", related_qa)
    print(resp1)
