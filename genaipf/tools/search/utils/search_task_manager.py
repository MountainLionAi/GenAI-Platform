import asyncio
import json
from genaipf.conf.server import OPENAI_API_KEY
from genaipf.utils.log_utils import logger
from genaipf.dispatcher.prompts_common import LionPromptCommon
from genaipf.dispatcher.utils import simple_achat
from genaipf.tools.search.metaphor.metaphor_search_agent import other_search, metaphor_search2
from genaipf.tools.search.google_serper.goole_serper_client import GoogleSerperClient
from genaipf.utils.common_utils import aget_multi_coro, sync_to_async


# 获取是否需要查询task
async def get_is_need_search_task(front_messages):
    is_need_search = False
    msgs = LionPromptCommon.get_prompted_messages("if_need_search", front_messages)
    try:
        res = await simple_achat(msgs)
        if res in 'True':
            is_need_search = True
    except Exception as e:
        logger.error(f'获取是否需要查询失败: {str(e)}')
    return is_need_search


# 获取相关问题相关task
async def get_related_question_task(newest_question_arr, fixed_related_question, language):
    msgs = LionPromptCommon.get_prompted_messages("related_question", newest_question_arr, language)
    questions_result = await simple_achat(msgs)
    related_questions = []
    if questions_result != 'False':
        try:
            for question in json.loads(questions_result):
                related_questions.append({"title": question})
            related_questions.insert(1, fixed_related_question[language])
        except Exception as e:
            logger.error(f'解析相关问题失败: {e}')
    return related_questions


# 获取相关source和content的task
async def get_sources_tasks(front_messages, related_qa, language):
    enrich_question = 'False'
    msgs = LionPromptCommon.get_prompted_messages("enrich_question", front_messages)
    try:
        enrich_question = await simple_achat(msgs)
        logger.info(f'丰富后的问题是: {enrich_question}')
    except Exception as e:
        logger.error(f'获取丰富后的问题失败: {str(e)}')
    sources = []
    final_related_qa = related_qa
    if enrich_question != 'False':
        # sources, content = await other_search(enrich_question, related_qa, language)
        sources, content = await multi_search(enrich_question, related_qa, language)
        final_related_qa = content
    return sources, final_related_qa


# 获取相关 url 摘要
async def get_web_urls_of_msg(front_messages):
    is_need_search = False
    msgs = LionPromptCommon.get_prompted_messages("related_url", front_messages)
    urls_str = await simple_achat(msgs)
    related_urls = []
    if "None".lower() in urls_str.lower():
        return related_urls
    try:
        urls = urls_str.strip().strip("https://").split(";")
        related_urls = ["https://" + u for u in urls if u]
    except Exception as e:
        logger.error(f'解析相关问题失败: {e}')
    # if urls_str != 'False':
    #     try:
    #         for u in json.loads(urls_str):
    #             related_urls.append("https://" + u.strip("https://"))
    #     except Exception as e:
    #         logger.error(f'解析相关问题失败: {e}')
    return related_urls


# 获取相关文章摘要
async def get_article_summary(front_messages):
    '''
    {
        "messages": [],
        "article_text": "xxx"
    }
    '''
    try:
        msgs = LionPromptCommon.get_prompted_messages("summary_page_by_msg", front_messages)
        # summary_str = await simple_achat(msgs, model="gpt-4-1106-preview")
        summary_str = await simple_achat(msgs)
        return summary_str
    except Exception as e:
        logger.error(f'解析相关问题失败: {e}')
        return None


async def aload_web(url):
    try:
        # print(f"url: {url}")
        from langchain.chains.summarize import load_summarize_chain
        from langchain_community.document_loaders import WebBaseLoader
        from langchain_openai import ChatOpenAI
        loader = WebBaseLoader(url)
        aload = sync_to_async(loader.load)
        res = await aload()
        openai_api_key = OPENAI_API_KEY
        llm = ChatOpenAI(temperature=0, openai_api_key=openai_api_key, model_name="gpt-3.5-turbo-0125")
        chain = load_summarize_chain(llm, chain_type="stuff")
        res = await chain.arun(res)
        return res
    except Exception as e:
        logger.error(f'aload_web: {e}')
        return None


async def summarize_urls(urls, timeout=10.1):
    res = await aget_multi_coro(aload_web, urls, 10, timeout)
    return res


async def get_web_summary_of_msg(front_messages, timeout=10.1):
    urls = await get_web_urls_of_msg(front_messages)
    urls = [[u] for u in urls]
    res = await summarize_urls(urls, timeout)
    return res


async def aload_web_by_msgs(url, msgs):
    """
    msgs: {"messages": [
            {"role": "user", "content": "swftc 最新价格"},
        ]}
    """
    try:
        # print(f"url: {url}")
        from langchain.chains.summarize import load_summarize_chain
        from langchain_community.document_loaders import WebBaseLoader
        from langchain_openai import ChatOpenAI
        loader = WebBaseLoader(url)
        aload = sync_to_async(loader.load)
        res = await aload()
        data = {"messages": msgs["messages"], "article_text": res}
        res = await get_article_summary(data)
        return res
    except Exception as e:
        logger.error(f'aload_web: {e}')
        return None


async def summarize_urls_by_msg(urls_and_msgs, timeout=10.1):
    res = await aget_multi_coro(aload_web_by_msgs, urls_and_msgs, 10, timeout)
    return res


async def multi_search(questions: str, related_qa=[], language=None):
    multi_search_task = []
    google_serper_client = GoogleSerperClient()
    multi_search_task.append(google_serper_client.search(questions))
    multi_search_task.append(metaphor_search2(questions, language))
    results = await asyncio.gather(*multi_search_task)

    final_sources = []
    final_content = ''
    if len(results) != 0:
        for result in results:
            final_sources = final_sources + result[0]
            final_content += result[1]
    if len(final_sources) > 0:
        related_qa.append(questions + ' : ' + final_content)
    return final_sources, related_qa
