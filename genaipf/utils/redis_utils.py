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

def generate_cache_key(func, *args, **kwargs):
    # 生成基于函数名、位置参数和关键字参数的缓存键
    args_str = ','.join([str(arg) for arg in args])
    kwargs_str = ','.join([f"{k}={v}" for k, v in kwargs.items()])
    return f"{func.__module__}.{func.__name__}:{args_str}:{kwargs_str}"

def async_redis_cache(ttl, key_prefix=""):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # 使用 generate_cache_key 函数生成基于函数参数的动态键
            dynamic_key = f"{key_prefix}:{generate_cache_key(func, *args, **kwargs)}"
            print(f"dynamic_key: {dynamic_key}")
            return await cached(
                ttl=ttl, 
                cache=Cache.REDIS, 
                key=dynamic_key, 
                serializer=PickleSerializer(), 
                port=redis_conf.PORT,  # 你的 Redis 端口，如果默认就是 6379 则这个不需要改
                endpoint=redis_conf.HOST,  # 用你的 Redis 服务器 IP 地址替换 "your_redis_ip"
                password=redis_conf.PASSWORD,  # 用你的 Redis 密码替换 "your_redis_password"
                namespace="main"
            )(func)(*args, **kwargs)
        return wrapper
    return decorator

# # 使用自定义的 async_redis_cache 装饰器
# @async_redis_cache(ttl=10, key="unique_key")
# async def cached_call():
#     # 这里是你的异步函数逻辑
#     ...
