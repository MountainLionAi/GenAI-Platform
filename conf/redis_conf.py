import os
from dotenv import load_dotenv
load_dotenv()
# os.getenv("")

HOST = os.getenv("REDIS_HOST")
PORT = int(os.getenv("REDIS_PORT"))
DB = int(os.getenv("REDIS_DB"))
PASSWORD = os.getenv("REDIS_PASSWORD")