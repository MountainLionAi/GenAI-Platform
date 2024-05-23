import os
from genaipf.conf.server import GOOGLE_SERPER_API_KEY
os.environ["SERPER_API_KEY"] = GOOGLE_SERPER_API_KEY 
from langchain_community.utilities import GoogleSerperAPIWrapper
from typing_extensions import Literal
from genaipf.utils.common_utils import sync_to_async
from genaipf.utils.log_utils import logger
import asyncio

async def google_serper(question, type="search", k=5):
    type: Literal["news", "search", "places", "images"] = "search"
    search = GoogleSerperAPIWrapper(type=type)
    cleint = sync_to_async(search.results)
    try:
        results = await cleint(question)
        return parse_snippets(results, type, k)
    except Exception as e:
        logger.error("Google serper error")
        return [], ''

def parse_snippets(results, type, k):
    result_key_for_type = {
        "news": "news",
        "places": "places",
        "images": "images",
        "search": "organic",
    }
    sources = []
    content = ""

    if type not in result_key_for_type:
        logger.error("error type for serper tools")
        return sources, content
    
    if results.get("answerBox"):
        answer_box = results.get("answerBox", {})
        if answer_box.get("answer"):
            content += answer_box.get("answer")
        elif answer_box.get("snippet"):
            content += answer_box.get("snippet").replace("\n", " ")
        elif answer_box.get("snippetHighlighted"):
            content += answer_box.get("snippetHighlighted")
        content += "\n"

    # if results.get("knowledgeGraph"):
    #     kg = results.get("knowledgeGraph", {})
    #     title = kg.get("title")
    #     entity_type = kg.get("type")
    #     if entity_type:
    #         snippets.append(f"{title}: {entity_type}.")
    #     description = kg.get("description")
    #     if description:
    #         snippets.append(description)
    #     for attribute, value in kg.get("attributes", {}).items():
    #         snippets.append(f"{title} {attribute}: {value}.")

    for result in results[result_key_for_type[type]][: k]:
        if "snippet" in result:
            sources.append(
                {"title":result["title"], "url":result["link"]}
            )
            content += result["snippet"] + "\n引用地址" + result["link"] + "\n"
        # for attribute, value in result.get("attributes", {}).items():
        #     snippets.append(f"{attribute}: {value}.")

    return sources, content

# asyncio.run(google_serper("perdict btc price"))
