from genaipf.conf.server import os

HOST = os.getenv("REDIS_HOST")
PORT = int(os.getenv("REDIS_PORT"))
DB = int(os.getenv("REDIS_DB"))
PASSWORD = os.getenv("REDIS_PASSWORD")