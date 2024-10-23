from sanic import Request, response
from genaipf.exception.customer_exception import CustomerError
from genaipf.utils.log_utils import logger
from genaipf.interfaces.common_response import success, fail
from genaipf.constant.error_code import ERROR_CODE
import genaipf.services.user_service as user_service
from genaipf.utils.common_utils import mask_email
# import lib.hcaptcha as hcaptcha
import genaipf.utils.hcaptcha_utils as hcaptcha
from genaipf.utils.bot_utils import CollectionPool, get_news_by_api
from ml4gp.services.user_account_service import create_ai_account
from genaipf.utils.email_utils import EMAIL_SOURCE


# 用户登陆
async def login(request: Request):
    logger.info('user_login')
    request_params = request.json
    if not request_params:
        raise CustomerError(status_code=ERROR_CODE['PARAMS_ERROR'])
    login_type = request_params.get('type', 0)
    if int(login_type) == 0:
        if not request_params.get('email') or not request_params.get('password'):
            raise CustomerError(status_code=ERROR_CODE['PARAMS_ERROR'])
    elif int(login_type) == 1:
        if (not request_params.get('timestamp') or not request_params.get('signature')
                or not request_params.get('wallet_address')):
            raise CustomerError(status_code=ERROR_CODE['PARAMS_ERROR'])
    elif int(login_type) == 2:
        if not request_params.get('access_token') or not request_params.get('oauth'):
            raise CustomerError(status_code=ERROR_CODE['PARAMS_ERROR'])
    login_res = await user_service.user_login(request_params.get('email', ''), request_params.get('password', ''),
                                              request_params.get('signature', ''),
                                              request_params.get('wallet_address', ''),
                                              request_params.get('access_token', ''),
                                              request_params.get('oauth', ''),
                                              request_params.get('timestamp', ''), login_type)
    return success(login_res)

# 用户三方登陆
async def login_other(request: Request):
    logger.info('user_login_other')
    request_params = request.json
    if not request_params:
        raise CustomerError(status_code=ERROR_CODE['PARAMS_ERROR'])
    login_res = await user_service.user_login_other(request_params.get('email', ''), request_params.get('wallet_address', ''), request_params.get('source', ''))
    return success(login_res)


# 判断用户是否登陆
async def check_login(request: Request):
    logger.info('check_user_login')
    user_key = request.ctx.user.get('email')
    if hasattr(user_key, '@'):
        account = mask_email(user_key)
    else:
        account = user_key
    user_id = request.ctx.user.get('id')
    await create_ai_account(user_id)
    return success(
        {'is_login': True, 'account': account, 'user_id': request.ctx.user.get('id')})

# 判断用户是否存在
async def check_exist(request: Request):
    logger.info('check_exist')
    request_params = request.json
    if not request_params or not request_params['email']:
        raise CustomerError(status_code=ERROR_CODE['PARAMS_ERROR'])
    exist = True
    user = await user_service.get_user_info_from_db(request_params['email'])
    if not user:
        exist = False
    return success({'exist': exist})

# 用户注册
async def register(request: Request):
    logger.info('user register')
    request_params = request.json
    if not request_params or not request_params['email'] or not request_params['password'] or \
            not request_params['verifyCode']:
        raise CustomerError(status_code=ERROR_CODE['PARAMS_ERROR'])
    inviter = request_params.get('inviter', '')
    register_res = await user_service.user_register(request_params['email'], request_params['password'],
                                                    request_params['verifyCode'], inviter)
    return success(register_res)


async def modify_password(request: Request):
    logger.info('user modify password')
    request_params = request.json
    if not request_params or not request_params['email'] or not request_params['password'] or \
            not request_params['verifyCode']:
        raise CustomerError(status_code=ERROR_CODE['PARAMS_ERROR'])
    modify_res = await user_service.user_modify_password(request_params['email'], request_params['password'],
                                                         request_params['verifyCode'])
    return success(modify_res)


# 用户登出
async def login_out(request: Request):
    logger.info('user login out')
    user = request.ctx.user
    token = request.token
    login_out_res = await user_service.user_login_out(user['email'], user['id'], token)
    return success(login_out_res)


# 发送邮箱验证码
async def send_verify_code(request: Request):
    logger.info('send verify code')
    request_params = request.json
    if not request_params or not request_params['email'] or not request_params['captchaCode']:
        raise CustomerError(status_code=ERROR_CODE['PARAMS_ERROR'])
    # session_id = request.cookies.get('captcha_sid')
    # if not session_id:
    #     raise CustomerError(status_code=ERROR_CODE['PARAMS_ERROR'])
    send_res = await user_service.send_verify_code(request_params['email'], request_params['captchaCode'], '')
    return success(send_res)


async def send_verify_code_new(request: Request):
    logger.info('send verify code new')
    request_params = request.json
    email = request_params.get('email')
    captcha_resp = request_params.get('g-recaptcha-response', '')
    language = request_params.get('language', 'en')
    scene_type = request_params.get('scene', 'REGISTER')
    if not email:
        raise CustomerError(status_code=ERROR_CODE['PARAMS_ERROR'])
    send_res = await user_service.send_verify_code_new(email, captcha_resp, language, scene_type)
    return success(send_res)


async def send_verify_code_mobile(request: Request):
    logger.info('send verify code from app')
    request_params = request.json
    email = request_params.get('email')
    language = request_params.get('language', 'en')
    scene_type = request_params.get('scene', 'REGISTER')
    uuid = request_params.get('uuid', '')
    if not email or not uuid:
        raise CustomerError(status_code=ERROR_CODE['PARAMS_ERROR'])
    send_res = await user_service.send_verify_code_new(email, '', language, scene_type, False, {}, uuid, EMAIL_SOURCE['SWFTGPT'])
    return success(send_res)


# 获取图形验证码
async def get_captcha(request: Request):
    logger.info('get captcha image')
    session_id = request.ctx.session.sid
    image = user_service.get_user_captcha(session_id)
    format_response = {
        "code": 200,
        "data": image,
        "message": "success",
        "status": "true"
    }
    res = response.json(format_response)
    res.cookies['captcha_sid'] = session_id
    return res


async def verify_captcha_code(request: Request):
    captcha_res = request.form.get('g-recaptcha-response')
    res = hcaptcha.verify_hcaptcha(captcha_res)
    return success(res)


async def get_news(request: Request):
    sql = "SELECT id, content from total_news where is_sent != 1"
    update_sql = "UPDATE total_news set is_sent = 1 where id=%s"
    res = await CollectionPool().query(sql)
    renews = []
    if len(res) > 0:
        for id, content in enumerate(res):
            renews.append(content['content'])
            await CollectionPool().update(update_sql, content['id'])
    else:
        logger.info("开始发送快讯定时消息")
        msg = "Mlion.ai助手快讯播报\n\n"
        news = get_news_by_api()
        msg += news
        msg += "最新最全币圈资讯，尽在 Mlion.ai，欢迎使用 Mlion.ai 助手——您的 Web3 专属专家投资顾问，让投资交易更简单！\n使用链接：https://www.mlion.ai/"
        renews.append(msg)
    return success(renews)
