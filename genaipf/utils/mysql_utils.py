import asyncio
import pymysql
import pymysql.cursors
from queue import Queue
from genaipf.conf import db_conf
from genaipf.utils.log_utils import logger

# RDS LOCK_WRITE_GROWTH（errno 1290）常为短暂写锁；轻量重试，不改调用方契约（仍返回 True/False）
_LOCK_WRITE_ERRNO = 1290
_WRITE_RETRY = 2
_WRITE_RETRY_BASE_SLEEP = 1.0


def _sql_preview(sql, limit=180):
    s = " ".join(str(sql).split())
    return s if len(s) <= limit else s[:limit] + "..."


def _is_lock_write_growth(exc) -> bool:
    args = getattr(exc, "args", ())
    return bool(args) and args[0] == _LOCK_WRITE_ERRNO


class CollectionPool:
    def __init__(self):
        self.host = db_conf.HOST
        self.port = db_conf.PORT
        self.user = db_conf.USER
        self.password = db_conf.PASSWORD
        self.database = db_conf.DATABASE
        self.pool_size = db_conf.POOL_SIZE
        self.connection_pool = Queue(maxsize=db_conf.POOL_SIZE)
        self._initialize_pool()

    def _initialize_pool(self):
        for _ in range(self.pool_size):
            conn = pymysql.connect(
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password,
                database=self.database,
                cursorclass=pymysql.cursors.DictCursor
            )
            self.connection_pool.put(conn)

    # 查询数据
    async def query(self, sql, params=None):
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(sql, params)
            query_data = cursor.fetchall()
            self.release_connection(conn)
            return query_data
        except Exception as e:
            logger.error(f"FetchDataError: {e}")
            self.release_connection(conn)
            return False

    # 更新数据
    async def update(self, sql, params=None):
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(sql, params)
            conn.commit()
            self.release_connection(conn)
            return True
        except Exception as e:
            logger.error(f"UpdateDataError: {e}")
            self.release_connection(conn)
            return False

    async def _write_with_retry(self, kind, runner, sql):
        """runner(conn, cursor) -> None；成功返回 True，失败返回 False。"""
        for attempt in range(_WRITE_RETRY + 1):
            conn = self.get_connection()
            cursor = conn.cursor()
            try:
                runner(conn, cursor)
                conn.commit()
                self.release_connection(conn)
                return True
            except Exception as e:
                try:
                    conn.rollback()
                except Exception:
                    pass
                self.release_connection(conn)
                preview = _sql_preview(sql)
                if _is_lock_write_growth(e) and attempt < _WRITE_RETRY:
                    logger.error(
                        f"{kind} LOCK_WRITE_GROWTH errno=1290 "
                        f"attempt={attempt + 1}/{_WRITE_RETRY + 1} sql={preview}: {e}"
                    )
                    await asyncio.sleep(_WRITE_RETRY_BASE_SLEEP * (attempt + 1))
                    continue
                if _is_lock_write_growth(e):
                    logger.error(
                        f"{kind} LOCK_WRITE_GROWTH errno=1290 exhausted sql={preview}: {e}"
                    )
                else:
                    logger.error(f"{kind} sql={preview}: {e}")
                return False
        return False

    # 插入数据
    async def insert(self, sql, params=None):
        def _run(conn, cursor):
            cursor.execute(sql, params)

        return await self._write_with_retry("InsertDataError", _run, sql)

    # 批量插入数据
    async def insert_batch(self, sql, params=None):
        def _run(conn, cursor):
            cursor.executemany(sql, params)

        return await self._write_with_retry("InsertDataError", _run, sql)

    # 删除数据
    async def delete(self, sql, params=None):
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(sql, params)
            conn.commit()
            self.release_connection(conn)
            return True
        except Exception as e:
            logger.error(f"DeleteDataError: {e}")
            self.release_connection(conn)
            return False

    # 执行事务操作
    async def execute_transaction(self, operations):
        """
        执行多步操作作为一个事务。
        operations 是一个列表，每个元素是一个 (sql, params) 元组。
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            for sql, params in operations:
                cursor.execute(sql, params)
            conn.commit()  # 全部操作成功后提交事务
            self.release_connection(conn)
            return True
        except Exception as e:
            conn.rollback()  # 发生异常时回滚事务
            logger.error(f"TransactionError: {e}")
            self.release_connection(conn)
            return False
        return True


    # 获取数据库连接
    def get_connection(self):
        return self.connection_pool.get()

    # 释放数据库连接
    def release_connection(self, conn):
        self.connection_pool.put(conn)
