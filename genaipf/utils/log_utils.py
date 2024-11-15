import logging
import os
import sys
import asyncio
from logging.handlers import TimedRotatingFileHandler
from genaipf.conf import server

LOG_PATH = server.LOG_PATH

# 处理的异步方法
async def async_error_handler(record):
    from genaipf.utils.interface_error_notice_tg_bot_util_without_logger import send_notice_message
    await send_notice_message(record.pathname, record.funcName, record.lineno, record.msg, record.levelno)

class AsyncLoggingHandler(logging.Handler):
    def __init__(self, loop, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.loop = loop

    def emit(self, record):
        try:
            if record.levelno == logging.ERROR:
                # 异步调用处理函数
                asyncio.ensure_future(async_error_handler(record))
        except Exception:
            self.handleError(record)

def get_logger():
    logger = logging.getLogger("LOGGER")
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter(
        '{"time": "%(asctime)s", "level": "%(levelname)s", "filename": "%(filename)s", "line": "%(lineno)d", "message": "%(message)s"}')

    # 获取当前事件循环
    loop = asyncio.get_event_loop()

    # 添加控制台输出处理器
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    # 添加文件输出处理器
    log_dir = LOG_PATH
    script_path = sys.argv[0]
    script_arr = script_path.split("/")
    script_name = script_arr[len(script_arr)-1]
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, f'{script_name}.log')
    handler = TimedRotatingFileHandler(log_file, when="midnight", interval=1, backupCount=365)
    handler.suffix = "%Y%m%d"
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    # 添加异步日志处理器
    # async_handler = AsyncLoggingHandler(loop)
    # async_handler.setFormatter(formatter)
    # logger.addHandler(async_handler)

    return logger

logger = get_logger()
