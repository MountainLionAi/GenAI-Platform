from sanic import Request
import genaipf.services.user_service as user_service
import genaipf.services.user_log_service as user_log_service
from genaipf.utils.jwt_utils import JWTManager
from genaipf.utils.redis_utils import RedisConnectionPool
from genaipf.utils.log_utils import logger


# 记录用户操作日志
async def save_user_log(request: Request):
    request_path = request.path
    request_ip = request.remote_addr
    try:
        token = request.token
        if token is None or len(request.token) == 0:
            user_id = 0
            await user_log_service.save_user_log(user_id, request_ip, request_path)
            return
        jwt_manager = JWTManager()
        check_res = jwt_manager.validate_token(token)
        if not check_res[0]:
            user_id = 0
            await user_log_service.save_user_log(user_id, request_ip, request_path)
            return
        redis_client = RedisConnectionPool().get_connection()
        user_token_key = user_service.get_user_key(check_res[1], check_res[2])
        user_token_key_final = user_token_key + ':' + token
        user = redis_client.get(user_token_key_final)
        if user is None:
            user_id = 0
            await user_log_service.save_user_log(user_id, request_ip, request_path)
            return
        user_id = check_res[1]
        await user_log_service.save_user_log(user_id, request_ip, request_path)
        return
    except Exception as e:
        logger.error(f'记录操作日志失败: {e}')    
        return



    



