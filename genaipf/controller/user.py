from sanic import Request, response
from genaipf.exception.customer_exception import CustomerError
from genaipf.utils.log_utils import logger
from genaipf.interfaces.common_response import success, fail
from genaipf.constant.error_code import ERROR_CODE
import genaipf.services.user_service as user_service
from genaipf.utils.common_utils import mask_email
# import lib.hcaptcha as hcaptcha
import genaipf.utils.hcaptcha_utils as hcaptcha


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
    login_res = await user_service.user_login(request_params.get('email', ''), request_params.get('password', ''),
                                              request_params.get('signature', ''),
                                              request_params.get('wallet_address', ''),
                                              request_params.get('timestamp', ''), login_type)
    return success(login_res)


# 判断用户是否登陆
async def check_login(request: Request):
    logger.info('check_user_login')
    return success(
        {'is_login': True, 'account': mask_email(request.ctx.user.get('email')), 'user_id': request.ctx.user.get('id')})


# 用户注册
async def register(request: Request):
    logger.info('user register')
    request_params = request.json
    if not request_params or not request_params['email'] or not request_params['password'] or \
            not request_params['verifyCode']:
        raise CustomerError(status_code=ERROR_CODE['PARAMS_ERROR'])
    register_res = await user_service.user_register(request_params['email'], request_params['password'],
                                                    request_params['verifyCode'])
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
    login_out_res = await user_service.user_login_out(user['email'], user['id'])
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
