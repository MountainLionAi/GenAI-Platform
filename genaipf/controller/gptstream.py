import asyncio
from concurrent.futures import ThreadPoolExecutor
import traceback
import openai
from sanic import Request, response
from sanic.response import ResponseStream
from genaipf.exception.customer_exception import CustomerError
from genaipf.constant.error_code import ERROR_CODE
from genaipf.interfaces.common_response import success,fail
import requests
import json
# import snowflake.client
import genaipf.services.gpt_service as gpt_service
from genaipf.controller.preset_entry import preset_entry_mapping, get_swap_preset_info
import genaipf.services.user_account_service_wrapper as user_account_service_wrapper
from datetime import datetime
from genaipf.utils.log_utils import logger
import time
from genaipf.utils.common_utils import get_random_number
from pprint import pprint
from genaipf.dispatcher.api import generate_unique_id, get_format_output, gpt_functions, afunc_gpt_generator, aref_answer_gpt_generator
from genaipf.dispatcher.utils import get_qa_vdb_topk, merge_ref_and_input_text
from genaipf.dispatcher.prompts_v001 import LionPrompt
# from dispatcher.gptfunction import unfiltered_gpt_functions, gpt_function_filter
from genaipf.dispatcher.functions import gpt_functions_mapping, gpt_function_filter, need_tool_agent_l
from genaipf.dispatcher.postprocess import posttext_mapping, PostTextParam
from genaipf.dispatcher.converter import convert_func_out_to_stream, run_tool_agent
from genaipf.utils.redis_utils import RedisConnectionPool
from genaipf.conf.server import IS_INNER_DEBUG, IS_UNLIMIT_USAGE
from genaipf.utils.speech_utils import transcribe, textToSpeech
from genaipf.tools.search.utils.search_agent_utils import other_search
from genaipf.tools.search.utils.search_agent_utils import premise_search, premise_search1, premise_search2, is_need_rag_simple, new_question_question, fixed_related_question, multi_rag
from genaipf.tools.search.utils.search_task_manager import get_related_question_task
from genaipf.utils.common_utils import contains_chinese
from genaipf.utils.sensitive_util import isNormal
from genaipf.dispatcher.model_selection import check_and_pick_model
import ml4gp.services.points_service as points_service
from ml4gp.dispatcher.rag_read import get_answer
import os
import base64
from copy import deepcopy
from genaipf.conf.server import os, AI_ANALYSIS_USE_MODEL
from genaipf.utils.malicious_intent_util import safety_checker
from genaipf.utils import time_utils

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

proxy = { 'https' : '127.0.0.1:8001'}

executor = ThreadPoolExecutor(max_workers=10)

redis_client = RedisConnectionPool().get_connection()

async def http(request: Request):
    return response.json({"http": "sendchat"})


async def http4gpt4(request: Request):
    return response.json({"http4gpt4": "sendchat_gpt4"})

def process_messages(messages):
    processed_messages = []
    previousIsUser = False
    for message in messages:
        if previousIsUser and message['role'] == 'user':
            processed_messages = processed_messages[:-1]
        previousIsUser = message['role'] == 'user'
        shadow_message = {
            "role": message['role'],
            "type": message.get('type', 'text'),
            "format": message.get('format', 'text'),
            "version": message.get('version', 'v001')
        }
        if message.get('type') == 'voice':
            content = transcribe(message['content'])
            need_whisper = True
        elif message.get('type') == 'image':
            shadow_message['base64content'] = message.get('base64content')
            content = message['content']
            need_whisper = False
        elif message.get('type') == 'pdf':
            shadow_message['extra_content'] = message.get('extra_content')
            content = message['content']
            need_whisper = False
        else:
            content = message['content']
            need_whisper = False
        if message.get('quote_info') != '' and message.get('quote_info') is not None:
            shadow_message['quote_info'] = message.get('quote_info')
        shadow_message['need_whisper'] = need_whisper
        shadow_message['content'] = content
        processed_messages.append(shadow_message)
    processed_messages = processed_messages[-11:]
    for message in processed_messages[:]:
        if message['role'] != 'user':
            processed_messages.remove(message)
        else:
            break
    return processed_messages

async def send_stream_chat(request: Request):
    logger.info("======start gptstream===========")

    request_params = request.json
    # if not request_params or not request_params['content'] or not request_params['msggroup']:
    #     raise CustomerError(status_code=ERROR_CODE['PARAMS_ERROR'])

    userid = 0
    if hasattr(request.ctx, 'user'):
        userid = request.ctx.user['id']
    language = request_params.get('language', 'en')
    msggroup = request_params.get('msggroup')
    messages = request_params.get('messages', [])
    device_no = request.remote_addr
    question_code = request_params.get('code', '')
    model = request_params.get('model', '')
    source = request_params.get('source', 'v001')
    chain_id = request_params.get('chain_id', '')
    owner = request_params.get('owner', 'Mlion.ai')
    agent_id = request_params.get('agent_id', None)
    # messages = process_messages(messages)
    output_type = request_params.get('output_type', 'text') # text or voice; (voice is mp3)
    llm_model = request_params.get('llm_model', 'openai') # openai | perplexity | claude
    wallet_type = request_params.get('wallet_type', 'AI')
    visitor_id = request_params.get('visitor_id', '')
    regenerate_response = request_params.get('regenerate_response', None)
    logger_content = f"""
input_params:
userid={userid},language={language},msggroup={msggroup},device_no={device_no},question_code={question_code},model={model},source={source},chain_id={chain_id},owner={owner},agent_id={agent_id},output_type={output_type},llm_model={llm_model},wallet_type={wallet_type},regenerate_response={regenerate_response}
    """
    logger.info(logger_content)

    # messages = [{"role": msg["role"], "content": msg["content"]} for msg in process_messages(messages)]
    # messages = messages[-10:]
    messages = process_messages(messages)
    try:
        # v201、v202 swft移动端，v203 mlion tgbot，v204 external对外开放，v210 swftGpt
        source_list = ['v005','v006','v008','v009','v010','v201','v202','v203','v204','v210']
        if (not IS_UNLIMIT_USAGE and not IS_INNER_DEBUG) and model == 'ml-plus' and source not in source_list:
            _user_id = ''
            if userid != 0:
                _user_id = userid
            can_use = await points_service.check_user_can_use_time(_user_id, visitor_id)
            # can_use = await user_account_service_wrapper.get_user_can_use_time(userid)
            if can_use:
                await points_service.minus_user_can_use_time(_user_id, 'query', visitor_id)
            else:
                return fail(ERROR_CODE['NO_REMAINING_TIMES'])
    except Exception as e:
        logger.error(e)
        logger.error(traceback.format_exc())

    try:
        async def event_generator(_response):
            # async for _str in getAnswerAndCallGpt(request_params['content'], userid, msggroup, language, messages):
            async for _str in getAnswerAndCallGpt(request_params.get('content'), userid, msggroup, language, messages, device_no, question_code, model, output_type, source, owner, agent_id, chain_id, llm_model, wallet_type, regenerate_response):
                await _response.write(f"data:{_str}\n\n")
                await asyncio.sleep(0.01)
        return ResponseStream(event_generator, headers={"accept": "application/json"}, content_type="text/event-stream")

    except Exception as e:
        logger.error(e)
        logger.error(traceback.format_exc())

async def send_chat(request: Request):
    logger.info("======start gptstream===========")

    request_params = request.json
    # if not request_params or not request_params['content'] or not request_params['msggroup']:
    #     raise CustomerError(status_code=ERROR_CODE['PARAMS_ERROR'])

    userid = 0
    if hasattr(request.ctx, 'user'):
        userid = request.ctx.user['id']
    language = request_params.get('language', 'en')
    msggroup = request_params.get('msggroup')
    messages = request_params.get('messages', [])
    device_no = request.remote_addr
    question_code = request_params.get('code', '')
    model = request_params.get('model', '')
    source = request_params.get('source', 'v001')
    owner = request_params.get('owner', 'Mlion.ai')
    agent_id = request_params.get('agent_id', None)
    # messages = process_messages(messages)
    output_type = request_params.get('output_type', 'text') # text or voice; (voice is mp3)
    # messages = [{"role": msg["role"], "content": msg["content"]} for msg in process_messages(messages)]
    # messages = messages[-10:]
    messages = process_messages(messages)
    try:
        # v201、v202 swft移动端，v203 mlion tgbot，v204 external对外开放，v210 swftGpt
        source_list = ['v005', 'v006', 'v008', 'v009', 'v010', 'v201', 'v202', 'v203', 'v204', 'v210']
        if (not IS_UNLIMIT_USAGE and not IS_INNER_DEBUG) and model == 'ml-plus' and source not in source_list:
            _user_id = ''
            if userid != 0:
                _user_id = userid
            can_use = await points_service.check_user_can_use_time(_user_id, visitor_id)
            # can_use = await user_account_service_wrapper.get_user_can_use_time(userid)
            if can_use:
                await points_service.minus_user_can_use_time(_user_id, 'query', visitor_id)
            else:
                return fail(ERROR_CODE['NO_REMAINING_TIMES'])
                raise CustomerError(status_code=ERROR_CODE['NO_REMAINING_TIMES'])
    except Exception as e:
        logger.error(e)
        logger.error(traceback.format_exc())

    try:
        if owner == 'IOS' or owner == "tgbot" or owner == "MountainLion.ai":
            owner = 'Mlion.ai'
        response = await getAnswerAndCallGptData(request_params.get('content'), userid, msggroup, language, messages, device_no, question_code, model, output_type, source, owner, agent_id)
        return response

    except Exception as e:
        logger.error(e)
        logger.error(traceback.format_exc())
   

async def  getAnswerAndCallGpt(question, userid, msggroup, language, front_messages, device_no, question_code, model, output_type, source, owner, agent_id, chain_id, llm_model, wallet_type, regenerate_response):
    from genaipf.dispatcher.stylized_process import stylized_process_mapping
    last_sp_msg = front_messages[-1]
    if last_sp_msg.get("type") in stylized_process_mapping.keys():
        _t = last_sp_msg.get("type")
        last_sp_msg["language"] = language
        last_sp_msg['user_id'] = userid
        g = stylized_process_mapping[_t](last_sp_msg)
        data = {}
        async for _x in g:
            _d = json.loads(_x)
            if _d['role'] == 'preset':
                data = _d['content']
            yield _x
        if question and msggroup :
            gpt_message = (
            question,
            'user',
            userid,
            msggroup,
            question_code,
            device_no,
            None,
            None,
            None,
            None,
            agent_id,
            None
            )
            await gpt_service.add_gpt_message_with_code(gpt_message)
            _code = generate_unique_id()
            data['responseType'] = 0
            data['code'] = _code
            data['chatSerpResults'] = []
            data['chatRelatedResults'] = []
            messageContent = json.dumps(data)
            gpt_message = (
                messageContent,
                data['type'],
                userid,
                msggroup,
                data['code'],
                device_no,
                None,
                None,
                None,
                None,
                agent_id,
                None
            )
            await gpt_service.add_gpt_message_with_code(gpt_message)
        return
    t0 = time.time()
    MAX_CH_LENGTH = 8000
    _ensure_ascii = False
    used_rag = True
    used_graph_rag = False
    messages = []
    picked_content = ""
    isPreSwap = False
    has_image = False
    continue_get_quote = True
    quote_message = ''
    has_sensitive_word = False
    for x in front_messages:
        if continue_get_quote:
            if x.get("quote_info"):
                quote_message = x['quote_info']
                continue_get_quote = False
        if x.get("type") == "image":
            has_image = True
        if x.get("code"):
            del x["code"]
        if x["role"] == "gptfunc":
            messages.append({"role": "assistant", "content": None, "function_call": x["function_call"]})
        else:
            # messages.append({"role": x["role"], "content": x["content"]})
            messages.append(deepcopy(x))
    last_front_msg = front_messages[-1]
    user_history_l = [x["content"] for x in messages if x["role"] == "user"]
    newest_question = user_history_l[-1]
    last_front_msg = front_messages[-1]
    question = last_front_msg['content']

    # 特殊处理IOS移动端问题 tgbot特殊处理owner
    if owner == 'IOS' or owner == "tgbot" or owner == "MountainLion.ai":
        owner = 'Mlion.ai'

    # 初始化rag_status
    rag_status = {
        "usedRag": False,
        "promptAnalysis": {
            "isCompleted": False
        },
        "searchData": {
            "isCompleted": False,
            "totalSources": 0,
            "usedSources": 0,
        },
        "generateAnswer": {
            "isCompleted": False
        }
    }

    language_ = language

    # 判断是否有敏感词汇，更改用户问题、上下文内容。question为存库数据，不需要修改
    if source != 'v004': 
        # 先进行敏感词检查
        is_normal_question = await isNormal(newest_question)
        logger.info(f"userid={userid},is_normal_question={is_normal_question}")
        
        if not is_normal_question:
            # 如果检测到敏感词，直接执行敏感词的处理逻辑
            newest_question = '用户的问题中涉及敏感词汇，明确告知用户他的问题中有敏感词汇，并且不能使用敏感词汇'
            front_messages = [
                {"role": "user", "content": newest_question}
            ]
            messages = [
                {"role": "user", "content": newest_question}
            ]
        else:
            # 只有在没有敏感词的情况下，才进行安全意图检查
            user_messages = [newest_question]
            is_safe = await safety_checker.is_safe_intent(user_messages)
            logger.info(f"userid={userid},is_safe_intent={is_safe}")

            if not is_safe:
                # 根据用户最新输入语言选择不同提示
                if language_ in ['zh', 'cn']:
                    newest_question = '检测到用户的问题包含了一些敏感不适合系统回答的内容。有礼貌地请用户理解，并引导用户重新提出问题。请尝试用更正向的方式提问，或者避免讨论敏感话题。'
                else:
                    newest_question = 'Detected that the user’s question contains sensitive content not suitable for the system to answer. Please politely ask the user for understanding and encourage them to rephrase the question in a more positive manner or avoid discussing sensitive topics.'
                
                front_messages = [
                    {"role": "user", "content": newest_question}
                ]
                messages = [
                    {"role": "user", "content": newest_question}
                ]

    if last_front_msg.get("need_whisper"):
        yield json.dumps(get_format_output("whisper", last_front_msg['content']))
    
    # vvvvvvvv 在第一次 func gpt 就准备好数据 vvvvvvvv
    logger.info(f'>>>>> newest_question: {newest_question}')
    logger.info(f'>>>>>>>>>>>>>>>>>> quote_message: {quote_message}')
    start_time1 = time.perf_counter()
    related_qa = []
    # 钱包客服不走向量数据库
    # if source != 'v005':
    # 临时去掉
    # if source == 'v001':
    #     related_qa.append(await get_answer(source, newest_question, front_messages))
    # else:
    #     related_qa = get_qa_vdb_topk(newest_question, source=source)
    related_qa = get_qa_vdb_topk(newest_question, source=source)
    logger.info(f'===============>使用graphRAG的related_qa是 {related_qa}')
    logger.info(f"userid={userid}, vdb_qa={related_qa}")
    end_time1 = time.perf_counter()
    elapsed_time1 = (end_time1 - start_time1) * 1000
    logger.info(f'=====================>get_qa_vdb_topk耗时：{elapsed_time1:.3f}毫秒')
    # if source == 'v007':  # 空投产品，系统语言不切换
    #     language_ = language
    # else:
    #     language_ = contains_chinese(newest_question)
    # 去掉判断语言逻辑
    language_ = language
    logger.info(f"userid={userid},本次对话语言={language_}")
    _code = generate_unique_id()
    # responseType （0是回答，1是分析）
    responseType = 0
    yield json.dumps(get_format_output("code", _code))
    # 判断最新的问题中是否含有中文
    yield json.dumps(get_format_output("systemLanguage", language_))
    # trustwallet过来的返回msggroup
    if msggroup and msggroup.find('tw_') != -1:
        yield json.dumps(get_format_output("msggroup", msggroup))
    # TODO 速度问题暂时注释掉
    # sources, related_qa, related_questions = await premise_search(newest_question, user_history_l, related_qa)
    # sources, related_qa = await other_search(newest_question, related_qa)
    # sources, related_qa, related_questions = await premise_search1(front_messages, related_qa, language_)
    # logger.info(f'>>>>> other_search sources: {sources}')
    logger.info(f'>>>>> frist related_qa: {related_qa}')
    # yield json.dumps(get_format_output("chatSerpResults", sources))
    # yield json.dumps(get_format_output("chatRelatedResults", related_questions))

    # if len(related_qa) > 0:
    #     used_rag = False
    need_qa = True
    if source == 'v003':
        used_rag = False
        responseType = 1
    # 判断是分析还是回答
    if source == 'v004':
        responseType = 1
    if source == 'v005' or source == 'v006' or source == 'v008' or source == 'v009' or source == 'v010':
        used_rag = False
        need_qa = False
        newest_question = newest_question + f'\nsource 来源信息:{source}'
        logger.info(f">>>>> add source newest_question: {newest_question}")
    if source == 'v009' or source == 'v010':
        used_rag = True
        # used_graph_rag = True
    # 特殊处理swap前置问题
    if source == 'v101':
        source = 'v001'
        isPreSwap = True
        used_rag = False
    if 'type' in last_front_msg and (last_front_msg['type'] == 'image' or last_front_msg['type'] == 'pdf'):
        used_rag = False
        need_qa = False
    yield json.dumps(get_format_output("responseType", responseType))
    logger.info(f"userid={userid},本次对话是否需要用到rag={used_rag}")

    if used_rag:
        is_need_search = is_need_rag_simple(newest_question)
        if is_need_search:
            premise_search2_start_time = time.perf_counter()
            # 问题分析已经完成
            sources_task, related_questions_task = await multi_rag(front_messages, related_qa, language_, source)
            premise_search2_end_time = time.perf_counter()
            elapsed_premise_search2 = (premise_search2_end_time - premise_search2_start_time) * 1000
            logger.info(f'=====================>premise_search2耗时：{elapsed_premise_search2:.3f}毫秒')
    elif used_graph_rag:
        is_need_search = is_need_rag_simple(newest_question)
        sources_task = await get_answer(source, newest_question, front_messages)
    else:
        is_need_search = False
        sources_task = None
        related_questions_task = asyncio.create_task(get_related_question_task({"messages": [front_messages[-1]]}, fixed_related_question, language_))
    logger.info(f"userid={userid},本次对话是否需要用到rag中的检索={is_need_search}")
    _messages = [x for x in messages if x["role"] != "system"]
    msgs = _messages[::]
    # ^^^^^^^^ 在第一次 func gpt 就准备好数据 ^^^^^^^^
    gpt_function_filter_start_time = time.perf_counter()
    used_gpt_functions = gpt_function_filter(gpt_functions_mapping, _messages, source=source)
    logger.info(f"userid={userid},本次对话用到的gpt_functions={used_gpt_functions}")
    gpt_function_filter_end_time = time.perf_counter()
    elapsed_gpt_function_filter_time = (gpt_function_filter_end_time - gpt_function_filter_start_time) * 1000
    logger.info(f'=====================>gpt_function_filter耗时：{elapsed_gpt_function_filter_time:.3f}毫秒')
    _tmp_text = ""
    isPresetTop = False
    data = {
        'type' : 'gpt',
        'content' : _tmp_text
    }
    sources = []
    related_questions = []
    _related_news = []
    if source == 'v004':
        from genaipf.dispatcher.callgpt import DispatcherCallGpt
        _data = {"msgs": msgs, "model": model, "preset_name": "attitude", "source": source, "owner": owner, "llm_model": AI_ANALYSIS_USE_MODEL}
        _tmp_attitude, _related_news = await DispatcherCallGpt.get_subtype_task_result(source, language_, _data)
        yield json.dumps(get_format_output("attitude", _tmp_attitude))
        yield json.dumps(get_format_output("chatRelatedNews", _related_news))
        data["attitude"] = _tmp_attitude
        data["chatRelatedNews"] = _related_news
        picked_content = _tmp_attitude
        if int(picked_content) == 1:
            if language_ == 'zh' or language_ == 'cn':
                picked_content = "这则新闻对Web3行业是利好消息"
            else:
                picked_content = "The news is positive for the Web3 industry"
        else:
            if language_ == 'zh' or language_ == 'cn':
                picked_content = "这则新闻对Web3行业是利空消息"
            else:
                picked_content = "The news is negative for the Web3 industry"
        yield json.dumps(get_format_output("source", "v004"))
        yield json.dumps(get_format_output("gpt", picked_content + '\n'))
        yield json.dumps(get_format_output("gpt", '\n'))
    if source == 'v007':
        airdrop_info = json.loads(newest_question)
        if airdrop_info:
            picked_content = airdrop_info.get('content')
        logger.info(f'=====================>airdrop_picked_content：{picked_content}')
    # 根据用户请求自动分辨使用哪个model
    if llm_model == 'auto':
        llm_model = await check_and_pick_model(newest_question, llm_model)
        logger.info(f"当前使用模型{llm_model}")
        yield json.dumps(get_format_output("model", llm_model))
    afunc_gpt_generator_start_time = time.perf_counter()
    resp1 = await afunc_gpt_generator(msgs, used_gpt_functions, language_, model, picked_content, related_qa, source, owner)
    afunc_gpt_generator_end_time = time.perf_counter()
    elapsed_afunc_gpt_generator_time = (afunc_gpt_generator_end_time - afunc_gpt_generator_start_time) * 1000
    logger.info(f'=====================>afunc_gpt_generator耗时：{elapsed_afunc_gpt_generator_time:.3f}毫秒')
    chunk = await asyncio.wait_for(resp1.__anext__(), timeout=20)
    isvision = False
    func_chunk = None
    if 'role' in chunk and chunk['role'] == 'error':
        yield json.dumps(chunk)
        return
    if chunk["content"] == "llm_yielding":
        route_mode = "text"
        if used_rag and is_need_search:
            rag_status['usedRag'] = True
            rag_status['promptAnalysis']['isCompleted'] = True
            yield json.dumps(get_format_output("rag_status", rag_status))
    else:
        func_chunk = await resp1.__anext__()
        route_mode = "function"
    await resp1.aclose()
    # 特殊处理swap前置问题
    if isPreSwap:
        # 不匹配function
        route_mode = "text"
    if route_mode == "text":
        logger.info(f"userid={userid},本次聊天未触发function")
        if used_rag and is_need_search:
            sources_task_start_time = time.perf_counter()
            sources, related_qa = await sources_task
            rag_status['searchData']['isCompleted'] = True
            rag_status['searchData']['totalSources'] = get_random_number(80, 100)
            rag_status['searchData']['usedSources'] = len(sources) if (sources and len(sources)) else 9
            yield json.dumps(get_format_output("rag_status", rag_status))
            sources_task_end_time = time.perf_counter()
            elapsed_sources_task_time = (sources_task_end_time - sources_task_start_time) * 1000
            logger.info(f'=====================>sources_task耗时：{elapsed_sources_task_time:.3f}毫秒')
            logger.info(f"userid={userid}, 本次聊天rag检索到的网站={sources}")
            logger.info(f"userid={userid},本次聊天rag检索生成的rag_qa={related_qa}")
            # logger.info(f'>>>>> second related_qa: {related_qa}')
            if source != 'v004':
                # yield json.dumps(get_format_output("chatSerpResults", []))  #  TODO 因为敏感词屏蔽RAG来源
                # yield json.dumps(get_format_output("chatSerpResults", sources))
                pass
            else:
                # yield json.dumps(get_format_output("chatSerpResults", []))
                if len(related_qa) == 0:
                    related_qa.append('\n'.join([str(i) for i in _related_news]))
                else:
                    related_qa[0] = '\n'.join([str(i) for i in _related_news])
                yield json.dumps(get_format_output("source", "v004"))
                llm_model = "openai"
        if used_graph_rag and is_need_search:
            sources_task_start_time = time.perf_counter()
            related_qa = [sources_task]
            sources_task_end_time = time.perf_counter()
            elapsed_sources_task_time = (sources_task_end_time - sources_task_start_time) * 1000
            logger.info(f'=====================>sources_task耗时：{elapsed_sources_task_time:.3f}毫秒')
            logger.info(f"userid={userid},本次聊天rag检索生成的rag_qa={related_qa}")
        # if last_front_msg.get('type') == 'image' and last_front_msg.get('base64content') is not None:
        #     msgs = msgs[:-1] + buildVisionMessage(last_front_msg)
        if has_image:
            isvision = True
            used_gpt_functions = None

        aref_answer_gpt_generator_start_time = time.perf_counter()
        resp1 = await aref_answer_gpt_generator(msgs, model, language_, None, picked_content, related_qa, source, owner, isvision, output_type, llm_model, quote_message)
        aref_answer_gpt_generator_end_time = time.perf_counter()
        elapsed_aref_answer_gpt_generator_time = (aref_answer_gpt_generator_end_time - aref_answer_gpt_generator_start_time) * 1000
        logger.info(f'=====================>aref_answer_gpt_generator耗时：{elapsed_aref_answer_gpt_generator_time:.3f}毫秒')
        rag_status['generateAnswer']['isCompleted'] = True
        yield json.dumps(get_format_output("rag_status", rag_status))
        _need_check_text = ''
        async for chunk in resp1:
            if chunk["role"] == "inner_____gpt_whole_text":
                _tmp_text = chunk["content"]
                # if output_type == "voice":
                #     # 对于语音输出，将文本转换为语音并编码
                #     base64_encoded_voice = textToSpeech(_tmp_text)
                #     yield json.dumps(get_format_output("tts", base64_encoded_voice, "voice_mp3_v001"))
            else:
                if chunk["role"] == "gpt":
                    _need_check_text += chunk['content']
                if chunk["role"] != 'tts' and not await isNormal(_need_check_text):
                    logger.info(f'=====================>isNormal _need_check_text:{_need_check_text}')
                    has_sensitive_word = True
                    yield json.dumps(get_format_output("hasSensitiveWord", True))
                    yield json.dumps(get_format_output("step", "done"))
                    _tmp_text = 'response has sensitive word'
                    await resp1.aclose()
                else:
                    yield json.dumps(chunk)
    else:
        try:
            func_name = func_chunk["content"]["func_name"]
            sub_func_name = func_chunk["content"]["sub_func_name"]
            whole_func_name = f"{func_name}_____{sub_func_name}"
            logger.info(f"userid={userid},本次聊天触发function,whole_func_name={whole_func_name}")
            if func_name in need_tool_agent_l or whole_func_name in need_tool_agent_l:
                run_tool_agent_start_time = time.perf_counter()
                stream_gen = run_tool_agent(func_chunk , messages, newest_question, model, language_, related_qa, source, owner, sources, is_need_search, sources_task, chain_id)
                run_tool_agent_end_time = time.perf_counter()
                elapsed_run_tool_agent_time = (run_tool_agent_end_time - run_tool_agent_start_time) * 1000
                logger.info(f'=====================>run_tool_agent耗时：{elapsed_run_tool_agent_time:.3f}毫秒')
            else:
                convert_func_out_to_stream_start_time = time.perf_counter()
                stream_gen = convert_func_out_to_stream(func_chunk , messages, newest_question, model, language_, related_qa, source, owner, sources, is_need_search, sources_task, chain_id, output_type, llm_model, userid, wallet_type)
                convert_func_out_to_stream_time_end_time = time.perf_counter()
                elapsed_convert_func_out_to_stream_time = (convert_func_out_to_stream_time_end_time - convert_func_out_to_stream_start_time) * 1000
                logger.info(f'=====================>convert_func_out_to_stream耗时：{elapsed_convert_func_out_to_stream_time:.3f}毫秒')
        except Exception as e:
            logger.error(f'error: {e} \n func_chunk: {func_chunk}')
            raise e
        await resp1.aclose()
        async for item in stream_gen:
            if item["role"] == "inner_____gpt_whole_text":
                _tmp_text = item["content"]
                # if output_type == "voice":
                #     # 对于语音输出，将文本转换为语音并编码
                #     base64_encoded_voice = textToSpeech(_tmp_text)
                #     yield json.dumps(get_format_output("tts", base64_encoded_voice, "voice_mp3_v001"))
            elif item["role"] == "inner_____preset":
                data.update(item["content"])
            elif item["role"] == "inner_____preset_top":
                isPresetTop = True
                data.update(item["content"])
                data.update({
                    'code' : _code
                })
                _tmp = {
                    "role": "preset", 
                    "type": data["type"], 
                    "format": data["subtype"], 
                    "version": "v001", 
                    "content": data
                }
                yield json.dumps(_tmp)
                from genaipf.dispatcher.callgpt import DispatcherCallGpt
                if DispatcherCallGpt.need_call_gpt(data):
                    # 研报的相关问题前置，不然加载很慢
                    need_qa = False
                    related_questions_task_start_time = time.perf_counter()
                    await related_questions_task
                    related_questions = related_questions_task.result()
                    related_questions_task_end_time = time.perf_counter()
                    elapsed_related_questions_task_time = (related_questions_task_end_time - related_questions_task_start_time) * 1000
                    logger.info(f'=====================>related_questions_task耗时：{elapsed_related_questions_task_time:.3f}毫秒')
                    yield json.dumps(get_format_output("chatRelatedResults", related_questions))

                    subtype_task_result = await DispatcherCallGpt.get_subtype_task_result(data["subtype"], language_, data)
                    preset_type, preset_content, data = DispatcherCallGpt.gen_preset_content(data["subtype"], subtype_task_result, data)
                    yield json.dumps(get_format_output("preset", preset_content, type=preset_type))
            elif item["role"] == "sources":
                sources = item["content"]
            else:
                yield json.dumps(item)

    if source == 'v004':
        _tmp_text = picked_content + "\n" + _tmp_text
    data.update({
        'content' : _tmp_text,
        'code' : _code
    })
    if data["type"] != "gpt" and not isPresetTop:
        _tmp = {
            "role": "preset", 
            "type": data["type"], 
            "format": data["subtype"], 
            "version": "v001", 
            "content": data
        }
        yield json.dumps(_tmp)
    if isPreSwap:
        v101_content = await get_swap_preset_info(language_)
        v101_content['content'].update(
            {
                'content' : _tmp_text,
                'code' : _code
            }
        )
        yield json.dumps(v101_content)
        data = v101_content['content']

    # 把相关问题放到这里 节省执行时间
    logger.info(f"userid={userid},本次对话是否需要qa={need_qa}")
    if not has_sensitive_word: # 如果没有敏感词
        if need_qa:
            related_questions_task_start_time = time.perf_counter()
            if not is_need_search:
                related_questions = []
            else:
                await related_questions_task
                related_questions = related_questions_task.result()
                related_questions_task_end_time = time.perf_counter()
                elapsed_related_questions_task_time = (related_questions_task_end_time - related_questions_task_start_time) * 1000
                logger.info(f'=====================>related_questions_task耗时：{elapsed_related_questions_task_time:.3f}毫秒')
                logger.info(f"userid={userid},related_questions={related_questions}")
            yield json.dumps(get_format_output("chatRelatedResults", related_questions))
        elif not related_questions:
            yield json.dumps(get_format_output("chatRelatedResults", related_questions))
        yield json.dumps(get_format_output("step", "done"))
        logger.info(f'>>>>> userid={userid}, func & ref _tmp_text & output_type: {output_type}: {_tmp_text}')
        base64_type = 0
        base64_content_str = ''
        if last_front_msg.get('type') == 'image':
            base64_type = 1
            base64_content = last_front_msg.get('base64content')
            base64_content_str = ' '.join(base64_content)
        quote_info = last_front_msg.get('quote_info', None)
        file_type = last_front_msg.get('format')
        if question and msggroup :
            gpt_message = (
            question,
            'user',
            userid,
            msggroup,
            question_code,
            device_no,
            base64_type,
            base64_content_str,
            quote_info,
            file_type,
            agent_id,
            regenerate_response
            )
            if not isPreSwap:
                await gpt_service.add_gpt_message_with_code(gpt_message)
            if data['type'] in ['coin_swap', 'wallet_balance', 'token_transfer']:  # 如果是兑换类型，存库时候需要加一个过期字段，前端用于判断不再发起交易
                data['expired'] = True
            # TODO 速度问题暂时注释掉
            if used_rag:
                # data['chatSerpResults'] = [] # TODO 因为敏感词屏蔽RAG来源
                # data['chatSerpResults'] = sources
                data['chatRelatedResults'] = related_questions
            data['responseType'] = responseType
            messageContent = json.dumps(data)
            gpt_message = (
                messageContent,
                data['type'],
                userid,
                msggroup,
                data['code'],
                device_no,
                None,
                None,
                None,
                None,
                agent_id,
                None
            )
            await gpt_service.add_gpt_message_with_code(gpt_message)
    else:
        logger.info(f'>>>>> userid={userid}, query={newest_question}, func & ref _tmp_text & output_type & has sensitive word in response: {output_type}: {_tmp_text}')


async def  getAnswerAndCallGptData(question, userid, msggroup, language, front_messages, device_no, question_code, model, output_type, source, owner, agent_id):
    t0 = time.time()
    MAX_CH_LENGTH = 8000
    _ensure_ascii = False
    messages = []
    for x in front_messages:
        if x.get("code"):
            del x["code"]
        if x["role"] == "gptfunc":
            messages.append({"role": "assistant", "content": None, "function_call": x["function_call"]})
        else:
            messages.append({"role": x["role"], "content": x["content"]})
    user_history_l = [x["content"] for x in messages if x["role"] == "user"]
    newest_question = user_history_l[-1]
    if source in ('v005', 'v006', 'v008', 'v009', 'v010', 'v301'):
        newest_question = newest_question + f'\nsource:{source}'
    last_front_msg = front_messages[-1]
    question = last_front_msg['content']
    
    # vvvvvvvv 在第一次 func gpt 就准备好数据 vvvvvvvv
    logger.info(f'>>>>> newest_question: {newest_question}')
    related_qa = get_qa_vdb_topk(newest_question, source=source)
    # language_ = contains_chinese(newest_question)
    # 判断最新的问题中是否含有中文
    language_ = language
    # TODO 速度问题暂时注释掉
    # sources, related_qa, related_questions = await premise_search(newest_question, user_history_l, related_qa)
    # sources, related_qa = await other_search(newest_question, related_qa)
    # sources, related_qa, related_questions = await premise_search1(front_messages, related_qa, language_)
    # logger.info(f'>>>>> other_search sources: {sources}')
    # logger.info(f'>>>>> frist related_qa: {related_qa}')
    _messages = [x for x in messages if x["role"] != "system"]
    msgs = _messages[::]
    # ^^^^^^^^ 在第一次 func gpt 就准备好数据 ^^^^^^^^
    used_gpt_functions = gpt_function_filter(gpt_functions_mapping, _messages, source=source)
    _tmp_text = ""
    _code = generate_unique_id()
    isPresetTop = False
    data = {
        'type' : 'gpt',
        'content' : _tmp_text
    }
    resp1 = await afunc_gpt_generator(msgs, used_gpt_functions, language_, model, "", related_qa, source, owner)
    chunk = await asyncio.wait_for(resp1.__anext__(), timeout=20)
    assert chunk["role"] == "step"
    if chunk["content"] == "llm_yielding":
        async for chunk in resp1:
            if chunk["role"] == "inner_____gpt_whole_text":
                _tmp_text = chunk["content"]
    elif chunk["content"] == "agent_routing":
        chunk = await resp1.__anext__()
        stream_gen = convert_func_out_to_stream(chunk, messages, newest_question, model, language_, related_qa, source, owner)
        async for item in stream_gen:
            if item["role"] == "inner_____gpt_whole_text":
                _tmp_text = item["content"]
            elif item["role"] == "inner_____preset":
                data.update(item["content"])
            elif item["role"] == "inner_____preset_top":
                isPresetTop = True
                data.update(item["content"])
                data.update({
                    'code' : _code
                })
                _tmp = {
                    "role": "preset", 
                    "type": data["type"], 
                    "format": data["subtype"], 
                    "version": "v001", 
                    "content": data
                }
    await resp1.aclose()
    data.update({
        'content' : _tmp_text,
        'code' : _code
    })
    logger.info(f'>>>>> func & ref _tmp_text & output_type: {output_type}: {_tmp_text}')

    if question and msggroup :
        gpt_message = (
        question,
        'user',
        userid,
        msggroup,
        question_code,
        device_no,
        agent_id,
        None
        )
        await gpt_service.add_gpt_message_with_code(gpt_message)
        if data['type'] == 'coin_swap':  # 如果是兑换类型，存库时候需要加一个过期字段，前端用于判断不再发起交易
            data['expired'] = True
        # TODO 速度问题暂时注释掉
        # data['chatSerpResults'] = sources
        # data['chatRelatedResults'] = related_questions
        messageContent = json.dumps(data)
        gpt_message = (
            messageContent,
            data['type'],
            userid,
            msggroup,
            data['code'],
            device_no,
            agent_id,
            None
        )
        await gpt_service.add_gpt_message_with_code(gpt_message)
    # else :
    #     data['chatSerpResults'] = sources
    #     data['chatRelatedResults'] = related_questions
    
    if source == 'v003':
        return data
    return success(data)
    

def buildVisionMessage(_type_message):
    base64_image = _type_message.get('base64content')
    _message = {
        "role": "user",
        "content": []
    }
    _content_image_url = {
        "type": "image_url",
        "image_url": {
            "url": base64_image
        }
    }
    if _type_message.get('content') is not None and _type_message.get('content') != '':
        _message_question = {
            "type": "text",
            "text": _type_message.get('content')
        }
        _message.get('content').append(_message_question)
    _message.get('content').append(_content_image_url)
    return [_message]
