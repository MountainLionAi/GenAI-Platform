from sanic import Request
import genaipf.services.user_service as user_service
import genaipf.services.user_log_service as user_log_service
from genaipf.utils.jwt_utils import JWTManager
from genaipf.utils.redis_utils import RedisConnectionPool
from genaipf.utils.log_utils import logger
from genaipf.constant.redis_keys import REDIS_KEYS
from genaipf.constant.error_code import ERROR_CODE
from genaipf.interfaces.common_response import fail

# IP封禁相关常量
MAX_IP_REQUESTS_PER_MINUTE = 60


# 记录用户操作日志
async def save_user_log(request: Request):
    request_path = request.path
    request_ip = request.remote_addr
    
    # 检查IP封禁状态和频率限制
    ip_check_result = await check_ip_access(request_ip)
    if ip_check_result:
        return ip_check_result  # 如果IP被封禁或频率过高，直接返回错误
    
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


async def check_ip_access(request_ip: str):
    """
    检查IP是否被封禁或频率过高
    :param request_ip: 请求IP地址
    :return: 如果有问题返回错误响应，否则返回None
    """
    try:
        redis_client = RedisConnectionPool().get_connection()
        
        # 检查IP是否在黑名单中
        blocked_ips_key = REDIS_KEYS['REQUEST_API_KEYS']['BLOCKED_IPS']
        is_blocked_ip = redis_client.sismember(blocked_ips_key, request_ip)
        if is_blocked_ip:
            logger.warning(f'IP {request_ip} 已被封禁，拒绝访问')
            return fail(ERROR_CODE['REQUEST_FREQUENCY_TOO_HIGH'], '')

        # 检查IP请求频率
        ip_frequency_key = REDIS_KEYS['REQUEST_API_KEYS']['IP_FREQUENCY'].format(request_ip)
        ip_request_count = redis_client.incr(ip_frequency_key, 1)
        if int(ip_request_count) == 1:
            redis_client.expire(ip_frequency_key, 60)  # 1分钟过期
        else:
            if int(ip_request_count) > MAX_IP_REQUESTS_PER_MINUTE:
                # 自动封禁IP
                redis_client.sadd(blocked_ips_key, request_ip)
                logger.warning(f'IP {request_ip} 请求频率过高 ({ip_request_count}次/分钟)，已自动封禁')
                return fail(ERROR_CODE['REQUEST_FREQUENCY_TOO_HIGH'], '')
        
        return None  # IP检查通过
    except Exception as e:
        logger.error(f'检查IP访问权限失败: {e}')
        return None  # 出错时允许通过，避免影响正常服务


async def add_blocked_ip(ip_address: str):
    """
    手动添加IP到黑名单
    :param ip_address: 需要封禁的IP地址
    """
    try:
        redis_client = RedisConnectionPool().get_connection()
        blocked_ips_key = REDIS_KEYS['REQUEST_API_KEYS']['BLOCKED_IPS']
        redis_client.sadd(blocked_ips_key, ip_address)
        logger.info(f'手动封禁IP: {ip_address}')
        return True
    except Exception as e:
        logger.error(f'手动封禁IP失败: {e}')
        return False


async def remove_blocked_ip(ip_address: str):
    """
    从黑名单中移除IP
    :param ip_address: 需要解封的IP地址
    """
    try:
        redis_client = RedisConnectionPool().get_connection()
        blocked_ips_key = REDIS_KEYS['REQUEST_API_KEYS']['BLOCKED_IPS']
        redis_client.srem(blocked_ips_key, ip_address)
        logger.info(f'解封IP: {ip_address}')
        return True
    except Exception as e:
        logger.error(f'解封IP失败: {e}')
        return False


async def get_blocked_ips():
    """
    获取所有被封禁的IP列表
    :return: 被封禁的IP列表
    """
    try:
        redis_client = RedisConnectionPool().get_connection()
        blocked_ips_key = REDIS_KEYS['REQUEST_API_KEYS']['BLOCKED_IPS']
        blocked_ips = redis_client.smembers(blocked_ips_key)
        return list(blocked_ips)
    except Exception as e:
        logger.error(f'获取黑名单IP列表失败: {e}')
        return []


async def get_ip_request_count(ip_address: str):
    """
    获取指定IP的当前请求计数
    :param ip_address: IP地址
    :return: 当前请求次数
    """
    try:
        redis_client = RedisConnectionPool().get_connection()
        ip_frequency_key = REDIS_KEYS['REQUEST_API_KEYS']['IP_FREQUENCY'].format(ip_address)
        count = redis_client.get(ip_frequency_key)
        return int(count) if count else 0
    except Exception as e:
        logger.error(f'获取IP请求次数失败: {e}')
        return 0


async def reset_ip_request_count(ip_address: str):
    """
    重置指定IP的请求计数
    :param ip_address: IP地址
    """
    try:
        redis_client = RedisConnectionPool().get_connection()
        ip_frequency_key = REDIS_KEYS['REQUEST_API_KEYS']['IP_FREQUENCY'].format(ip_address)
        redis_client.delete(ip_frequency_key)
        logger.info(f'重置IP {ip_address} 的请求计数')
        return True
    except Exception as e:
        logger.error(f'重置IP请求计数失败: {e}')
        return False



    



