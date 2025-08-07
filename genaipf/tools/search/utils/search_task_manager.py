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
from genaipf.tools.search.ai_search.ai_search_openai import ResearchAssistant
from genaipf.tools.search.ai_search.intelligent_search_engine import intelligent_search
import genaipf.utils.sensitive_util as sensitive_utils
import genaipf.utils.common_utils as common_utils
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
    try:
        questions_result = await async_simple_chat(msgs)
        logger.info(f'===========>async_simple_chat介些相关问题的结果是: {questions_result}')
        if questions_result != 'False':
            for question in json.loads(questions_result):
                related_questions.append({"title": question})
            # AIswap用的少，先去掉
            # related_questions.insert(1, fixed_related_question[language])
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
    if enrich_question not in ['False', 'False.']:
        # sources, content = await other_search(enrich_question, related_qa, language)
        multi_search_start_time = time.perf_counter()
        sources, content = await multi_search(enrich_question, related_qa, language)
        multi_search_end_time = time.perf_counter()
        elapsed_multi_search_time = (multi_search_end_time - multi_search_start_time) * 1000
        logger.info(f'=====================>multi_search耗时：{elapsed_multi_search_time:.3f}毫秒')
        need_white_list = False
        try:
            for message in front_messages['messages']:
                if message.get('role', '') == 'user' and (
                        'trustwallet' in message.get('content', '').lower() or 'trust wallet' in message.get('content',
                                                                                                             '').lower()):
                    need_white_list = True
                    break
            if need_white_list:
                new_sources = []
                for i, source in enumerate(sources):
                    url = source['url']
                    url = url[url.find('//') + 2:]
                    url = url[0:url.find('/'):]
                    if url.count('.') > 1:
                        url1 = url[url.rindex('.') + 1:len(url)]
                        tmp = url[0:url.rindex('.')]
                        url = tmp[tmp.rindex('.') + 1:]
                        url = url + '.' + url1
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


async def get_divide_questions(front_messages, language, source, context_length=-4):
    user_messages = front_messages['messages'][context_length:]
    latest_user_msg = user_messages[-1]
    final_question_arr = []
    if source == 'v007':  # 单独处理空投的content
        return []
    else:
        if latest_user_msg.get('quote_info'):
            newest_question = latest_user_msg.get('quote_info')
        else:
            newest_question = latest_user_msg['content']
        final_question_arr.append(newest_question)
    logger.info(f'=====================>获取到的新问题数组是: {final_question_arr}')
    #  TODO 丰富问题先注释掉
    # try:
    #     msgs = LionPromptCommon.get_prompted_messages("divide_user_question", user_messages, language, 2)
    #     questions_result_str = await async_simple_chat(msgs)
    #     logger.info(f'=====================>获取到的新问题数组是: {questions_result_str}')
    #     questions_result = json.loads(questions_result_str)
    #     if questions_result and len(questions_result) != 0:
    #         final_question_arr.extend(questions_result)
    # except Exception as e:
    #     logger.error(f'分析总结用户问题失败: {e}')
    return final_question_arr


# 新的多轮搜索的方法
async def multi_sources_task(front_messages, related_qa, language, source, enrich_questions, search_type):
    enrich_question_start_time = time.perf_counter()
    sources = []
    image_sources = []
    final_related_qa = related_qa
    if enrich_questions and len(enrich_questions) != 0:
        multi_search_start_time = time.perf_counter()
        sources, content, image_sources = await multi_search_new(enrich_questions,search_type, related_qa, language, front_messages)
        multi_search_end_time = time.perf_counter()
        elapsed_multi_search_time = (multi_search_end_time - multi_search_start_time) * 1000
        logger.info(f'=====================>multi_search耗时：{elapsed_multi_search_time:.3f}毫秒')
        need_white_list = False
        try:
            for message in front_messages['messages']:
                if message.get('role', '') == 'user' and (
                        'trustwallet' in message.get('content', '').lower() or 'trust wallet' in message.get('content',
                                                                                                             '').lower()):
                    need_white_list = True
                    break
            if need_white_list:
                new_sources = []
                for i, source in enumerate(sources):
                    url = source['url']
                    url = url[url.find('//') + 2:]
                    url = url[0:url.find('/'):]
                    if url.count('.') > 1:
                        url1 = url[url.rindex('.') + 1:len(url)]
                        tmp = url[0:url.rindex('.')]
                        url = tmp[tmp.rindex('.') + 1:]
                        url = url + '.' + url1
                    if url in WHITE_LIST_URL:
                        new_sources.append(source)
                sources = new_sources
        except Exception as e:
            logger.error(f'白名单识别失败: {e}')
        final_related_qa = content
    get_sources_tasks_end_time = time.perf_counter()
    elapsed_get_sources_tasks_time = (get_sources_tasks_end_time - enrich_question_start_time) * 1000
    logger.info(f'=====================>get_sources_tasks耗时：{elapsed_get_sources_tasks_time:.3f}毫秒')
    return sources, final_related_qa, image_sources


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
    # multi_search_task.append(metaphor_search2(questions, language))
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


async def multi_search_intellgent(questions, search_type, related_qa=[], language=None, front_messages=None):
    search_clients = ['AI_SEARCH']
    # search_clients = ['SERPER']  # 'SERPER' 由于apikey暂时去掉
    question_sources = {}
    image_sources = []
    client1 = GoogleSerperClient()
    for question in questions:
        if not question_sources.get(question):
            question_sources[question] = []
        if search_clients[0] == 'AI_SEARCH': # TODO 特殊处理用于AI-Search
            tmp_question = '用户：'
            for message in front_messages['messages']:
                if message['role'] == 'user':
                    tmp_question += f"{message['content']};"
            search_result, formatted_result = await intelligent_search(front_messages['messages'])
            related_qa.append(tmp_question + ' : ' + formatted_result)
            tmp_sources, image_sources = await client1.multi_search(question, language) 
            question_sources[question] = question_sources[question] + tmp_sources

    results = await parse_results_new(search_result, formatted_result)
    final_sources = []
    if results:
        for question_info in results:
            final_sources.append(question_info['sources'])
            # if search_clients[0] != 'AI_SEARCH':
            #     related_qa.append(question_info['question'] + ' : ' + question_info['content'])
    logger.info(f'================最后的sources===============')
    logger.info(final_sources)
    logger.info(f'================最后的sources===============')
    logger.info(f'================最后的related_qa===============')
    logger.info(related_qa)
    logger.info(f'================最后的related_qa===============')
    return final_sources, related_qa, image_sources


async def multi_search_new(questions, search_type, related_qa=[], language=None, front_messages=None):
    search_clients = ['AI_SEARCH']
    # search_clients = ['SERPER']  # 'SERPER' 由于apikey暂时去掉
    question_sources = {}
    image_sources = []
    for search_client in search_clients:
        if search_client == 'Duckduckgo':
            client = DuckduckgoClient()
        if search_client == 'AI_SEARCH':
            client = ResearchAssistant()
            client1 = GoogleSerperClient()
        else:
            client = GoogleSerperClient()
        for question in questions:
            if not question_sources.get(question):
                question_sources[question] = []
            if search_clients[0] == 'AI_SEARCH': # TODO 特殊处理用于AI-Search
                tmp_question = '用户：'
                for message in front_messages['messages']:
                    if message['role'] == 'user':
                        tmp_question += f"{message['content']};"
                if search_type == 'deep_search':
                    search_result = await client.research_async(tmp_question)
                else:
                    search_result = await intelligent_search(front_messages['messages'])
                related_qa.append(tmp_question + ' : ' + search_result)
                tmp_sources, image_sources = await client1.multi_search(question, language)
                question_sources[question] = question_sources[question] + tmp_sources
            else:
                tmp_sources, image_sources = await client.multi_search(question, language)

                question_sources[question] = question_sources[question] + tmp_sources
    results = await parse_results(question_sources)
    final_sources = []
    if results:
        for question_info in results:
            final_sources += question_info['sources']
            if search_type == 'deep_search':
                related_qa.append(question_info['question'] + ' : ' + question_info['content'])
            # if search_clients[0] != 'AI_SEARCH':
            #     related_qa.append(question_info['question'] + ' : ' + question_info['content'])
    logger.info(f'================最后的sources===============')
    logger.info(final_sources)
    logger.info(f'================最后的sources===============')
    logger.info(f'================最后的related_qa===============')
    logger.info(related_qa)
    logger.info(f'================最后的related_qa===============')
    return final_sources, related_qa, image_sources


async def check_sensitive_words_in_sources(sources):
    checked_sources = []
    for source in sources:
        title = source['title']
        if await sensitive_utils.isNormal(title):
            checked_sources.append(source)
    return checked_sources


async def parse_results(question_sources):
    final_sources = []
    if question_sources:
        for key in question_sources:
            sources = question_sources.get(key)
            title_keys = []
            question_source = []
            question_content = ''
            for source in sources:
                if source['title'] in title_keys:
                    continue
                title_keys.append(source['title'])
                title = source['title']
                url = source['href']
                tmp_content = source['body']
                if await sensitive_utils.isNormal(title) and await sensitive_utils.isNormal(tmp_content):
                    temp_source = {
                        "title": title,
                        "url": url,
                        "content": tmp_content
                    }
                    question_source.append(temp_source)
                    question_content += tmp_content + "\n引用地址" + url + "\n"
            final_sources.append({
                "question": key,
                "sources": question_source,
                "content": question_content
            })

    return final_sources

async def parse_results_new(question_sources, formatted_result):
    final_sources = []
    if question_sources:
        for question_source in question_sources:
            api = question_source.get('api')
            query = question_source.get('query')
            description = question_source.get('description')
            question_content = ''
            sources = {"title": description, "url": api, "content": formatted_result}
     
            question_content += formatted_result + "\n引用来源" + api + "\n"
            final_sources.append({
                "question": query,
                "sources": sources,
                "content": question_content
            })

    return final_sources


async def check_ai_ranking(messages, language, source=''):
    """
    判断用户是否有对Web3行业内容进行排序对比的需求
    
    Args:
        messages: 用户消息历史
        language: 语言 ('zh', 'cn', 'en')
        source: 来源标识
    
    Returns:
        dict: 包含排序需求分析结果的字典
    """
    ranking_data = {
        "need_ranking": False,
        "category": None,
        "keywords": [],
        "ranking_type": None
    }
    try:
        # 获取最新的用户消息
        latest_message = messages['messages'][-1] if messages['messages'] else None
        if not latest_message or latest_message.get('role') != 'user':
            return ranking_data
        # 使用prompt模板判断是否有排序需求
        msgs = LionPromptCommon.get_prompted_messages("check_ai_ranking", messages, language)
        result = await async_simple_chat(msgs, model='gpt-4o')
        
        # 解析返回的JSON结果
        try:
            ranking_result = common_utils.extract_json_from_response(result)
            logger.info(f'AI ranking analysis result: {ranking_result}')
            if not ranking_result:
                return ranking_data
            else:
                ranking_data = ranking_result
            return ranking_data
        except Exception as e:
            logger.error(f'Failed to parse AI ranking result: {e}, result: {result}')
            # 如果解析失败，返回默认结果
            return ranking_data
    except Exception as e:
        logger.error(f'Error in check_ai_ranking: {e}')
        return ranking_data