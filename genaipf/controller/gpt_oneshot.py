import asyncio
import traceback
import json
from typing import Mapping
import openai
from sanic import Request, response
from sanic.response import ResponseStream
from genaipf.conf.server import os, IS_INNER_DEBUG
from genaipf.utils.log_utils import logger
from genaipf.constant.error_code import ERROR_CODE
from genaipf.interfaces.common_response import success, fail
from genaipf.dispatcher.api import aref_oneshot_gpt_generator
async def send_oneshot_chat(request: Request):
    '''
    messages: [
        {'role': 'user_a', 'content': 'how are you?', 'type': 'text', 'format': 'text', 'version': 'v001'},
        {'role': 'user_b', 'content': '不错', 'type': 'text', 'format': 'text', 'version': 'v001'}
    ]
    '''
    try:
        logger.info("======start send_oneshot_chat===========")
        request_params = request.json
        messages = request_params.get('messages', [])
        model = request_params.get('model', 'ml-plus')
        language = request_params.get('language', 'en')
        preset_name = request_params.get('preset_name', None)
        target_language = request_params.get('target_language', 'English')
        token = request_params.get('token', '')
        gpt_prams = request_params.get('gpt_prams', {})
        stream = request_params.get('stream', False)
        
        data = {
            "messages": messages,
            "target_language": target_language,
            "token": token,
            "gpt_prams": gpt_prams,
        }
        
        resp = await aref_oneshot_gpt_generator(
            messages=messages,
            model=model,
            language=language,
            preset_name=preset_name,
            picked_content=[],
            related_qa=[],
            data=data
        )
        _tmp_text = resp.choices[0].message.content
        resp_msgs = {
            "messages": [
                {'role': messages[-1]['role'], 'content': _tmp_text, 'type': 'text', 'format': 'text', 'version': 'v001'}
            ]
        }
        return success(resp_msgs)
    except Exception as e:
        logger.error(str(e))
        return fail(ERROR_CODE['PARAMS_ERROR'], str(e))
    
async def send_raw_chat_stream(request: Request):
    '''
    messages: [
        {'role': 'system', 'content': 'how are you?', 'type': 'text', 'format': 'text', 'version': 'v001'},
        {'role': 'user', 'content': '不错', 'type': 'text', 'format': 'text', 'version': 'v001'}
        {'role': 'assistant', 'content': '不错', 'type': 'text', 'format': 'text', 'version': 'v001'}
        {'role': 'user', 'content': '不错', 'type': 'text', 'format': 'text', 'version': 'v001'}
    ]
    '''
    try:
        logger.info("======start send_oneshot_chat===========")
        request_params = request.json
        messages = request_params.get('messages', [])
        model = request_params.get('model', 'ml-plus')
        language = request_params.get('language', 'en')
        preset_name = request_params.get('preset_name', None)
        target_language = request_params.get('target_language', 'English')
        token = request_params.get('token', '')
        gpt_prams = request_params.get('gpt_prams', {})
        stream = True
        
        data = {
            "messages": messages,
            "target_language": target_language,
            "token": token,
            "gpt_prams": gpt_prams,
        }
        
        resp = await aref_oneshot_gpt_generator(
            messages=messages,
            model=model,
            language=language,
            preset_name=preset_name,
            picked_content=[],
            related_qa=[],
            data=data,
            stream=stream,
            mode="raw",
        )
        
        async def event_generator(_response):
            # async for _str in getAnswerAndCallGpt(request_params['content'], userid, msggroup, language, messages):
            async for chunk in resp:
                _gpt_letter = chunk.choices[0].delta.content
                if _gpt_letter:
                    # _tmp_text += _gpt_letter
                    _str = json.dumps({"text": _gpt_letter})
                    await _response.write(f"data:{_str}\n\n")
                    await asyncio.sleep(0.001)
            await _response.write(f"data:[DONE]\n\n")
        return ResponseStream(event_generator, headers={"accept": "application/json"}, content_type="text/event-stream")
    except Exception as e:
        logger.error(e)
        logger.error(traceback.format_exc())


async def send_stylized_request(request: Request):
    # deep_insight, get_format_output
    params = request.json
    _type = params.get('type')
    userid = 0
    if hasattr(request.ctx, 'user'):
        userid = request.ctx.user['id']
    try:
        from genaipf.dispatcher.stylized_process import stylized_process_mapping
        stylized_generator = stylized_process_mapping[_type]
        async def event_generator(_response):
            async for _str in  stylized_generator(params):
                await _response.write(f"data:{_str}\n\n")
                await asyncio.sleep(0.01)
        return ResponseStream(event_generator, headers={"accept": "application/json"}, content_type="text/event-stream")
    except Exception as e:
        logger.error(e)
        logger.error(traceback.format_exc())