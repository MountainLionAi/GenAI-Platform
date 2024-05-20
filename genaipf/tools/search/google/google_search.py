from genaipf.utils.http_util import AsyncHTTPClient
from genaipf.conf import rag_conf
from genaipf.utils.log_utils import logger
import traceback
from genaipf.exception.customer_exception import CustomerError
from genaipf.constant.error_code import ERROR_CODE
from genaipf.utils.html_cleanout_util import cleanout
from genaipf.utils.rendered_html_util import get_rendered_html
import asyncio
import time
# from genaipf.tools.search.utils.search_task_manager import summarize_urls


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



# async def google_search_summarize_by_llm(search_content: str, num: int=5):
#     logger.info(f'call google_search_summarize_by_llm search_content={search_content}, num={num}')
#     url = rag_conf.GOOGLE_SEARCH_URL
#     key = rag_conf.API_KEY
#     cx = rag_conf.CX
#     if url is None or url == "" or key is None or key == "" or cx is None or cx == "":
#         raise CustomerError(status_code=ERROR_CODE['RAG_CONFIG_ERROR'])
#     try:
#         client = AsyncHTTPClient()
#         params = {"key": key, "cx": cx, "q": search_content, "num": num}
#         headers = {"Content-Type": "application/json; charset=UTF-8"}
#         result = await client.get_json(url, params, headers)
#         if result and result.get('items') and len(result.get('items')) > 0:
#             items = result.get('items')
#             urls = [[item.get("link")] for item in items]
#             summary = await summarize_urls(urls)
#             if len(summary) > 0:
#                 details = [{"url": su[0][0], "content": su[1]} for su in summary]
#                 return details
#             return []
#     except Exception as e:
#         logger.error(f"call google_search_summarize_by_llm error: \n{e}")
#         logger.error(traceback.format_exc())
#         return None


async def google_search(search_content: str, num: int = 5, language = None, site_search = None):
    logger.info(f'call google_search search_content={search_content}, num={num}')
    url = rag_conf.GOOGLE_SEARCH_URL
    key = rag_conf.API_KEY
    cx = rag_conf.CX
    if url is None or url == "" or key is None or key == "" or cx is None or cx == "":
        raise CustomerError(status_code=ERROR_CODE['RAG_CONFIG_ERROR'])
    sources = []
    content = ""
    try:
        search_details = AsyncSafeList()
        client = AsyncHTTPClient()
        if site_search:
            params = {"key": key, "cx": cx, "q": search_content, "num": num, "siteSearch": site_search, "siteSearchFilter": "i"}    
        else:
            params = {"key": key, "cx": cx, "q": search_content, "num": num}
        logger.info(f'google search params:{params}')

        if language:
            params["lr"] = language
        headers = {"Content-Type": "application/json; charset=UTF-8"}
        result = await client.get_json(url, params, headers)
        if result and result.get('items') and len(result.get('items')) > 0:
            items = result.get('items')
            tasks = [get_content_by_url(item.get("link"), item.get("title"), search_details) for item in items]
            items_link = []
            for item in items:
                items_link.append(item.get("link"))
            logger.info(f'google search items link:{items_link}')
            await asyncio.gather(*tasks)
        final_details = [await search_details.pop() for _ in range(len(search_details.list))]
        for result in final_details:
            sources.append({"title": result.get("title"), "url": result.get("url")})
            content += result.get("content") + "\n引用地址" + result.get("url") + "\n"
        logger.info(f'google search site_search:{site_search}, sources:{sources}')
        return sources, content
    except Exception as e:
        logger.error(f"call google_search error: \n{e}")
        logger.error(traceback.format_exc())
        return sources, content


async def get_content_by_url(url, title, _search_details: AsyncSafeList = None):
    try:
        html_str = await get_rendered_html(url)
        if html_str:
            cleanout_start_time = time.perf_counter()
            content = cleanout(html_str)
            cleanout_end_time = time.perf_counter()
            elapsed_cleanout_time = (cleanout_end_time - cleanout_start_time) * 1000
            logger.info(f'=====================>cleanout耗时：{elapsed_cleanout_time:.3f}毫秒')
            if content:
                detail = {"url": url, "title": title}
                detail['content'] = content
                await _search_details.append(detail)
    except Exception as e:
        logger.error(f"call get_content_by_url error, url={url}, {e}")
        logger.error(traceback.format_exc())


