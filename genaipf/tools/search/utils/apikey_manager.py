import json
import random
from genaipf.utils.redis_utils import RedisConnectionPool
from genaipf.constant.redis_keys import REDIS_KEYS
from genaipf.utils.log_utils import logger


# 根据接入的sdk类型获取api_key
def get_api_key_by_type(type = 'exa'):
    redis_client = RedisConnectionPool().get_connection()
    redis_key = REDIS_KEYS['RAG_API_KEYS']['KEYS_STATUS'].format(type)
    random_key = ''
    avaiable_keys = []
    try:
        hash_keys = redis_client.hgetall(redis_key)
        for key, value in hash_keys.items():
            if int(value) == 1:
                avaiable_keys.append(key)
        if len(avaiable_keys) != 0:
            random_key = random.choice(avaiable_keys)
    except Exception as e:
        logger.error(f'获取{type}--apikey错误: {e}')
    return random_key


# 向redis集合中添加key
def set_api_key_by_type(keys, type = 'exa'):
    redis_client = RedisConnectionPool().get_connection()
    redis_key = REDIS_KEYS['RAG_API_KEYS']['KEYS_STATUS'].format(type)
    api_keys = json.loads(keys)
    for api_key in api_keys:
        redis_client.hset(redis_key, api_key, 1)
    return True


# 设置某一个apikey不可用
def set_api_key_unavaiable(key, type = 'exa'):
    redis_client = RedisConnectionPool().get_connection()
    redis_key = REDIS_KEYS['RAG_API_KEYS']['KEYS_STATUS'].format(type)
    redis_client.hset(redis_key, key, 0)
    return True
