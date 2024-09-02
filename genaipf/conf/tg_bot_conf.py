import dotenv
import os

dotenv.load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
BOT_USER_NAME = os.getenv("BOT_USER_NAME")

MOUNTAIN_HOST = os.getenv("MOUNTAIN_HOST", "https://test1.mountainlion.ai/#/?")

LOCALES_FILE_PATH = os.getenv("LOCALES_FILE_PATH")
if not LOCALES_FILE_PATH:
    raise EnvironmentError("环境变量 'LOCALES_FILE_PATH' 未设置")

# 接口异常通知机器人TOKEN
INTERFACE_ERROR_NOTICE_TG_BOT_TOKEN = os.getenv("INTERFACE_ERROR_NOTICE_TG_BOT_TOKEN")
# 接口异常通知聊天ID
INTERFACE_ERROR_NOTICE_TG_BOT_CHAT_ID = os.getenv("INTERFACE_ERROR_NOTICE_TG_BOT_CHAT_ID")





