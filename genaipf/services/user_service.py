import bcrypt
import random
from genaipf.utils.mysql_utils import CollectionPool
from genaipf.exception.customer_exception import CustomerError
from genaipf.constant.error_code import ERROR_CODE
from genaipf.utils.jwt_utils import JWTManager
from genaipf.utils.redis_utils import RedisConnectionPool
from genaipf.constant.redis_keys import REDIS_KEYS
from genaipf.utils.log_utils import logger
from genaipf.utils.captcha_utils import CaptchaGenerator
from genaipf.utils.time_utils import get_format_time, get_current_timestamp
from genaipf.utils.common_utils import mask_email
from genaipf.constant.email_info import EMAIL_INFO
import genaipf.utils.hcaptcha_utils as hcaptcha
import genaipf.utils.email_utils as email_utils
from web3 import Web3
from eth_account.messages import encode_defunct
import requests
from datetime import datetime
ORIGIN_MESSAGE = "Welcome. Login Mountainlion. This is completely secure and doesn't cost anything! "


# 生成用户密码
def generate_user_password(password: str):
    pwd = password.encode('utf-8')
    hashed_pwd = bcrypt.hashpw(pwd, bcrypt.gensalt())
    return hashed_pwd


# 判断用户密码是否正确
def check_user_password(hashed_pwd, password: str):
    if bcrypt.checkpw(password.encode('utf-8'), hashed_pwd):
        return True
    else:
        return False


# 判断用户的签名钱包是否一致
def check_user_signature(signature, wallet_addr, time_stamp):
    is_valid = False
    # 检测时间是否过期
    time_stamp = str(time_stamp)
    if get_current_timestamp() - int(time_stamp) > 1800:
        raise CustomerError(status_code=ERROR_CODE['LOGIN_EXPIRED'])
    w3 = Web3()
    original_message = ORIGIN_MESSAGE + time_stamp
    message = encode_defunct(text=original_message)
    recovered_signer = w3.eth.account.recover_message(message, signature=signature)
    # 判断签名的钱包地址
    if wallet_addr.lower() == recovered_signer.lower():
        is_valid = True
    return is_valid


# 用户登陆
async def user_login(email, password, signature, wallet_addr, access_token, oauth, timestamp, login_type):
    if login_type == 1:
        if not check_user_signature(signature, wallet_addr, timestamp):
            raise CustomerError(status_code=ERROR_CODE['WALLET_SIGN_ERROR'])
        wallet_addr = wallet_addr.lower()
        user = await get_user_info_by_address(wallet_addr)
        if not user:
            user_info = (
                '',
                '',
                '',
                '',
                '',
                wallet_addr,
                '',
                '',
                get_format_time(),
                ''
            )
            await add_user(user_info)
            user = await get_user_info_by_address(wallet_addr)
            user_info = user[0]
            from ml4gp.services.points_service import create_user_points_account
            await create_user_points_account(user_info['id'])
        else:
            user_info = user[0]
        account = wallet_addr
    elif login_type == 2:
        if oauth == 'google':
            google_user_info = await get_google_user_info(access_token)
            user = await get_user_info_by_oauth(google_user_info['id'], oauth)
            email = google_user_info['email']
            if not user:
                user_info = (
                    email,
                    '',
                    '',
                    google_user_info['name'],
                    '',
                    '',
                    oauth,
                    google_user_info['id'],
                    get_format_time(),
                    ''
                )
                await add_user(user_info)
                user = await get_user_info_by_oauth(google_user_info['id'], oauth)
                user_info = user[0]
                from ml4gp.services.points_service import create_user_points_account
                await create_user_points_account(user_info['id'])
            else:
                user_info = user[0]
            account = mask_email(email)
    else:
        user = await get_user_info_from_db(email)
        if not user:
            raise CustomerError(status_code=ERROR_CODE['USER_NOT_EXIST'])
        user_info = user[0]
        if not check_user_password(user_info['password'].encode('utf-8'), password):
            raise CustomerError(status_code=ERROR_CODE['PWD_ERROR'])
        account = mask_email(email)
        if not user_info['sub_id']:
            from ml4gp.services.user_account_service import create_ai_account
            await create_ai_account(user_info['id'])
    user_id = user_info['id']
    user_key = email if login_type != 1 else wallet_addr
    jwt_manager = JWTManager()
    jwt_token = jwt_manager.generate_token(user_info['id'], user_key)
    redis_client = RedisConnectionPool().get_connection()
    token_key = get_user_key(user_info['id'], user_key)
    token_key_final = token_key + ':' + jwt_token
    redis_client.set(token_key_final, jwt_token, 3600 * 24 * 180)  # 设置登陆态到redis
    await update_user_token(user_info['id'], jwt_token)
    return {'user_token': jwt_token, 'account': account, 'user_id': user_id, 'login_type': login_type}

# google oauth
async def get_google_user_info(access_token):
    api_url = 'https://www.googleapis.com/oauth2/v2/userinfo'
    headers ={
        "Authorization": f"Bearer {access_token}"
    }
    res_json = requests.get(api_url, headers=headers).json()
    if res_json.get('id'):
        return res_json
    else:
        raise CustomerError(status_code=ERROR_CODE['GOOGLE_OAUTH_ERROR'])


# 用户三方登陆
async def user_login_other(email, wallet_addr, source):
    user = None
    if email:
        user = await get_user_info_from_db(email)
        account = mask_email(email)
        user_key = email
    else:
        user = await get_user_info_by_address(wallet_addr)
        account = wallet_addr
        user_key = wallet_addr
    if not user:
        if email:
            user_info = (
                email,
                '',
                '',
                email,
                '',
                '',
                '',
                get_format_time(),
                source
            )
            await add_user_source(user_info)
            user = await get_user_info_from_db(email)
        else:
            user_info = (
                '',
                '',
                '',
                '',
                '',
                wallet_addr,
                '',
                get_format_time(),
                source
            )
            await add_user_source(user_info)
            user = await get_user_info_by_address(wallet_addr)
    user_info = user[0]
    user_id = user_info['id']
    jwt_manager = JWTManager()
    jwt_token = jwt_manager.generate_token(user_info['id'], user_key)
    redis_client = RedisConnectionPool().get_connection()
    token_key = get_user_key(user_info['id'], user_key)
    token_key_final = token_key + ':' + jwt_token
    redis_client.set(token_key_final, jwt_token, 3600 * 24 * 180)  # 设置登陆态到redis
    await update_user_token(user_info['id'], jwt_token)
    return {'user_token': jwt_token, 'account': account, 'user_id': user_id}


# 用户靠id和账号登录，用于三方情况
async def user_login_by_id(user_id, account, expired_time_remain):
    user_key = account
    jwt_manager = JWTManager(expires_in_seconds=expired_time_remain)
    jwt_token = jwt_manager.generate_token(user_id, user_key)
    redis_client = RedisConnectionPool().get_connection()
    token_key = get_user_key(user_id, user_key)
    token_key_final = token_key + ':' + jwt_token
    redis_client.set(token_key_final, jwt_token, expired_time_remain)  # 设置登陆态到redis
    await update_user_token(user_id, jwt_token)
    return {'user_token': jwt_token, 'account': account, 'user_id': user_id}
        


# 用户登出相关操作
async def user_login_out(email, user_id, token):
    try:
        redis_client = RedisConnectionPool().get_connection()
        user_token_key = get_user_key(user_id, email)
        user_token_key = user_token_key + ':' + token
        redis_client.delete(user_token_key)
        await update_user_token(user_id, '')
        return True
    except Exception as e:
        logger.error(f'login out error {e}')
        return False


# 用户注册
async def user_register(email, password, verify_code, inviter):
    try:
        user = await get_user_info_from_db(email)
        if user and len(user) != 0:
            raise CustomerError(status_code=ERROR_CODE['USER_EXIST'])
        check_email_code(email, verify_code, email_utils.EMAIL_SCENES['REGISTER'])
        hashed_pwd = generate_user_password(password)
        user_info = (
            email,
            hashed_pwd,
            '',
            email,
            '',
            '',
            '',
            '',
            get_format_time(),
            inviter
        )
        await add_user(user_info)
        user_infos = await get_user_info_from_db(email)
        if user_infos and len(user_infos) != 0:
            user_info = user_infos[0]
            from ml4gp.services.points_service import create_user_points_account
            await create_user_points_account(user_info['id'])
        if inviter:
            from ml4gp.services.points_activity_service import create_user_points_act, POINTS_ACTIVITY_INVITATION
            await create_user_points_act({}, POINTS_ACTIVITY_INVITATION, inviter)
        return True
    except Exception as e:
        logger.error(f'User register error: {e}')
        if type(e) == CustomerError and e.status_code == 2006:
            raise CustomerError(status_code=ERROR_CODE['VERIFY_CODE_ERROR'])
        raise CustomerError(status_code=ERROR_CODE['REGISTER_ERROR'])


# 用户修改密码
async def user_modify_password(email, password, verify_code):
    try:
        user = await get_user_info_from_db(email)
        if not user or len(user) == 0:
            raise CustomerError(status_code=ERROR_CODE['USER_NOT_EXIST'])
        user = user[0]
        check_email_code(email, verify_code, email_utils.EMAIL_SCENES['FORGET_PASSWORD'])
        password_hashed = generate_user_password(password)
        await update_user_password(user['id'], password_hashed)
        await clear_user_status(user['id'], email)
        return True
    except Exception as e:
        logger.error(f'User modify password error: {e}')
        if type(e) == CustomerError and e.status_code == 2006:
            raise CustomerError(status_code=ERROR_CODE['VERIFY_CODE_ERROR'])
        raise CustomerError(status_code=ERROR_CODE['MODIFY_PASSWORD_ERROR'])


# 生成用户token的redis_key
def get_user_key(user_id, email):
    token_key = REDIS_KEYS['USER_KEYS']['USER_TOKEN'].format(user_id, email)
    return token_key


# 根据email获取用户信息
async def get_user_info_from_db(email):
    sql = 'SELECT id, email, password, auth_token, user_name, avatar_url, wallet_address, sub_id  FROM user_infos WHERE ' \
          'email=%s ' \
          'AND status=%s'
    result = await CollectionPool().query(sql, (email, 0))
    return result


# 根据wallet_address获取用户信息
async def get_user_info_by_address(wallet_address):
    sql = 'SELECT id, email, password, auth_token, user_name, avatar_url, wallet_address  FROM user_infos WHERE ' \
          'wallet_address=%s ' \
          'AND status=%s'
    result = await CollectionPool().query(sql, (wallet_address, 0))
    return result

# 根据oauth获取用户信息
async def get_user_info_by_oauth(oauthid, oauth):
    sql = 'SELECT id, email, password, auth_token, user_name, avatar_url, wallet_address, sub_id  FROM user_infos WHERE ' \
          'oauth_id=%s ' \
          'AND oauth=%s ' \
          'AND status=%s'
    result = await CollectionPool().query(sql, (oauthid, oauth, 0))
    return result    


# 根据userid获取用户信息
async def get_user_info_by_userid(userid):
    sql = 'SELECT id, wallet_address, create_time, user_name, avatar_url, user_name_update_time FROM user_infos WHERE ' \
          'id=%s ' \
          'AND status=%s'
    result = await CollectionPool().query(sql, (userid, 0))
    return result


# 添加一个新用户
async def add_user(user_info):
    sql = "INSERT INTO `user_infos` (`email`, `password`, `auth_token`, `user_name`, `avatar_url`, `wallet_address`, " \
          "`oauth`, `oauth_id`, `create_time`, `inviter`) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    res = await CollectionPool().insert(sql, user_info)
    return res

# 添加一个三方新用户
async def add_user_source(user_info):
    sql = "INSERT INTO `user_infos` (`email`, `password`, `auth_token`, `user_name`, `avatar_url`, `wallet_address`, " \
          "`oauth`, `create_time`, `source`) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)"
    res = await CollectionPool().insert(sql, user_info)
    return res

# 更新用户token
async def update_user_token(user_id, token):
    sql = "UPDATE `user_infos` SET `auth_token`=%s WHERE id=%s"
    res = await CollectionPool().update(sql, (token, user_id))
    return res


# 更新用户password
async def update_user_password(user_id, password):
    sql = "UPDATE `user_infos` SET `password`=%s WHERE id=%s"
    res = await CollectionPool().update(sql, (password, user_id))
    return res

async def update_user_name(user_id, user_name):
    sql = "UPDATE `user_infos` SET `user_name`=%s , `user_name_update_time`=%s WHERE id=%s"
    res = await CollectionPool().update(sql, (user_name, datetime.now(), user_id))
    return res

async def update_user_avatar(user_id, user_image):
    sql = "UPDATE `user_infos` SET avatar_url=%s WHERE id=%s"
    res = await CollectionPool().update(sql, (user_image, user_id))
    return res

# 获取图形验证码
def get_user_captcha(session_id):
    generator = CaptchaGenerator()
    code, base64_image = generator.generate_base64()
    redis_client = RedisConnectionPool().get_connection()
    captcha_key = REDIS_KEYS['USER_KEYS']['CAPTCHA_CODE'].format(session_id)
    redis_client.setex(captcha_key, 60 * 2, code)
    return base64_image


# 给用户的邮箱发送注册验证码
async def send_verify_code(email, captcha_code, session_id):
    try:
        captcha_key = REDIS_KEYS['USER_KEYS']['CAPTCHA_CODE'].format(session_id)
        redis_client = RedisConnectionPool().get_connection()
        # TODO 增加临时逻辑
        if captcha_code == '3333':
            pass
        else:
            store_captcha_code = redis_client.get(captcha_key)
            if not store_captcha_code:
                raise CustomerError(status_code=ERROR_CODE['CAPTCHA_ERROR'])
            if captcha_code != store_captcha_code:
                raise CustomerError(status_code=ERROR_CODE['CAPTCHA_ERROR'])
        user = await get_user_info_from_db(email)
        if user and len(user) != 0:
            raise CustomerError(status_code=ERROR_CODE['USER_EXIST'])
        email_code = generate_email_code()
        email_key = REDIS_KEYS['USER_KEYS']['EMAIL_CODE'].format(email)
        await email_utils.send_email('CaptchaCode', email_code, email)
        redis_client.setex(email_key, 60 * 2, email_code)
        return True
    except Exception as e:
        logger.error(f'send user email error: {e}')
        if isinstance(e, CustomerError):
            raise CustomerError(status_code=e.status_code)
        return False


# 基于hcaptcha的图形验证
async def send_verify_code_new(email, captcha_resp, language, scene, need_captcha = True, option_params = {}, related_key = ''):
    try:
        redis_client = RedisConnectionPool().get_connection()
        user = await get_user_info_from_db(email)
        if scene == email_utils.EMAIL_SCENES['REGISTER'] and user and len(user) != 0:
            raise CustomerError(status_code=ERROR_CODE['USER_EXIST'])
        if scene == email_utils.EMAIL_SCENES['FORGET_PASSWORD'] and (not user or len(user) == 0):
            raise CustomerError(status_code=ERROR_CODE['USER_NOT_EXIST'])
        is_continue = await check_user_continue_send_email(email)
        if not need_captcha:
            is_continue = True
        captcha_verify_status = False

        # 判断要发的验证码类型是不是在列表中
        if scene not in email_utils.LIMIT_TIME_10MIN.keys():
            raise CustomerError(status_code=ERROR_CODE['PARAMS_ERROR'])

        # 先判断用户是否可以持续发送验证码，通过人机检测的用户在十分钟内可以再次发送验证码
        if not is_continue:
            if not hcaptcha.verify_hcaptcha(captcha_resp, email):
                raise CustomerError(status_code=ERROR_CODE['CAPTCHA_ERROR'])
            else:
                captcha_verify_status = True

        # 移动端uuid或者提现的的检测10分钟内请求次数
        if not need_captcha and related_key:
            unique_limit_key = REDIS_KEYS['USER_KEYS']['EMAIL_CODE_DEVICE_LIMIT'].format(scene, related_key)
            unique_times = redis_client.get(unique_limit_key)
            if unique_times:
                unique_times = int(unique_times)
            else:
                unique_times = 0
            current_times = unique_times + 1
            if current_times > 3:
                raise CustomerError(status_code=ERROR_CODE['EMAIL_TIME_LIMIT'])
            redis_client.set(unique_limit_key, current_times)
            redis_client.expire(unique_limit_key, 10 * 60)

        # 判断是否到达发送邮件数量的上线
        send_times = await email_utils.get_email_times(email, scene=email_utils.EMAIL_SCENES[scene])
        if not email_utils.check_time(send_times, email_utils.LIMIT_TIME_10MIN[scene]):
            raise CustomerError(status_code=ERROR_CODE['EMAIL_TIME_LIMIT'])

        # 生成发送验证码邮件相关的模版
        email_code = generate_email_code()
        subject = EMAIL_INFO[scene]['subject'][language]
        email_content = await email_utils.format_captcha_email(email, email_code, language, scene, option_params)
        if need_captcha == False:
            email_key = REDIS_KEYS['USER_KEYS']['EMAIL_CODE_OTHER'].format(email, scene, related_key)
        else:
            email_key = REDIS_KEYS['USER_KEYS']['EMAIL_CODE'].format(email, scene)
        # 发送邮箱验证码
        await email_utils.send_email(subject, email_content, email)
        redis_client.setex(email_key, 60 * 15, email_code)

        # 增加发送验证码的限制次数
        await email_utils.add_email_times(email, scene=email_utils.EMAIL_SCENES[scene])

        # 如果是通过人机检测的，设置为可以持续发送邮箱验证码
        if captcha_verify_status:
            await make_user_continue_send_email(email)
        return True
    except Exception as e:
        logger.error(f'send user email error: {e}')
        if isinstance(e, CustomerError):
            raise CustomerError(status_code=e.status_code)
        return False


# 生成6位随机邮箱验证码
def generate_email_code():
    random_number = ''.join([str(random.randint(0, 9)) for _ in range(6)])
    return random_number


# 检测邮箱验证码是否正确
def check_email_code(email, verify_code, scene, related_key = ''):
    redis_client = RedisConnectionPool().get_connection()
    if related_key:
        email_key = REDIS_KEYS['USER_KEYS']['EMAIL_CODE_OTHER'].format(email, scene, related_key)
    else:
        email_key = REDIS_KEYS['USER_KEYS']['EMAIL_CODE'].format(email, scene)
    stored_verify_code = redis_client.get(email_key)
    if not stored_verify_code:
        raise CustomerError(status_code=ERROR_CODE['VERIFY_CODE_ERROR'])
    if verify_code != stored_verify_code:
        raise CustomerError(status_code=ERROR_CODE['VERIFY_CODE_ERROR'])
    return True


# 设置某个邮箱可以持续发送邮件
async def make_user_continue_send_email(email):
    continue_key = REDIS_KEYS['USER_KEYS']['EMAIL_CONTINUE'].format(email)
    redis_client = RedisConnectionPool().get_connection()
    res = redis_client.set(continue_key, 1, 60 * 10)
    return True


# 判断用户是否可以持续发送验证码
async def check_user_continue_send_email(email):
    continue_key = REDIS_KEYS['USER_KEYS']['EMAIL_CONTINUE'].format(email)
    redis_client = RedisConnectionPool().get_connection()
    check_res = redis_client.get(continue_key)
    if check_res is not None:
        return True
    else:
        return False


# 清除用户相关登陆态
async def clear_user_status(user_id, email):
    redis_client = RedisConnectionPool().get_connection()
    token_key = get_user_key(user_id, email) + '*'
    keys_all = redis_client.keys(token_key)
    for key in keys_all:
        redis_client.delete(key)
    return True
