import pymysql
import pymysql.cursors
from queue import Queue
from genaipf.conf import bot_conf
from genaipf.utils.log_utils import logger
import requests

class CollectionPool:
    def __init__(self):
        self.host = bot_conf.HOST
        self.port = bot_conf.PORT
        self.user = bot_conf.USER
        self.password = bot_conf.PASSWORD
        self.database = bot_conf.DATABASE
        self.pool_size = bot_conf.POOL_SIZE
        self.connection_pool = Queue(maxsize=bot_conf.POOL_SIZE)
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
        except Exception as e:
            logger.error(f"UpdateDataError: {e}")
            self.release_connection(conn)
            return False

    # 插入数据
    async def insert(self, sql, params=None):
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(sql, params)
            conn.commit()
            self.release_connection(conn)
        except Exception as e:
            logger.error(f"InsertDataError: {e}")
            self.release_connection(conn)
            return False

    # 删除数据
    async def delete(self, sql, params=None):
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(sql, params)
            conn.commit()
            self.release_connection(conn)
        except Exception as e:
            logger.error(f"DeleteDataError: {e}")
            self.release_connection(conn)
            return False

    # 获取数据库连接
    def get_connection(self):
        return self.connection_pool.get()

    # 释放数据库连接
    def release_connection(self, conn):
        self.connection_pool.put(conn)



def get_news_by_api():
    news = ""
    url = []
    try:
        res = requests.get(
            "https://api.theblockbeats.news/v1/open-api/open-flash?size=10&page=1&type=push&lang=cn").json()
        if res['status'] == 0:
            for i in res['data']['data']:
                news += '-[' + i["title"] + ']\n'
                news += '(' + i["url"] if len(i["url"]) > 0 else i["link"]
                news += ')'
                news += "\n\n"
        return news
    except Exception as e:
        logger.error("getting news by restful error")
        return news
