import time
from genaipf.utils.redis_utils import RedisConnectionPool


def acquire_lock(lock_name, acquire_timeout=10):
    """尝试获取分布式锁"""
    # 生成唯一的锁标识符
    lock_identifier = str(time.time())
    redis_client = RedisConnectionPool().get_connection()
    # 使用SET命令尝试获取锁，如果锁已经被其他进程持有，将等待一段时间
    while True:
        result = redis_client.set(lock_name, lock_identifier, nx=True, ex=acquire_timeout)
        if result:
            return lock_identifier
        time.sleep(0.1)


def release_lock(lock_name, lock_identifier):
    """释放分布式锁"""
    redis_client = RedisConnectionPool().get_connection()
    stored_identifier = redis_client.get(lock_name)
    if stored_identifier and stored_identifier is not None and stored_identifier == lock_identifier:
        # 如果存储的标识符与当前标识符匹配，才释放锁
        redis_client.delete(lock_name)
