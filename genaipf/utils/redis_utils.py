import redis

from conf import redis_conf


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
