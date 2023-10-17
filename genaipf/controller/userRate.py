import json
from genaipf.utils.log_utils import logger
from sanic import Request
from genaipf.exception.customer_exception import CustomerError
from genaipf.services.gpt_service import add_share_message, del_gpt_message_by_code, get_share_msg, set_gpt_gmessage_rate_by_id
from genaipf.constant.error_code import ERROR_CODE
from genaipf.interfaces.common_response import success, fail


async def user_rate(request: Request):
    logger.info("======start userRate==========")

    request_params = request.args
    if not request_params or not request_params['code'] or not request_params['rate']:
        raise CustomerError(status_code=ERROR_CODE['PARAMS_ERROR'])
    msgid = request_params.get('code')
    rate = request_params.get('rate')
    comment = request_params.get('comment', "")
    if len(rate) <= 0:
        return 
    try: 
        result = await set_gpt_gmessage_rate_by_id(rate,comment, msgid)
        if not result:
            return success('已记录')
    except Exception as e:
        logger.error(e)


async def share_message(request: Request):
    userid = request.ctx.user['id']
    request_params = request.json
    _code = request_params.get("code")
    messages = request_params.get("messages")
    await add_share_message(_code, json.dumps(messages), userid)
    return success("成功")

async def get_share_message(request: Request):
    logger.info(f'>>>>>>>>>>>>>>>HEADERS:{request.headers}')
    logger.info(f'>>>>>>>>>>>>>>>remote_addr:{request.remote_addr}')
    request_params = request.json
    _code = request_params.get("code")
    messages = await get_share_msg(_code)
    if messages :
        message = messages[0]
        message['messages'] = json.loads(message['messages'])  
        return success(message)
    else :
        return fail(ERROR_CODE['PARAMS_ERROR'])

async def del_message_by_codes(request: Request):
    userid = request.ctx.user['id']
    request_params = request.json
    _code = request_params['code']
    try:
        result = await del_gpt_message_by_code(userid, _code)
        logger.info(f">>>>>>>>>>>>deleted messages:{_code}")
        if not result:
            return success('已删除')
    except Exception as e:
        logger.error(e)
