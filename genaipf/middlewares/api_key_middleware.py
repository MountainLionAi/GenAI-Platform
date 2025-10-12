from genaipf.interfaces.common_response import success, fail
from sanic import Request
from genaipf.utils.common_utils import get_uuid
from genaipf.constant.error_code import ERROR_CODE
from genaipf.constant.redis_keys import REDIS_KEYS
from genaipf.utils.redis_utils import RedisConnectionPool
from genaipf.utils.mysql_utils import CollectionPool
from genaipf.utils.log_utils import logger
from genaipf.routers.routers import blueprint_v2
from genaipf.utils.time_utils import get_format_time_YYYY_mm_dd
import asyncio

MAX_LIMIT_PER_MINUTE = 200
STATUS_AVAILABLE = 0
STATUS_UNAVAILABLE = 1


# 判断访问数据中的api_key是否合规
@blueprint_v2.middleware("request")
async def check_api_key(request: Request):
    request_ip = request.remote_addr
    api_key = request.headers.get('x-api-key', '')
    request.ctx.is_white_api = False
    if not api_key:
        return fail(ERROR_CODE['ILLEGAL_REQUEST'])
    redis_client = RedisConnectionPool().get_connection()
    if request.path != '/v2/api/getPopups':
        logger.info(f'当前请求的路径是{request.path},请求的ip是: {request_ip}, apiKey是{api_key}')
    api_set_key = REDIS_KEYS['REQUEST_API_KEYS']['API_KEYS']
    is_valida = redis_client.sismember(api_set_key, api_key)
    if not is_valida:
        return fail(ERROR_CODE['ILLEGAL_REQUEST'], '')

    # 检查是否被封禁
    is_a = False
    if request_ip in ['103.215.164.218']:
        is_a = True
    print('=========================request ip===========================')
    print(f'========================={request_ip}===========================')
    print(f'========================={is_a}===========================')
    print('=========================request ip===========================')
    if request_ip in ['103.215.164.218']:
        return fail(ERROR_CODE['REQUEST_FREQUENCY_TOO_HIGH'], '')
    forbid_api_key = REDIS_KEYS['REQUEST_API_KEYS']['FORBID_API_KEYS'].format(api_key, request_ip)
    forbid = redis_client.get(forbid_api_key)
    if forbid:
        return fail(ERROR_CODE['REQUEST_FREQUENCY_TOO_HIGH'], '')

    # 增加访问次数
    api_frequency_key = REDIS_KEYS['REQUEST_API_KEYS']['API_KEY_LIMIT'].format(api_key, request_ip)
    request_time = redis_client.incr(api_frequency_key, 1)
    if int(request_time) == 1:
        redis_client.expire(api_frequency_key, 60)
    else:
        if int(request_time) > MAX_LIMIT_PER_MINUTE:
            redis_client.set(forbid_api_key, 1)
            redis_client.expire(forbid_api_key, 15 * 60)
            return fail(ERROR_CODE['REQUEST_FREQUENCY_TOO_HIGH'], '')
    
    # 统计每日访问次数
    tracking_api_keys_key = REDIS_KEYS['REQUEST_API_KEYS']['TRACKING_API_KEYS']
    is_tracking = redis_client.sismember(tracking_api_keys_key, api_key)
    if is_tracking:
        request.ctx.is_white_api = True
        await record_daily_api_stats(redis_client, api_key, request.path)


async def generate_api_key(source=''):
    api_key = get_uuid()
    add_task = []
    add_params = (
        api_key,
        source,
        MAX_LIMIT_PER_MINUTE,
        STATUS_AVAILABLE
    )
    add_task.append(add_api_key_2db(add_params))
    add_task.append(add_api_key_2redis(api_key))
    await asyncio.gather(*add_task)
    return True


async def add_api_key_2db(params):
    sql = """
        INSERT INTO `api_keys` (`api_key`, `source`, `frequency`, `status`) VALUES (%s, %s, %s, %s)
    """
    res = await CollectionPool().insert(sql, params)
    return res


async def add_api_key_2redis(api_key):
    redis_client = RedisConnectionPool().get_connection()
    api_set_key = REDIS_KEYS['REQUEST_API_KEYS']['API_KEYS']
    redis_client.sadd(api_set_key, api_key)
    return True


async def remove_api_key(api_key):
    return True


async def record_daily_api_stats(redis_client, api_key: str, endpoint: str):
    """
    记录API key的每日访问统计
    :param redis_client: Redis客户端
    :param api_key: API key
    :param endpoint: 访问的接口路径
    """
    try:
        current_date = get_format_time_YYYY_mm_dd()
        
        # 记录特定接口的访问次数
        endpoint_stats_key = REDIS_KEYS['REQUEST_API_KEYS']['DAILY_STATS'].format(api_key, current_date)
        endpoint_key = f"{endpoint}"
        redis_client.hincrby(endpoint_stats_key, endpoint_key, 1)
        redis_client.expire(endpoint_stats_key, 60 * 60 * 24 * 40)  # 40天过期
        
        # 记录总访问次数
        total_stats_key = REDIS_KEYS['REQUEST_API_KEYS']['DAILY_STATS_TOTAL'].format(api_key, current_date)
        redis_client.incr(total_stats_key, 1)
        redis_client.expire(total_stats_key, 60 * 60 * 24 * 40)  # 30天过期
        
        logger.info(f'记录API key {api_key} 在 {current_date} 访问 {endpoint} 的统计')
    except Exception as e:
        logger.error(f'记录API key统计失败: {e}')


async def add_tracking_api_key(api_key: str):
    """
    添加需要统计的API key到名单中
    :param api_key: 需要统计的API key
    """
    try:
        redis_client = RedisConnectionPool().get_connection()
        tracking_api_keys_key = REDIS_KEYS['REQUEST_API_KEYS']['TRACKING_API_KEYS']
        redis_client.sadd(tracking_api_keys_key, api_key)
        logger.info(f'添加API key {api_key} 到统计名单')
        return True
    except Exception as e:
        logger.error(f'添加统计API key失败: {e}')
        return False


async def remove_tracking_api_key(api_key: str):
    """
    从统计名单中移除API key
    :param api_key: 需要移除的API key
    """
    try:
        redis_client = RedisConnectionPool().get_connection()
        tracking_api_keys_key = REDIS_KEYS['REQUEST_API_KEYS']['TRACKING_API_KEYS']
        redis_client.srem(tracking_api_keys_key, api_key)
        logger.info(f'从统计名单中移除API key {api_key}')
        return True
    except Exception as e:
        logger.error(f'移除统计API key失败: {e}')
        return False


async def get_tracking_api_keys():
    """
    获取所有需要统计的API key名单
    :return: 需要统计的API key列表
    """
    try:
        redis_client = RedisConnectionPool().get_connection()
        tracking_api_keys_key = REDIS_KEYS['REQUEST_API_KEYS']['TRACKING_API_KEYS']
        tracking_keys = redis_client.smembers(tracking_api_keys_key)
        return list(tracking_keys)
    except Exception as e:
        logger.error(f'获取统计API key名单失败: {e}')
        return []