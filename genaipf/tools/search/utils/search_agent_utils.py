from genaipf.tools.search.metaphor import metaphor_search_agent


# dict sources: [{'title': '', 'url': ''}]
# str content
async def other_search(question: str, related_qa=[], language=None):
    # -------- metaphor --------
    sources, metaphor_result = await metaphor_search_agent.metaphor_search2(question)
    if len(sources) > 0:
        related_qa.append(question + ' : ' + metaphor_result)

    # -------- other --------
    return sources, related_qa
