import os

import oss2
from genaipf.utils.log_utils import logger
import traceback
from genaipf.utils.interface_error_notice_tg_bot_util import send_notice_message
import base64
import aiohttp
import asyncio
from io import BytesIO

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

async def get_image_base64(url):
    """
    从指定的 URL 获取图片并生成 Base64 格式

    :param url: 图片的 URL
    :return: 图片的 Base64 字符串
    """
    try:
        # 异步发送 HTTP 请求获取图片数据
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=10) as response:
                # 检查响应状态
                if response.status != 200:
                    raise ValueError(f"Failed to fetch image, status code: {response.status}")

                # 确保是图片类型
                content_type = response.headers.get('Content-Type', '')
                if 'image' not in content_type:
                    raise ValueError("URL does not point to an image.")

                # 读取图片数据并编码为 Base64
                image_data = await response.read()
                base64_encoded = base64.b64encode(image_data).decode('utf-8')

                # 生成 HTML 标签可用的 Base64 格式
                base64_with_prefix = f"data:{content_type};base64,{base64_encoded}"

                # 返回 Base64 编码字符串
                return base64_with_prefix
    except Exception as e:
        logger.error(f'获取url链接生成base64格式失败，url: {url}, 错误: {e}')
        return ''