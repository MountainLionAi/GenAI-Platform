import os
import asyncio
import base64
import time
import traceback
import urllib.error
import urllib.request
from typing import Optional
from urllib.parse import parse_qs, urlparse, unquote

import oss2
import filetype
from genaipf.utils.log_utils import logger
from genaipf.utils.interface_error_notice_tg_bot_util import send_notice_message


access_key_id = os.getenv('OSS_ACCESS_KEY_ID')
access_key_secret = os.getenv('OSS_ACCESS_KEY_SECRET')
bucket_name = os.getenv('OSS_BUCKET')
endpoint = os.getenv('OSS_ENDPOINT')

_IMG_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'image/avif,image/webp,image/apng,image/*,*/*;q=0.8',
}
# ponytail: 并发太高时 aihot/OSS 会整批空超时；4 路够用
_FETCH_SEM = asyncio.Semaphore(4)
# 套接字空闲超时：无数据读写超过该值即断（有数据持续到达可一直读）
_SOCK_IDLE_TIMEOUT = 12
# 单图绝对上限：常规 CDN/OSS 多在 1–3s，远超则强杀（防慢速滴流占坑）
_IMG_WALL_TIMEOUT = 35
_MAX_IMG_BYTES = 15 * 1024 * 1024
_READ_CHUNK = 64 * 1024


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
        bucket.put_object(name, file)
        return True
    except Exception as e:
        err_message = f"调用image_util文件put_image异常：{e}"
        logger.error(err_message)
        err_message = traceback.format_exc()
        logger.error(err_message)
        await send_notice_message('genai_claude_client', 'claude_cached_api_call', 0, err_message, 4)
        return False


def _fetch_image_bytes_sync(url: str) -> bytes:
    """空闲超时：连接/两次读之间无数据则断；有数据则继续读到结束（另有墙钟上限在外层）。"""
    req = urllib.request.Request(url, headers=_IMG_HEADERS)
    try:
        with urllib.request.urlopen(req, timeout=_SOCK_IDLE_TIMEOUT) as resp:
            status = getattr(resp, 'status', 200)
            if status != 200:
                raise ValueError(f'请求失败，状态码: {status}')
            chunks = []
            total = 0
            while True:
                chunk = resp.read(_READ_CHUNK)
                if not chunk:
                    break
                chunks.append(chunk)
                total += len(chunk)
                if total > _MAX_IMG_BYTES:
                    raise ValueError(f'图片过大 n={total}')
            return b''.join(chunks)
    except urllib.error.HTTPError as e:
        raise ValueError(f'请求失败，状态码: {e.code}') from e


async def _fetch_image_bytes(url: str) -> bytes:
    return await asyncio.to_thread(_fetch_image_bytes_sync, url)


def _candidate_urls(url: str) -> list:
    """img-proxy 常过期 403，优先直连原图，再回退 proxy。"""
    alt = _unwrap_img_proxy(url)
    if alt and alt != url:
        return [alt, url]
    return [url]


async def get_image_base64(url: str) -> Optional[str]:
    """
    从指定 URL 下载图片并生成 Base64 字符串（自动识别图片类型）。
    - 套接字空闲超时：长时间无响应则结束
    - 有数据持续到达则读完
    - 总耗时超过墙钟上限则强杀（常规 1–3s）
    """
    t0 = time.monotonic()
    last_err = None
    async with _FETCH_SEM:
        for u in _candidate_urls(url):
            try:
                image_data = await asyncio.wait_for(
                    _fetch_image_bytes(u),
                    timeout=_IMG_WALL_TIMEOUT,
                )
                mime = _guess_image_mime(image_data)
                if not mime:
                    last_err = ValueError(f'无法识别为图片 head={image_data[:16]!r} n={len(image_data)}')
                    continue
                base64_encoded = base64.b64encode(image_data).decode('utf-8')
                dt = time.monotonic() - t0
                if dt >= 5:
                    logger.warning(f'get_image_base64 slow {dt:.1f}s n={len(image_data)} {u[:160]}')
                return f'data:{mime};base64,{base64_encoded}'
            except asyncio.TimeoutError:
                last_err = TimeoutError(f'单图墙钟超时 {_IMG_WALL_TIMEOUT}s')
                logger.error(f'根据url获取图片超时 {u}: wall={_IMG_WALL_TIMEOUT}s')
            except Exception as e:
                last_err = e
                logger.error(f'根据url获取图片异常 {u}: {type(e).__name__}: {e!r}')
    dt = time.monotonic() - t0
    if last_err is not None and dt >= 5:
        logger.warning(f'get_image_base64 fail after {dt:.1f}s {url[:160]}')
    return None
