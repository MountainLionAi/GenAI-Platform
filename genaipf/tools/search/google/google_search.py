from genaipf.utils.http_util import AsyncHTTPClient
from genaipf.conf import rag_conf
from genaipf.utils.log_utils import logger
import traceback
from genaipf.exception.customer_exception import CustomerError
from genaipf.constant.error_code import ERROR_CODE
from bs4 import BeautifulSoup,Comment
from genaipf.utils.rendered_html_util import get_rendered_html
import asyncio


class AsyncSafeList:
    def __init__(self):
        self.lock = asyncio.Lock()
        self.list = []

    async def append(self, item):
        async with self.lock:
            self.list.append(item)

    async def pop(self):
        async with self.lock:
            return self.list.pop()


async def google_search(search_content: str, num: int = 5):
    logger.info(f'call google_search search_content={search_content}, num={num}')
    url = rag_conf.GOOGLE_SEARCH_URL
    key = rag_conf.API_KEY
    cx = rag_conf.CX
    if url is None or url == "" or key is None or key == "" or cx is None or cx == "":
        raise CustomerError(status_code=ERROR_CODE['RAG_CONFIG_ERROR'])
    try:
        search_details = AsyncSafeList()
        client = AsyncHTTPClient()
        params = {"key": key, "cx": cx, "q": search_content, "num": num}
        headers = {"Content-Type": "application/json; charset=UTF-8"}
        result = await client.get_json(url, params, headers)
        if result and result.get('items') and len(result.get('items')) > 0:
            items = result.get('items')
            tasks = [get_content_by_url(item.get("link"), search_details) for item in items]
            await asyncio.gather(*tasks)
        final_details = [await search_details.pop() for _ in range(len(search_details.list))]
        return final_details
    except Exception as e:
        logger.error(f"call google search api error: \n{e}")
        logger.error(traceback.format_exc())
        return None


async def get_content_by_url(url, _search_details: AsyncSafeList):
    try:
        html_str = await get_rendered_html(url)
        if html_str:
            soup = BeautifulSoup(html_str, 'html.parser')
            body = soup.body
            body.attrs = {}
            # 移除不需要的标签
            for tag in body.find_all(['svg', 'img', 'a', 'button', 'script', 'audio', 'video', 'iframe', 'object', 'embed', 'footer', 'header', 'noscript', 'style']):
                tag.decompose()
            # 移除空标签
            for tag in body.find_all(['span', 'div', 'li', 'p', 'i']):
                if not tag.text.strip():
                    tag.decompose()
            # # 移除含有特定词汇的标签
            # keywords = ['breadcrumb', 'footer', 'header', 'download']
            # for tag in body.find_all(True):
            #     if tag is not None and tag.has_attr('class') and tag['class'] is not None:
            #         if any(keyword in ' '.join(tag['class']) for keyword in keywords):
            #             tag.decompose()
            #         else:
            #             for attr in list(tag.attrs) if tag.attrs else []:
            #                 if any(keyword in attr for keyword in keywords) or any(keyword in str(tag.attrs[attr] if tag.attrs else "") for keyword in keywords):
            #                     tag.decompose()
            #                     break
            # 移除所有标签的属性
            for tag in body.find_all(True):  # True匹配所有的tag
                tag.attrs = {}
            # 移除所有注释
            comments = soup.find_all(string=lambda text: isinstance(text, Comment))
            for comment in comments:
                comment.extract()
            content = body.decode_contents()
            if content:
                detail = {"url": url}
                detail['content'] = content
                await _search_details.append(detail)
    except Exception as e:
        logger.error(f"call get_content_by_url error, url={url}, {e}")
        logger.error(traceback.format_exc())


