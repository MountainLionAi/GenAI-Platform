import os

import oss2
from genaipf.utils.log_utils import logger
import traceback
from genaipf.utils.interface_error_notice_tg_bot_util import send_notice_message

access_key_id = os.getenv('OSS_ACCESS_KEY_ID')
access_key_secret = os.getenv('OSS_ACCESS_KEY_SECRET')
bucket_name = os.getenv('OSS_BUCKET')
endpoint = os.getenv('OSS_ENDPOINT')

async def put_image(name: str, file: str):
    bucket = oss2.Bucket(oss2.Auth(access_key_id, access_key_secret), endpoint, bucket_name)
    try:
        # 上传文件
        result = bucket.put_object(name, file)
        return True
    except Exception as e:
        err_message = f"调用image_util文件put_image异常：{e}"
        logger.error(err_message)
        err_message = traceback.format_exc()
        logger.error(err_message)
        await send_notice_message('genai_claude_client', 'claude_cached_api_call', 0, err_message, 4)
        return False
