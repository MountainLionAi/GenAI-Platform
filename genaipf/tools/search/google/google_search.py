from genaipf.utils.http_util import AsyncHTTPClient
from genaipf.conf import rag_conf
from genaipf.utils.log_utils import logger
import traceback
from genaipf.exception.customer_exception import CustomerError
from genaipf.constant.error_code import ERROR_CODE
from bs4 import BeautifulSoup


async def google_search(search_content: str, num: int = 5):
    logger.info(f'call google_search search_content={search_content}, num={num}')
    url = rag_conf.GOOGLE_SEARCH_URL
    key = rag_conf.API_KEY
    cx = rag_conf.CX
    if url is None or url == "" or key is None or key == "" or cx is None or cx == "":
        raise CustomerError(status_code=ERROR_CODE['RAG_CONFIG_ERROR'])
    try:
        search_details = []
        client = AsyncHTTPClient()
        params = {"key": key, "cx": cx, "q": search_content, "num": num}
        headers = {"Content-Type": "application/json; charset=UTF-8"}
        result = await client.get_json(url, params, headers)
        if result and result.get('items') and len(result.get('items')) > 0:
            items = result.get('items')
            for item in items:
                link = item.get("link")
                content = await get_content_by_url(link)
                if content:
                    detail = {"url": link}
                    detail['content'] = content
                    search_details.append(detail)
        return search_details
    except Exception as e:
        logger.error(f"call google search api error: \n{e}")
        logger.error(traceback.format_exc())
        return None
    

async def get_content_by_url(url):
    headers = {"Content-Type": "text/html; charset=utf-8"}
    client = AsyncHTTPClient()
    try:
        html_str = await client.get_html(url, None, headers)
        if html_str:
            soup = BeautifulSoup(html_str, 'html.parser')
            body = soup.body
            return body.decode_contents()
    except Exception as e:
        logger.error(f"call get_content_by_url error, url={url}, {e}")
        logger.error(traceback.format_exc())
    return ""