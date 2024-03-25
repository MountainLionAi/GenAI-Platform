import json
from genaipf.utils.log_utils import logger
from genaipf.dispatcher.prompts_common import LionPromptCommon
from genaipf.dispatcher.utils import simple_achat
from genaipf.tools.search.metaphor.metaphor_search_agent import other_search


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
        sources, content = await other_search(enrich_question, related_qa, language)
        final_related_qa = content
    return sources, final_related_qa


# 获取相关 url 摘要
async def get_web_summary_of_msg(front_messages):
    is_need_search = False
    msgs = LionPromptCommon.get_prompted_messages("related_url", front_messages)
    urls_str = await simple_achat(msgs)
    related_urls = []
    if urls_str != 'False':
        try:
            for u in json.loads(urls_str):
                related_urls.append("https://" + u.strip("https://"))
        except Exception as e:
            logger.error(f'解析相关问题失败: {e}')
    return related_urls
        
        