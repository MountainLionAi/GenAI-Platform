import os

import oss2
from genaipf.utils.log_utils import logger
import traceback
from genaipf.utils.interface_error_notice_tg_bot_util import send_notice_message
import base64
import aiohttp
import asyncio
from io import BytesIO
from typing import Optional
import filetype


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

async def get_image_base64(url: str) -> Optional[str]:
    """
    从指定 URL 下载图片并生成 Base64 字符串（自动识别图片类型）

    参数:
        url (str): 图片的网络地址

    返回:
        str: 带 data:image/... 前缀的 Base64 编码字符串；无法识别为图片时返回 ''
    """
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=10) as response:
                if response.status != 200:
                    raise ValueError(f"请求失败，状态码: {response.status}")

                # 读取内容
                image_data = await response.read()

                # 使用 filetype 判断实际内容 MIME 类型
                kind = filetype.guess(image_data)
                if not kind or not kind.mime.startswith("image/"):
                    raise ValueError(f"无法识别为图片，返回类型: {kind.mime if kind else '未知'}")

                # 编码为 base64 并拼接 data URI
                base64_encoded = base64.b64encode(image_data).decode('utf-8')
                base64_with_prefix = f"data:{kind.mime};base64,{base64_encoded}"
                return base64_with_prefix
    except Exception as e:
        logger.error("根据url获取图片异常", e)
        return None
