from genaipf.interfaces.common_response import success, fail
from sanic import Request
from genaipf.utils.common_utils import get_uuid
from genaipf.constant.error_code import ERROR_CODE
from genaipf.constant.redis_keys import REDIS_KEYS
from genaipf.utils.redis_utils import RedisConnectionPool
from genaipf.utils.mysql_utils import CollectionPool
from genaipf.utils.log_utils import logger
from genaipf.routers.routers import blueprint_v2
import asyncio

MAX_LIMIT_PER_MINUTE = 200
STATUS_AVAILABLE = 0
STATUS_UNAVAILABLE = 1


# 判断访问数据中的api_key是否合规
@blueprint_v2.middleware("request")
async def check_api_key(request: Request):
    request_ip = request.remote_addr
    api_key = request.headers.get('x-api-key', '')
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