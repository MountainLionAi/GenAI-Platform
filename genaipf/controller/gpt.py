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
from genaipf.utils import time_utils
from datetime import datetime, timedelta
from collections import defaultdict


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
    msggroup = args.get('msggroup', '')
    if not msggroup:
        data = {
            "messageList" : []
        }
        return success(data)
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
            base64content_array = ''
            if message.get('base64content'):
                base64content_array = message.get('base64content').split()
            message['content'] = {
                'type': 'user',
                'content': message['content'],
                'base64content': base64content_array,
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
            base64_content = None
            content = message['content']
            role = message['role']
            if role == 'assistant':
                if message['type'] in ['isDeep','text', 'eth_addresses_label_analyse', 'trx_addresses_label_analyse', 'btc_addresses_label_analyse', 'preset1', 'preset2', 'preset3', 'preset4', 'preset5', 'preset6', 'preset7']:
                    type = message['type']
                    if type == 'text':
                        type = 'gpt'
                    content_gpt = {
                        "type": type,
                        "content": content
                    }
                    content = json.dumps(content_gpt, ensure_ascii=False)
            elif role == 'user':
                type = 'user'
                if message['type'] in ['image']:
                    base64_content = " ".join(message['base64Content'])
                if message['type'] in ['pdf']:
                    base64_content = message['extra_content']
            gpt_message = (content, type, userid, message['msggroup'], message['code'], message['device_no'], message['file_type'], message['agent_id'], base64_content)
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
    args = request.args
    fixed_source = args.get('fixedSource', '')
    if fixed_source:
        messageList = await gpt_service.get_msggrou_plugin(userid)
    else:
        messageList = await gpt_service.get_msggroup(userid)
    # 获取当前时间
    now = datetime.now()
    # 定义存放结果的字典
    result = defaultdict(list)
    for message in messageList:
        create_time = message['create_time']
        if now.date() == create_time.date():
            result['today'].append(message)
        elif now.date() - create_time.date() == timedelta(days=1):
            result['yesterday'].append(message)
        elif now - create_time <= timedelta(days=7):
            result['seven'].append(message)
        elif create_time.year == now.year and create_time.month == now.month:
            result['thirty'].append(message)
        elif create_time.year == now.year:
            month_key = f"m-{create_time.month}"
            result[month_key].append(message)
        else:
            year_key = f"y-{create_time.year}"
            result[year_key].append(message)
        message['create_time'] = message['create_time'].strftime('%Y-%m-%d %H:%M:%S')
    # 对每个分组内部的数据按 create_time 倒序排序
    for key in result:
        result[key] = sorted(result[key], key=lambda x: x['create_time'], reverse=True)
    # 自定义排序规则
    sorted_keys = ['today', 'yesterday', 'seven', 'thirty'] + [f"m-{i}" for i in range(12, 0, -1)] + [f"y-{year}" for year in range(now.year, now.year - 10, -1)]
    # 排序结果
    sorted_result = []
    for key in sorted_keys:
        if key in result:
            sorted_result.append({key: result[key]})
    data = {
        "messageList" : sorted_result
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
