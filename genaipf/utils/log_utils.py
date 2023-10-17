import logging
import os
import sys
from logging.handlers import TimedRotatingFileHandler
from genaipf.conf import server

LOG_PATH = server.LOG_PATH


def get_logger():
    logger = logging.getLogger("LOGGER")
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter(
        '{"time": "%(asctime)s", "level": "%(levelname)s", "filename": "%(filename)s", "line": "%(lineno)d", "message": "%(message)s"}')

    # 添加控制台输出处理器
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    # 添加文件输出处理器
    log_dir = LOG_PATH
    # 获取当前脚本名称
    script_path = sys.argv[0]
    script_arr = script_path.split("/")
    script_name = script_arr[len(script_arr)-1]
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, f'{script_name}.log')
    handler = TimedRotatingFileHandler(log_file, when="midnight", interval=1, backupCount=365)
    handler.suffix = "%Y%m%d"
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger


logger = get_logger()
