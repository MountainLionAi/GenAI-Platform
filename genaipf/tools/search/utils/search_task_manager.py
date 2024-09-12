import asyncio
import json
from genaipf.conf.server import OPENAI_API_KEY
from genaipf.utils.log_utils import logger
from genaipf.dispatcher.prompts_common import LionPromptCommon
from genaipf.dispatcher.utils import async_simple_chat
from genaipf.tools.search.metaphor.metaphor_search_agent import other_search, metaphor_search2
from genaipf.tools.search.google_serper.goole_serper_client import GoogleSerperClient
from genaipf.tools.search.duckduckgo.ddg_client import DuckduckgoClient
from genaipf.utils.common_utils import aget_multi_coro, sync_to_async
from genaipf.tools.search.google.google_search import google_search
from genaipf.conf.rag_conf import RAG_SEARCH_CLIENT
import genaipf.utils.sensitive_util as sensitive_utils
import time

WHITE_LIST_URL = [
    "trustwallet.com",
    "tokenpocket.pro",
    "tpwallet.io",
    "google.com",
    "binance.com",
    "medium.com",
    "coindesk.com",
    "techflowpost.com",
    "chaincatcher.com"
]


# 获取是否需要查询task
async def get_is_need_search_task(front_messages):
    is_need_search = False
    msgs = LionPromptCommon.get_prompted_messages("if_need_search", front_messages)
    try:
        res = await async_simple_chat(msgs)
        if res in 'True':
            is_need_search = True
    except Exception as e:
        logger.error(f'获取是否需要查询失败: {str(e)}')
    return is_need_search


# 获取相关问题相关task
async def get_related_question_task(newest_question_arr, fixed_related_question, language, source=''):
    related_questions = []
    if source == 'v007':
        return related_questions
    msgs = LionPromptCommon.get_prompted_messages("related_question", newest_question_arr, language)
    # questions_result = await async_simple_chat(msgs, 'gpt-4')
    questions_result = await async_simple_chat(msgs)
    if questions_result != 'False':
        try:
            for question in json.loads(questions_result):
                related_questions.append({"title": question})
            related_questions.insert(1, fixed_related_question[language])
        except Exception as e:
            logger.error(f'解析相关问题失败: {e}')
    return related_questions


# 获取相关source和content的task
async def get_sources_tasks(front_messages, related_qa, language, source):
    enrich_question = 'False'
    enrich_question_start_time = time.perf_counter()
    # msgs = LionPromptCommon.get_prompted_messages("enrich_question", front_messages, language)
    # try:
    #     enrich_question = await async_simple_chat(msgs)
    #     logger.info(f'丰富后的问题是: {enrich_question}')
    # except Exception as e:
    #     logger.error(f'获取丰富后的问题失败: {str(e)}')
    latest_user_msg = front_messages['messages'][-1]
    if latest_user_msg.get('quote_info'):
        enrich_question = latest_user_msg.get('quote_info')
    else:
        enrich_question = latest_user_msg['content']
    if source == 'v007':  # 单独处理空投的content
        airdrop_info = json.loads(latest_user_msg['content'])
        if language == 'zh':
            enrich_question = f'请帮我介绍一下: {airdrop_info.get("title")}这个空投项目'
        else:
            enrich_question = f'Please introduce the {airdrop_info.get("title")} Airdrop Project'
    logger.info(f'丰富后的问题是: {enrich_question}')
    enrich_question_end_time = time.perf_counter()
    elapsed_enrich_question_time = (enrich_question_end_time - enrich_question_start_time) * 1000
    logger.info(f'=====================>enrich_question耗时：{elapsed_enrich_question_time:.3f}毫秒')
    sources = []
    final_related_qa = related_qa
    if enrich_question not in['False', 'False.'] :
        # sources, content = await other_search(enrich_question, related_qa, language)
        multi_search_start_time = time.perf_counter()
        sources, content = await multi_search(enrich_question, related_qa, language)
        multi_search_end_time = time.perf_counter()
        elapsed_multi_search_time = (multi_search_end_time - multi_search_start_time) * 1000
        logger.info(f'=====================>multi_search耗时：{elapsed_multi_search_time:.3f}毫秒')
        need_white_list = False
        try:
            for message in front_messages['messages']:
                if message.get('role', '') == 'user' and ('trustwallet' in message.get('content', '').lower() or 'trust wallet' in message.get('content', '').lower()):
                    need_white_list = True
                    break
            if need_white_list:
                new_sources = []
                for i,source in enumerate(sources):
                    url = source['url']
                    url = url[url.find('//')+2:]
                    url = url[0:url.find('/'):]
                    if url.count('.') > 1:
                        url1 = url[url.rindex('.')+1:len(url)]
                        tmp = url[ 0:url.rindex('.')]
                        url = tmp[tmp.rindex('.')+1:]
                        url = url+'.'+url1
                    if url in WHITE_LIST_URL:
                        new_sources.append(source)
                sources = new_sources
        except Exception as e:
            logger.error(f'白名单识别失败: {e}')
        final_related_qa = content
    get_sources_tasks_end_time = time.perf_counter()
    elapsed_get_sources_tasks_time = (get_sources_tasks_end_time - enrich_question_start_time) * 1000
    logger.info(f'=====================>get_sources_tasks耗时：{elapsed_get_sources_tasks_time:.3f}毫秒')
    return sources, final_related_qa


async def get_divide_questions(front_messages, language, source, context_length=4):
    user_messages = front_messages['messages'][:context_length]
    latest_user_msg = user_messages[-1]
    final_question_arr = []
    if source == 'v007':  # 单独处理空投的content
        airdrop_info = json.loads(latest_user_msg['content'])
        if language == 'zh':
            add_question = f'请帮我介绍一下: {airdrop_info.get("title")}这个空投项目'
        else:
            add_question = f'Please introduce the {airdrop_info.get("title")} Airdrop Project'
        final_question_arr.append(add_question)
    else:
        if latest_user_msg.get('quote_info'):
            newest_question = latest_user_msg.get('quote_info')
        else:
            newest_question = latest_user_msg['content']
        final_question_arr.append(newest_question)
    try:
        msgs = LionPromptCommon.get_prompted_messages("divide_user_question", user_messages, language, 3)
        questions_result_str = await async_simple_chat(msgs)
        logger.info(f'=====================>获取到的新问题数组是: {questions_result_str}')
        questions_result = json.loads(questions_result_str)
        if questions_result and len(questions_result) != 0:
            final_question_arr.extend(questions_result)
    except Exception as e:
        logger.error(f'分析总结用户问题失败: {e}')
    return final_question_arr


# 新的多轮搜索的方法
async def multi_sources_task(front_messages, related_qa, language, source):
    enrich_question_start_time = time.perf_counter()
    enrich_questions = await get_divide_questions(front_messages, language, source)  # 根据上下文生成新的问题数组
    logger.info(f'丰富后的问题是: {enrich_questions}')
    enrich_question_end_time = time.perf_counter()
    elapsed_enrich_question_time = (enrich_question_end_time - enrich_question_start_time) * 1000
    logger.info(f'=====================>enrich_question耗时：{elapsed_enrich_question_time:.3f}毫秒')
    sources = []
    final_related_qa = related_qa
    if enrich_questions and len(enrich_questions) != 0:
        multi_search_start_time = time.perf_counter()
        sources, content = await multi_search_new(enrich_questions, related_qa, language)
        multi_search_end_time = time.perf_counter()
        elapsed_multi_search_time = (multi_search_end_time - multi_search_start_time) * 1000
        logger.info(f'=====================>multi_search耗时：{elapsed_multi_search_time:.3f}毫秒')
        need_white_list = False
        try:
            for message in front_messages['messages']:
                if message.get('role', '') == 'user' and ('trustwallet' in message.get('content', '').lower() or 'trust wallet' in message.get('content', '').lower()):
                    need_white_list = True
                    break
            if need_white_list:
                new_sources = []
                for i,source in enumerate(sources):
                    url = source['url']
                    url = url[url.find('//')+2:]
                    url = url[0:url.find('/'):]
                    if url.count('.') > 1:
                        url1 = url[url.rindex('.')+1:len(url)]
                        tmp = url[ 0:url.rindex('.')]
                        url = tmp[tmp.rindex('.')+1:]
                        url = url+'.'+url1
                    if url in WHITE_LIST_URL:
                        new_sources.append(source)
                sources = new_sources
        except Exception as e:
            logger.error(f'白名单识别失败: {e}')
        final_related_qa = content
    get_sources_tasks_end_time = time.perf_counter()
    elapsed_get_sources_tasks_time = (get_sources_tasks_end_time - enrich_question_start_time) * 1000
    logger.info(f'=====================>get_sources_tasks耗时：{elapsed_get_sources_tasks_time:.3f}毫秒')
    return sources, final_related_qa


# 获取相关 url 摘要
async def get_web_urls_of_msg(front_messages):
    is_need_search = False
    msgs = LionPromptCommon.get_prompted_messages("related_url", front_messages)
    urls_str = await async_simple_chat(msgs)
    related_urls = []
    if "None".lower() in urls_str.lower():
        return related_urls
    try:
        urls = urls_str.strip().strip("https://").split(";")
        related_urls = ["https://" + u for u in urls if u]
    except Exception as e:
        logger.error(f'获取相关 url 摘要失败: {e}')
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
        # summary_str = await async_simple_chat(msgs, model="gpt-4o")
        summary_str = await async_simple_chat(msgs)
        return summary_str
    except Exception as e:
        logger.error(f'获取相关文章摘要失败: {e}')
        return None
    
# 获取分享内容总结
async def get_share_summary(front_messages, language):
    try:
        msgs = LionPromptCommon.get_prompted_messages("share_summary", front_messages, language)
        summary_str = await simple_achat(msgs)
        return summary_str
    except Exception as e:
        logger.error(f'获取分享内容总结失败: {e}')
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
        llm = ChatOpenAI(temperature=0, openai_api_key=openai_api_key, model_name="gpt-4o-mini")
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
            {"role": "user", "content": "btc 最新价格"},
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
    if RAG_SEARCH_CLIENT == 'SERPER':
        google_serper_client = GoogleSerperClient()
        multi_search_task.append(google_serper_client.search(questions))
    elif RAG_SEARCH_CLIENT == 'Duckduckgo':
        ddk_client = DuckduckgoClient()
        multi_search_task.append(ddk_client.aget_results(questions))
    elif RAG_SEARCH_CLIENT == 'GOOGLE_SEARCH':
        # multi_search_task.append(google_search(questions, 1, language, 'https://www.techflowpost.com/'))
        # multi_search_task.append(google_search(questions, 1, language, 'https://foresightnews.pro/'))
        # multi_search_task.append(google_search(questions, 1, language, 'https://www.coindesk.com/'))
        # multi_search_task.append(google_search(questions, 1, language, 'https://www.reddit.com/'))
        # multi_search_task.append(google_search(questions, 1, language, 'https://www.chaincatcher.com/'))
        multi_search_task.append(google_search(questions, 4, language))
    elif RAG_SEARCH_CLIENT == 'ALL':
        google_serper_client = GoogleSerperClient()
        multi_search_task.append(google_serper_client.search(questions))
        multi_search_task.append(google_search(questions, 1, language, 'https://www.coindesk.com/'))
        multi_search_task.append(google_search(questions, 1, language, 'https://www.theblock.co/'))
        multi_search_task.append(google_search(questions, 1, language, 'https://decrypt.co/'))
        multi_search_task.append(google_search(questions, 1, language, 'https://www.reddit.com/'))
        multi_search_task.append(google_search(questions, 1, language, 'https://www.chaincatcher.com/'))
        multi_search_task.append(google_search(questions, 1, language, 'https://www.odaily.news/'))
        multi_search_task.append(google_search(questions, 1, language, 'https://www.panewslab.com/'))
        # multi_search_task.append(google_search(questions))
    #multi_search_task.append(metaphor_search2(questions, language))
    results = await asyncio.gather(*multi_search_task)

    final_sources = []
    final_content = ''
    if len(results) != 0:
        for result in results:
            source_info = result[0]
            source_content = result[1]
            # 检查sources
            checked_sources = await check_sensitive_words_in_sources(source_info)
            final_sources = final_sources + checked_sources
            # 检查内容
            if await sensitive_utils.isNormal(source_content):
                final_content += source_content
    if len(final_sources) > 0:
        related_qa.append(questions + ' : ' + final_content)
    logger.info(f'================最后的sources===============')
    logger.info(final_sources)
    logger.info(f'================最后的sources===============')
    logger.info(f'================最后的related_qa===============')
    logger.info(related_qa)
    logger.info(f'================最后的related_qa===============')
    return final_sources, related_qa


async def multi_search_new(questions, related_qa=[], language=None):
    search_clients = ['Duckduckgo', 'SERPER']
    sources = []
    for search_client in search_clients:
        client = None
        if search_client == 'Duckduckgo':
            client = DuckduckgoClient()
        else:
            client = GoogleSerperClient()
        for question in questions:
            tmp_sources = await client.multi_search(question, language)
            sources.extend(tmp_sources)
    results, content = parse_results(sources)
    final_sources = []
    final_content = ''
    if len(results) != 0:
        for result in results:
            source_info = result[0]
            source_content = result[1]
            # 检查sources
            checked_sources = await check_sensitive_words_in_sources(source_info)
            final_sources = final_sources + checked_sources
            # 检查内容
            if await sensitive_utils.isNormal(source_content):
                final_content += source_content
    if len(final_sources) > 0:
        related_qa.append(questions + ' : ' + final_content)
    logger.info(f'================最后的sources===============')
    logger.info(final_sources)
    logger.info(f'================最后的sources===============')
    logger.info(f'================最后的related_qa===============')
    logger.info(related_qa)
    logger.info(f'================最后的related_qa===============')
    return final_sources, related_qa


async def check_sensitive_words_in_sources(sources):
    checked_sources = []
    for source in sources:
        title = source['title']
        if await sensitive_utils.isNormal(title):
            checked_sources.append(source)
    return checked_sources


def parse_results(results):
    sources = []
    content = ''
    if results and len(results) != 0:
        for result in results:
            sources.append(
                {"title": result["title"], "url": result["href"]}
            )
            content += result["body"] + "\n引用地址" + result["href"] + "\n"

    return sources, content