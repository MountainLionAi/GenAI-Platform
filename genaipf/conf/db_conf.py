from genaipf.conf.server import os

HOST = os.getenv("MYSQL_HOST")
PORT = int(os.getenv("MYSQL_PORT"))
USER = os.getenv("MYSQL_USER")
PASSWORD = os.getenv("MYSQL_PASSWORD")
DATABASE = os.getenv("MYSQL_DATABASE")
POOL_SIZE = 1
