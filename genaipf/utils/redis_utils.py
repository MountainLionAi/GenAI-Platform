import redis
# https://github.com/aio-libs/aiocache
from redis import asyncio as aioredis
from aiocache import cached, Cache
from aiocache.serializers import PickleSerializer
import asyncio
from functools import wraps
from typing import List
from genaipf.conf import redis_conf

REDIS_DEFAULT_NAMESPACE = "main"

class RedisConnectionPool:
    redis_client = None

    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(RedisConnectionPool, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        self.pool = redis.ConnectionPool(host=redis_conf.HOST, port=redis_conf.PORT, db=redis_conf.DB,
                                         password=redis_conf.PASSWORD, decode_responses=True)

    def get_connection(self):
        if self.redis_client is not None:
            return self.redis_client
        else:
            self.redis_client = redis.Redis(connection_pool=self.pool)
            return self.redis_client

async def get_from_cache(cache, key):
    return await cache.get(key)

async def set_to_cache(cache, key, value, ttl):
    await cache.set(key, value, ttl=ttl)

def generate_cache_key(func, *args, **kwargs):
    # 生成基于函数名、位置参数和关键字参数的缓存键
    args_str = ','.join([str(arg) for arg in args])
    kwargs_str = ','.join([f"{k}={v}" for k, v in kwargs.items()])
    return f"{func.__module__}.{func.__name__}:{args_str}:{kwargs_str}"

# 初始化 Redis 缓存实例
__cache = Cache(
    Cache.REDIS, serializer=PickleSerializer(), namespace=REDIS_DEFAULT_NAMESPACE,
    endpoint=redis_conf.HOST, port=redis_conf.PORT, password=redis_conf.PASSWORD
)

def async_redis_cache(ttl, key_prefix=""):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # 使用 generate_cache_key 函数生成基于函数参数的动态键
            dynamic_key = f"{key_prefix}:{generate_cache_key(func, *args, **kwargs)}"
            print(f"dynamic_key: {dynamic_key}")
            result = await get_from_cache(__cache, dynamic_key)
            if result is None:
                print(f"not hit dynamic_key: {dynamic_key}")
                # 缓存未命中，调用原函数并将结果保存到缓存
                result = await func(*args, **kwargs)
                await set_to_cache(__cache, dynamic_key, result, ttl)
            else:
                print(f"hit dynamic_key: {dynamic_key}")
            return result
        return wrapper
    return decorator

# # 使用自定义的 async_redis_cache 装饰器
# @async_redis_cache(ttl=10, key="unique_key")
# async def cached_call():
#     # 这里是你的异步函数逻辑
#     ...


# 手动使用的 cache
manual_cache = Cache(
    Cache.REDIS, serializer=PickleSerializer(), namespace="manual",
    endpoint=redis_conf.HOST, port=redis_conf.PORT, password=redis_conf.PASSWORD
)

# from genaipf.utils.redis_utils import x_get, x_set, x_is_key_in, x_delete
async def x_get(key):
    return await manual_cache.get(key)

async def x_set(key, value, ttl=None):
    await manual_cache.set(key, value, ttl=ttl)

async def x_is_key_in(key):
    return await manual_cache.exists(key)

async def x_delete(key):
    await manual_cache.delete(key)

# async def x_scratch_keys_of_prefix(prefix):
#     keys_with_prefix = []
#     match_pattern = f'{manual_cache.namespace}:{prefix}*'
#     cursor = 0
#     async for x in manual_cache.client.scan_iter(match=match_pattern):
#         print(x)
#     cursor, keys = await manual_cache.client.scan(cursor, match=match_pattern)
    
#     keys_with_prefix.extend(keys)
#     # Clean up: Remove the namespace prefix from keys
#     keys_with_prefix = [key.decode('utf-8').replace(f'{manual_cache.namespace}:', '') for key in keys_with_prefix]
#     return keys_with_prefix



# async def x_delete_keys_of_prefix(prefix):
#     keys_with_prefix = await x_scratch_keys_of_prefix(prefix)

#     # The delete method expects the keys to include the namespace
#     keys_with_namespace = [f'{manual_cache.namespace}:{key}' for key in keys_with_prefix]
#     if keys_with_namespace:
#         await manual_cache.client.delete(*keys_with_namespace)


def x_list_cache(prefix, ttl=None):
    def decorator(func):
        @wraps(func)
        async def wrapper(input_l: List):
            tasks = []
            not_in_cache = []

            # Check which items are already in cache
            for item in input_l:
                cache_key = f"{prefix}{item}"
                if await x_is_key_in(cache_key):
                    tasks.append(x_get(cache_key))
                else:
                    not_in_cache.append(item)

            # Fetch cached values
            cached_results = await asyncio.gather(*tasks)

            # Calculate the values that are not in cache
            print(f'>>>x_list_cache {prefix}: {not_in_cache}')
            calculated_results = await func(not_in_cache) if not_in_cache else []

            # Store the newly calculated values in cache
            for item, result in zip(not_in_cache, calculated_results):
                cache_key = f"{prefix}{item}"
                await x_set(cache_key, result, ttl=ttl)

            # Combine results from cache and newly calculated values
            results = cached_results + calculated_results
            return results

        return wrapper
    return decorator