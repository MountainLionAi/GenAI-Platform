from sanic import Request, response
from genaipf.exception.customer_exception import CustomerError
from genaipf.constant.error_code import ERROR_CODE
from genaipf.interfaces.common_response import success,fail
import requests
import json
# import snowflake.client
import genaipf.services.gpt_service as gpt_service
from datetime import datetime
from genaipf.conf.server import os
from genaipf.utils.log_utils import logger
import traceback


OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

proxy = { 'https' : '127.0.0.1:8001'}
# specialType = ['preset1','preset2','preset3','preset4','coin_rate','multi_coin_price','multi_coin_predict']

async def http(request: Request):
    return response.json({"http": "sendchat"})


async def http4gpt4(request: Request):
    return response.json({"http4gpt4": "sendchat_gpt4"})



async def get_message_list(request: Request):
    userid = 13
    if hasattr(request.ctx, 'user'):
        userid = request.ctx.user['id']
    args = request.args
    msggroup = args['msggroup'][0]
    messageList = await gpt_service.get_gpt_message_limit(userid, msggroup, 20)
    for message in messageList:
        message['create_time'] = message['create_time'].strftime('%Y-%m-%d %H:%M:%S')
        if message['type'] == 'user_isDeep':
            message['content'] = {
                'type': 'user_isDeep',
                'content': message['content']
            }
            del message['base64content']
            del message['quoteInfo']
        elif message['type'] != 'user':
            message['content'] = json.loads(message['content'])
        else:
            message['content'] = {
                'type': 'user',
                'content': message['content'],
                'base64content': message.get('base64content'),
                'quote_info': message.get('quoteInfo')
            }
            del message['base64content']
            del message['quoteInfo']
        message['agent_id'] = message.get('agent_id') 
    data = {
        "messageList" : messageList
    }
    return success(data)


async def add_message(request: Request):
    try:
        userid = 0
        if hasattr(request.ctx, 'user'):
            userid = request.ctx.user['id']
        request_params = request.json
        logger.info(f'userid={userid}的用户添加聊天记录， request_params={request_params}')
        messages = request_params.get("messages")
        gpt_messages = []
        for message in messages:
            content = message['content']
            if message['type'] == 'gpt':
                content_gpt = {
                    "type": "gpt",
                    "content": content
                }
                content = json.dumps(content_gpt, ensure_ascii=False)
            gpt_message = (content, message['type'], userid, message['msggroup'], message['code'], message['device_no'], message['file_type'], message['agent_id'])
            gpt_messages.append(gpt_message)
        await gpt_service.add_gpt_message_with_code_from_share_batch(gpt_messages)
    except Exception as e:
        logger.error(f'add_message error {e}')
        logger.error(traceback.format_exc())
    return success(None)


async def get_msggroup_list(request: Request):
    userid = 0
    if hasattr(request.ctx, 'user'):
        userid = request.ctx.user['id']
    else:
        return success({"messageList" : []})
    messageList = await gpt_service.get_msggroup(userid)
    data = {
        "messageList" : messageList
    }
    return success(data)

async def del_msggroup_list(request: Request):
    userid = request.ctx.user['id']
    request_params = request.json
    if 'msggroup' in request_params:
        result = await gpt_service.del_msggroup(userid, request_params['msggroup'])    
        data = {
            "result" : "ok"
        }
        return success(data)
    else:
        return fail(ERROR_CODE['PARAMS_ERROR'])
