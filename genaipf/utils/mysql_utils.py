import asyncio
import threading
from queue import Queue

import pymysql
import pymysql.cursors
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
    """pymysql 连接池。假异步会冻 Sanic 事件循环，所有阻塞 I/O 走 to_thread。

    调用方普遍写 CollectionPool().query(...)；必须单例，否则每次新建 POOL_SIZE 条连接。
    """

    _instance = None
    _instance_lock = threading.Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._instance_lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._constructed = False
        return cls._instance

    def __init__(self):
        if getattr(self, "_constructed", False):
            return
        with self._instance_lock:
            if getattr(self, "_constructed", False):
                return
            self.host = db_conf.HOST
            self.port = db_conf.PORT
            self.user = db_conf.USER
            self.password = db_conf.PASSWORD
            self.database = db_conf.DATABASE
            self.pool_size = db_conf.POOL_SIZE
            self.connection_pool = Queue(maxsize=db_conf.POOL_SIZE)
            self._pool_ready = False
            self._pool_lock = threading.Lock()
            self._constructed = True

    def _new_connection(self):
        # 超时避免慢 SQL / 网络抖动无限占用连接
        return pymysql.connect(
            host=self.host,
            port=self.port,
            user=self.user,
            password=self.password,
            database=self.database,
            cursorclass=pymysql.cursors.DictCursor,
            connect_timeout=10,
            read_timeout=30,
            write_timeout=30,
        )

    def _initialize_pool(self):
        for _ in range(self.pool_size):
            self.connection_pool.put(self._new_connection())

    def _ensure_pool_sync(self):
        if self._pool_ready:
            return
        with self._pool_lock:
            if self._pool_ready:
                return
            self._initialize_pool()
            self._pool_ready = True

    async def _ensure_pool(self):
        if self._pool_ready:
            return
        await asyncio.to_thread(self._ensure_pool_sync)

    def _query_sync(self, sql, params=None):
        self._ensure_pool_sync()
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

    async def query(self, sql, params=None):
        await self._ensure_pool()
        return await asyncio.to_thread(self._query_sync, sql, params)

    def _update_sync(self, sql, params=None):
        self._ensure_pool_sync()
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

    async def update(self, sql, params=None):
        await self._ensure_pool()
        return await asyncio.to_thread(self._update_sync, sql, params)

    def _write_once_sync(self, kind, runner, sql):
        """成功返回 ('ok', None)；可重试返回 ('retry', None)；失败返回 ('fail', None)。"""
        self._ensure_pool_sync()
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            runner(conn, cursor)
            conn.commit()
            self.release_connection(conn)
            return "ok"
        except Exception as e:
            try:
                conn.rollback()
            except Exception:
                pass
            self.release_connection(conn)
            preview = _sql_preview(sql)
            if _is_lock_write_growth(e):
                logger.error(f"{kind} LOCK_WRITE_GROWTH errno=1290 sql={preview}: {e}")
                return "retry"
            logger.error(f"{kind} sql={preview}: {e}")
            return "fail"

    async def _write_with_retry(self, kind, runner, sql):
        """runner(conn, cursor) -> None；成功返回 True，失败返回 False。"""
        await self._ensure_pool()
        for attempt in range(_WRITE_RETRY + 1):
            status = await asyncio.to_thread(self._write_once_sync, kind, runner, sql)
            if status == "ok":
                return True
            if status == "retry" and attempt < _WRITE_RETRY:
                logger.error(
                    f"{kind} LOCK_WRITE_GROWTH errno=1290 "
                    f"attempt={attempt + 1}/{_WRITE_RETRY + 1} sql={_sql_preview(sql)}"
                )
                await asyncio.sleep(_WRITE_RETRY_BASE_SLEEP * (attempt + 1))
                continue
            if status == "retry":
                logger.error(
                    f"{kind} LOCK_WRITE_GROWTH errno=1290 exhausted sql={_sql_preview(sql)}"
                )
            return False
        return False

    async def insert(self, sql, params=None):
        def _run(conn, cursor):
            cursor.execute(sql, params)

        return await self._write_with_retry("InsertDataError", _run, sql)

    async def insert_batch(self, sql, params=None):
        def _run(conn, cursor):
            cursor.executemany(sql, params)

        return await self._write_with_retry("InsertDataError", _run, sql)

    def _delete_sync(self, sql, params=None):
        self._ensure_pool_sync()
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

    async def delete(self, sql, params=None):
        await self._ensure_pool()
        return await asyncio.to_thread(self._delete_sync, sql, params)

    def _execute_transaction_sync(self, operations):
        self._ensure_pool_sync()
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            for sql, params in operations:
                cursor.execute(sql, params)
            conn.commit()
            self.release_connection(conn)
            return True
        except Exception as e:
            conn.rollback()
            logger.error(f"TransactionError: {e}")
            self.release_connection(conn)
            return False

    async def execute_transaction(self, operations):
        """
        执行多步操作作为一个事务。
        operations 是一个列表，每个元素是一个 (sql, params) 元组。
        """
        await self._ensure_pool()
        return await asyncio.to_thread(self._execute_transaction_sync, operations)

    def get_connection(self):
        # 池耗尽时最多等 10s，避免无限卡住线程
        conn = self.connection_pool.get(timeout=10)
        # POOL_SIZE=1 时空闲连接易被服务端踢掉，表现为 FetchDataError: (0, '')
        try:
            conn.ping(reconnect=True)
            return conn
        except Exception as e:
            logger.error(f"MySQL ping failed, reconnecting: {e}")
            try:
                conn.close()
            except Exception:
                pass
            return self._new_connection()

    def release_connection(self, conn):
        try:
            if conn is None or not getattr(conn, "open", True):
                self.connection_pool.put(self._new_connection())
                return
        except Exception:
            self.connection_pool.put(self._new_connection())
            return
        self.connection_pool.put(conn)
