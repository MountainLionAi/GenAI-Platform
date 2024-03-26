import os
from genaipf.conf.server import GOOGLE_SERPER_API_KEY
os.environ["SERPER_API_KEY"] = GOOGLE_SERPER_API_KEY 
from langchain_community.utilities import GoogleSerperAPIWrapper
from typing_extensions import Literal

async def google_serper(question, type="search", k=5):
    type: Literal["news", "search", "places", "images"] = "search"
    search = GoogleSerperAPIWrapper(type=type)
    results = search.results(question)
    return parse_snippets(results, type, k)   

def parse_snippets(results, type, k):
    result_key_for_type = {
        "news": "news",
        "places": "places",
        "images": "images",
        "search": "organic",
    }
    resp = {}
    snippets = []
    if results.get("answerBox"):
        answer_box = results.get("answerBox", {})
        if answer_box.get("answer"):
            resp["answer"] = answer_box.get("answer")
        elif answer_box.get("snippet"):
            resp["snippet"] = answer_box.get("snippet").replace("\n", " ")
        elif answer_box.get("snippetHighlighted"):
            resp["snippetHighlighted"] = answer_box.get("snippetHighlighted")

    if results.get("knowledgeGraph"):
        kg = results.get("knowledgeGraph", {})
        title = kg.get("title")
        entity_type = kg.get("type")
        if entity_type:
            snippets.append(f"{title}: {entity_type}.")
        description = kg.get("description")
        if description:
            snippets.append(description)
        for attribute, value in kg.get("attributes", {}).items():
            snippets.append(f"{title} {attribute}: {value}.")

    for result in results[result_key_for_type[type]][: k]:
        if "snippet" in result:
            snippets.append(
                f"Title:{result['title']}\nSnippet:{result['snippet']}\nLink:{result['link']}\n"
            )
        for attribute, value in result.get("attributes", {}).items():
            snippets.append(f"{attribute}: {value}.")
    if len(snippets) == 0:
        snippets = ""
    resp["snippets"] = snippets
    return resp

