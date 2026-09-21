from genaipf.interfaces.common_response import success, fail
from sanic import Request
from genaipf.conf import path_without_login as path_without_login_conf
from genaipf.constant.error_code import ERROR_CODE
import genaipf.services.user_service as user_service
from genaipf.utils.jwt_utils import JWTManager
from genaipf.utils.redis_utils import RedisConnectionPool


def _no_login_required(path: str) -> bool:
    if '/static/' in path:
        return True
    table = path_without_login_conf.PATH_WITHOUT_LOGIN
    if path in table:
        return True
    # 浏览器或反代有时会带尾斜杠，免登名单是精确匹配
    if path.endswith('/') and path.rstrip('/') in table:
        return True
    return False


# 判断用户的登陆态并赋值给request对象
async def check_user(request: Request):
    request_path = request.path
    # 判断当前路由是否在不需要登陆态的路由中
    if _no_login_required(request_path):
        token = request.token
        if token is None or len(request.token) == 0:
            return
        jwt_manager = JWTManager()
        check_res = jwt_manager.validate_token(token)
        if not check_res[0]:
            return
        redis_client = RedisConnectionPool().get_connection()
        user_token_key = user_service.get_user_key(check_res[1], check_res[2])
        user_token_key_final = user_token_key + ':' + token
        user = redis_client.get(user_token_key_final)
        if user is None:
            return
        user = {
            'id': check_res[1],
            'email': check_res[2]
        }
        request.ctx.user = user
    else:
        token = request.token
        if token is None or len(request.token) == 0:
            return fail(ERROR_CODE["NOT_AUTHORIZED"])
        jwt_manager = JWTManager()
        check_res = jwt_manager.validate_token(token)
        if not check_res[0]:
            return fail(ERROR_CODE["NOT_AUTHORIZED"])
        redis_client = RedisConnectionPool().get_connection()
        user_token_key = user_service.get_user_key(check_res[1], check_res[2])
        user_token_key_final = user_token_key + ':' + token
        user = redis_client.get(user_token_key_final)
        if user is None:
            return fail(ERROR_CODE["NOT_AUTHORIZED"])
        user = {
            'id': check_res[1],
            'email': check_res[2]
        }
        request.ctx.user = user



