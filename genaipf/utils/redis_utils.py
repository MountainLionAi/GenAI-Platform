import redis
# https://github.com/aio-libs/aiocache
from aiocache import cached, Cache
from aiocache.serializers import PickleSerializer
from functools import wraps
from genaipf.conf import redis_conf


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
    Cache.REDIS, serializer=PickleSerializer(), namespace="main",
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
