from genaipf.conf.server import os

HOST = os.getenv("DB_HOST")
PORT = int(os.getenv("DB_PORT"))
USER = os.getenv("DB_USER")
PASSWORD = os.getenv("DB_PASSWORD")
DATABASE = os.getenv("DB_DATABASE")
POOL_SIZE = 1
