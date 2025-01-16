import json
from genaipf.utils.log_utils import logger
from sanic import Request
from genaipf.exception.customer_exception import CustomerError
from genaipf.services.gpt_service import add_share_message, del_gpt_message_by_code, get_share_msg, set_gpt_gmessage_rate_by_id
from genaipf.constant.error_code import ERROR_CODE
from genaipf.interfaces.common_response import success, fail
from genaipf.utils.qrcode_util import generate_qr_code_base64
from genaipf.tools.search.utils.search_task_manager import get_share_summary


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
        return success('记录成功')
    except Exception as e:
        logger.error(e)


async def user_opinion_for_tw(request: Request):
    logger.info("======start userRate for tw==========")

    params = request.json
    code = params.get('code', '')
    opinion = params.get('opinion', '')
    comment = params.get('comment', '')
    if not request_params or not code or not opinion:
        raise CustomerError(status_code=ERROR_CODE['PARAMS_ERROR'])
    msgid = str(code)
    if len(opinion) <= 0:
        raise CustomerError(status_code=ERROR_CODE['PARAMS_ERROR'])
    try:
        result = await set_gpt_gmessage_rate_by_id(opinion, comment, msgid)
        if not result:
            return success('already recorded')
        return success(True)
    except Exception as e:
        logger.error(e)


async def share_message(request: Request):
    userid = request.ctx.user['id']
    request_params = request.json
    _code = request_params.get("code")
    messages = request_params.get("messages")
    language = request_params.get("language", "cn")
    qrcode_url = request_params.get("qrcode_url", "")
    summary = request_params.get("summary", 0)
    qrcode = await generate_qr_code_base64(qrcode_url)
    summary_str = ''
    if summary == 1:
        for m in messages:
            if m["role"] in ["system", "user", "assistant"]:
                if m.get("type", "") == "preset4":
                    summary_str = f'{m["content"]["coinName"]}币价预测'
                    if language == 'en':
                        summary_str = f'{m["content"]["coinName"]} Daily Coin price predict'
                    break
                elif m.get("type", "") == "preset7":
                    summary_str = f'{m["content"]["predict"]["coinName"]}研报'
                    if language == 'en':
                        summary_str = f'{m["content"]["predict"]["coinName"]} research report'
                    break
        if summary_str == '':
            summary_str = await get_share_summary(messages, language)
    await add_share_message(_code, json.dumps(messages), userid, summary_str)
    data = {
        "qrcode": qrcode,
        "summary_str": summary_str
    }
    return success(data)

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
        if result:
            return success('已删除')
    except Exception as e:
        logger.error(e)
        return fail(ERROR_CODE['PARAMS_ERROR'])
