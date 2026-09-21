import os

import oss2
from genaipf.utils.log_utils import logger
import traceback
from genaipf.utils.interface_error_notice_tg_bot_util import send_notice_message
import base64
import aiohttp
from typing import Optional
from urllib.parse import parse_qs, urlparse, unquote
import filetype


access_key_id = os.getenv('OSS_ACCESS_KEY_ID')
access_key_secret = os.getenv('OSS_ACCESS_KEY_SECRET')
bucket_name = os.getenv('OSS_BUCKET')
endpoint = os.getenv('OSS_ENDPOINT')

_IMG_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'image/avif,image/webp,image/apng,image/*,*/*;q=0.8',
}


def _guess_image_mime(data: bytes) -> Optional[str]:
    if not data:
        return None
    kind = filetype.guess(data)
    if kind and kind.mime.startswith('image/'):
        return kind.mime
    if len(data) >= 12 and data[:4] == b'RIFF' and data[8:12] == b'WEBP':
        return 'image/webp'
    if data[:8] == b'\x89PNG\r\n\x1a\n':
        return 'image/png'
    if data[:2] == b'\xff\xd8':
        return 'image/jpeg'
    if data[:6] in (b'GIF87a', b'GIF89a'):
        return 'image/gif'
    return None


def _unwrap_img_proxy(url: str) -> Optional[str]:
    if not url:
        return None
    try:
        u = urlparse(url)
        if 'img-proxy' not in (u.path or '').lower():
            return None
        real = (parse_qs(u.query).get('u') or [None])[0]
        return unquote(real) if real else None
    except Exception:
        return None


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

async def _fetch_image_bytes(url: str) -> bytes:
    timeout = aiohttp.ClientTimeout(total=20)
    async with aiohttp.ClientSession(timeout=timeout) as session:
        async with session.get(url, headers=_IMG_HEADERS, allow_redirects=True) as response:
            if response.status != 200:
                raise ValueError(f"请求失败，状态码: {response.status}")
            return await response.read()


async def get_image_base64(url: str) -> Optional[str]:
    """
    从指定 URL 下载图片并生成 Base64 字符串（自动识别图片类型）

    参数:
        url (str): 图片的网络地址

    返回:
        str: 带 data:image/... 前缀的 Base64 编码字符串；无法识别为图片时返回 None
    """
    try:
        image_data = await _fetch_image_bytes(url)
        mime = _guess_image_mime(image_data)
        if not mime:
            alt = _unwrap_img_proxy(url)
            if alt and alt != url:
                image_data = await _fetch_image_bytes(alt)
                mime = _guess_image_mime(image_data)
        if not mime:
            raise ValueError('无法识别为图片')
        base64_encoded = base64.b64encode(image_data).decode('utf-8')
        return f'data:{mime};base64,{base64_encoded}'
    except Exception as e:
        logger.error(f'根据url获取图片异常 {url}: {e}')
        return None
