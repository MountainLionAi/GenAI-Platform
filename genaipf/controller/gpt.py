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
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

proxy = { 'https' : '127.0.0.1:8001'}
# specialType = ['preset1','preset2','preset3','preset4','coin_rate','multi_coin_price','multi_coin_predict']

async def http(request: Request):
    return response.json({"http": "sendchat"})


async def http4gpt4(request: Request):
    return response.json({"http4gpt4": "sendchat_gpt4"})



async def get_message_list(request: Request):
    userid = 0
    if hasattr(request.ctx, 'user'):
        userid = request.ctx.user['id']
    args = request.args
    msggroup = args['msggroup'][0]
    messageList = await gpt_service.get_gpt_message_limit(userid, msggroup, 20)
    for message in messageList:
        message['create_time'] = message['create_time'].strftime('%Y-%m-%d %H:%M:%S')
        if message['type'] != 'user':
            message['content'] = json.loads(message['content'])
        else:
            message['content'] = {
                'type': 'user',
                'content': message['content'],
                'base64content': message.get('base64content')
            }
            del message
    data = {
        "messageList" : messageList
    }
    return success(data)

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
