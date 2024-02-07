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
from genaipf.controller.preset_entry import preset_entry_mapping
import genaipf.services.user_account_service_wrapper as user_account_service_wrapper
from datetime import datetime
from genaipf.utils.log_utils import logger
import time
from pprint import pprint
from genaipf.dispatcher.api import generate_unique_id, get_format_output, gpt_functions, afunc_gpt_generator, aref_answer_gpt_generator
from genaipf.dispatcher.utils import get_qa_vdb_topk, merge_ref_and_input_text
from genaipf.dispatcher.prompts_v001 import LionPrompt
# from dispatcher.gptfunction import unfiltered_gpt_functions, gpt_function_filter
from genaipf.dispatcher.functions import gpt_functions_mapping, gpt_function_filter
from genaipf.dispatcher.postprocess import posttext_mapping, PostTextParam
from genaipf.dispatcher.converter import convert_func_out_to_stream
from genaipf.utils.redis_utils import RedisConnectionPool
from genaipf.conf.server import IS_INNER_DEBUG, IS_UNLIMIT_USAGE
from genaipf.utils.speech_utils import transcribe, textToSpeech
from genaipf.tools.search.utils.search_agent_utils import other_search
from genaipf.tools.search.utils.search_agent_utils import premise_search, premise_search1
from genaipf.utils.common_utils import contains_chinese
import os
import base64
from genaipf.conf.server import os
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

proxy = { 'https' : '127.0.0.1:8001'}

executor = ThreadPoolExecutor(max_workers=10)

async def http(request: Request):
    return response.json({"http": "sendchat"})


async def http4gpt4(request: Request):
    return response.json({"http4gpt4": "sendchat_gpt4"})

def process_messages(messages):
    processed_messages = []
    for message in messages:
        if message.get('type') == 'voice':
            content = transcribe(message['content'])
            need_whisper = True
        else:
            content = message['content']
            need_whisper = False
        processed_messages.append({
            "role": message['role'],
            "content": content,
            "type": message.get('type', 'text'),
            "format": message.get('format', 'text'),
            "version": message.get('version', 'v001'),
            "need_whisper": need_whisper
        })
    return processed_messages[-10:]

async def send_strem_chat(request: Request):
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
    owner = request_params.get('owner', 'MountainLion')
    # messages = process_messages(messages)
    output_type = request_params.get('output_type', 'text') # text or voice; (voice is mp3)
    # messages = [{"role": msg["role"], "content": msg["content"]} for msg in process_messages(messages)]
    # messages = messages[-10:]
    messages = process_messages(messages)
    try:
        if (not IS_UNLIMIT_USAGE and not IS_INNER_DEBUG) and model == 'ml-plus':
            can_use = await user_account_service_wrapper.get_user_can_use_time(userid)
            if can_use > 0:
                await user_account_service_wrapper.minus_one_user_can_use_time(userid)
            else:
                raise CustomerError(status_code=ERROR_CODE['NO_REMAINING_TIMES'])
    except Exception as e:
        logger.error(e)
        logger.error(traceback.format_exc())

    try:
        async def event_generator(_response):
            # async for _str in getAnswerAndCallGpt(request_params['content'], userid, msggroup, language, messages):
            async for _str in getAnswerAndCallGpt(request_params.get('content'), userid, msggroup, language, messages, device_no, question_code, model, output_type, owner):
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
    owner = request_params.get('owner', 'MountainLion')
    # messages = process_messages(messages)
    output_type = request_params.get('output_type', 'text') # text or voice; (voice is mp3)
    # messages = [{"role": msg["role"], "content": msg["content"]} for msg in process_messages(messages)]
    # messages = messages[-10:]
    messages = process_messages(messages)
    try:
        if (not IS_UNLIMIT_USAGE and not IS_INNER_DEBUG) and model == 'ml-plus':
            can_use = await user_account_service_wrapper.get_user_can_use_time(userid)
            if can_use > 0:
                await user_account_service_wrapper.minus_one_user_can_use_time(userid)
            else:
                raise CustomerError(status_code=ERROR_CODE['NO_REMAINING_TIMES'])
    except Exception as e:
        logger.error(e)
        logger.error(traceback.format_exc())

    try:
        response = await getAnswerAndCallGptData(request_params.get('content'), userid, msggroup, language, messages, device_no, question_code, model, output_type, source, owner)
        return response

    except Exception as e:
        logger.error(e)
        logger.error(traceback.format_exc())
   

async def  getAnswerAndCallGpt(question, userid, msggroup, language, front_messages, device_no, question_code, model, output_type, owner):
    t0 = time.time()
    MAX_CH_LENGTH = 8000
    _ensure_ascii = False
    messages = []
    source = 'v001'
    for x in front_messages:
        if x.get("code"):
            del x["code"]
        if x["role"] == "gptfunc":
            messages.append({"role": "assistant", "content": None, "function_call": x["function_call"]})
        else:
            messages.append({"role": x["role"], "content": x["content"]})
    user_history_l = [x["content"] for x in messages if x["role"] == "user"]
    newest_question = user_history_l[-1]
    
    last_front_msg = front_messages[-1]
    question = last_front_msg['content']
    if last_front_msg.get("need_whisper"):
        yield json.dumps(get_format_output("whisper", last_front_msg['content']))
    
    # vvvvvvvv 在第一次 func gpt 就准备好数据 vvvvvvvv
    logger.info(f'>>>>> newest_question: {newest_question}')
    related_qa = get_qa_vdb_topk(newest_question)
    language_ = contains_chinese(newest_question)
    # 判断最新的问题中是否含有中文
    yield json.dumps(get_format_output("systemLanguage", language_))
    # TODO 速度问题暂时注释掉
    # sources, related_qa, related_questions = await premise_search(newest_question, user_history_l, related_qa)
    # sources, related_qa = await other_search(newest_question, related_qa)
    sources, related_qa, related_questions = await premise_search1(front_messages, related_qa, language_)
    logger.info(f'>>>>> other_search sources: {sources}')
    logger.info(f'>>>>> frist related_qa: {related_qa}')
    yield json.dumps(get_format_output("chatSerpResults", sources))
    yield json.dumps(get_format_output("chatRelatedResults", related_questions))
    _messages = [x for x in messages if x["role"] != "system"]
    msgs = _messages[::]
    # ^^^^^^^^ 在第一次 func gpt 就准备好数据 ^^^^^^^^
    used_gpt_functions = gpt_function_filter(gpt_functions_mapping, _messages)
    _tmp_text = ""
    _code = generate_unique_id()
    isPresetTop = False
    data = {
        'type' : 'gpt',
        'content' : _tmp_text
    }
    resp1 = await afunc_gpt_generator(msgs, used_gpt_functions, language, model, "", related_qa, source, owner)
    chunk = await asyncio.wait_for(resp1.__anext__(), timeout=20)
    assert chunk["role"] == "step"
    if chunk["content"] == "llm_yielding":
        async for chunk in resp1:
            if chunk["role"] == "inner_____gpt_whole_text":
                _tmp_text = chunk["content"]
            else:
                yield json.dumps(chunk)
    elif chunk["content"] == "agent_routing":
        chunk = await resp1.__anext__()
        stream_gen = convert_func_out_to_stream(chunk, messages, newest_question, model, language, related_qa, source, owner)
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
                yield json.dumps(_tmp)
            else:
                yield json.dumps(item)

    if output_type == "voice":
        # 对于语音输出，将文本转换为语音并编码
        base64_encoded_voice = textToSpeech(_tmp_text)
        yield json.dumps(get_format_output("tts", base64_encoded_voice, "voice_mp3_v001"))
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
    yield json.dumps(get_format_output("step", "done"))
    logger.info(f'>>>>> func & ref _tmp_text & output_type: {output_type}: {_tmp_text}')

    if question and msggroup :
        gpt_message = (
        question,
        'user',
        userid,
        msggroup,
        question_code,
        device_no
        )
        await gpt_service.add_gpt_message_with_code(gpt_message)
        if data['type'] == 'coin_swap':  # 如果是兑换类型，存库时候需要加一个过期字段，前端用于判断不再发起交易
            data['expired'] = True
        # TODO 速度问题暂时注释掉
        data['chatSerpResults'] = sources
        data['chatRelatedResults'] = related_questions
        messageContent = json.dumps(data)
        gpt_message = (
            messageContent,
            data['type'],
            userid,
            msggroup,
            data['code'],
            device_no
        )
        await gpt_service.add_gpt_message_with_code(gpt_message)


async def  getAnswerAndCallGptData(question, userid, msggroup, language, front_messages, device_no, question_code, model, output_type, source, owner):
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
    
    last_front_msg = front_messages[-1]
    question = last_front_msg['content']
    
    # vvvvvvvv 在第一次 func gpt 就准备好数据 vvvvvvvv
    logger.info(f'>>>>> newest_question: {newest_question}')
    related_qa = get_qa_vdb_topk(newest_question)
    # TODO 速度问题暂时注释掉
    # sources, related_qa, related_questions = await premise_search(newest_question, user_history_l, related_qa)
    # sources, related_qa = await other_search(newest_question, related_qa)
    sources, related_qa, related_questions = await premise_search1(front_messages, related_qa)
    logger.info(f'>>>>> other_search sources: {sources}')
    logger.info(f'>>>>> frist related_qa: {related_qa}')
    _messages = [x for x in messages if x["role"] != "system"]
    msgs = _messages[::]
    # ^^^^^^^^ 在第一次 func gpt 就准备好数据 ^^^^^^^^
    used_gpt_functions = gpt_function_filter(gpt_functions_mapping, _messages)
    _tmp_text = ""
    _code = generate_unique_id()
    isPresetTop = False
    data = {
        'type' : 'gpt',
        'content' : _tmp_text
    }
    resp1 = await afunc_gpt_generator(msgs, used_gpt_functions, language, model, "", related_qa, source, owner)
    chunk = await asyncio.wait_for(resp1.__anext__(), timeout=20)
    assert chunk["role"] == "step"
    if chunk["content"] == "llm_yielding":
        async for chunk in resp1:
            if chunk["role"] == "inner_____gpt_whole_text":
                _tmp_text = chunk["content"]
    elif chunk["content"] == "agent_routing":
        chunk = await resp1.__anext__()
        stream_gen = convert_func_out_to_stream(chunk, messages, newest_question, model, language, related_qa, source, owner)
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
        device_no
        )
        await gpt_service.add_gpt_message_with_code(gpt_message)
        if data['type'] == 'coin_swap':  # 如果是兑换类型，存库时候需要加一个过期字段，前端用于判断不再发起交易
            data['expired'] = True
        # TODO 速度问题暂时注释掉
        data['chatSerpResults'] = sources
        data['chatRelatedResults'] = related_questions
        messageContent = json.dumps(data)
        gpt_message = (
            messageContent,
            data['type'],
            userid,
            msggroup,
            data['code'],
            device_no
        )
        await gpt_service.add_gpt_message_with_code(gpt_message)
    else :
        data['chatSerpResults'] = sources
        data['chatRelatedResults'] = related_questions
    
    return success(data)
    

