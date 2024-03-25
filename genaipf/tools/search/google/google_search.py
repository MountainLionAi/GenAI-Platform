from genaipf.utils.http_util import AsyncHTTPClient
from genaipf.conf import rag_conf
from genaipf.utils.log_utils import logger
import traceback
from genaipf.exception.customer_exception import CustomerError
from genaipf.constant.error_code import ERROR_CODE


async def google_search(search_content: str, num: int = 5):
    logger.info(f'call google_search search_content={search_content}, num={num}')
    url = rag_conf.GOOGLE_SEARCH_URL
    key = rag_conf.API_KEY
    cx = rag_conf.CX
    if url is None or url == "" or key is None or key == "" or cx is None or cx == "":
        raise CustomerError(status_code=ERROR_CODE['RAG_CONFIG_ERROR'])
    try:
        client = AsyncHTTPClient()
        params = {"key": key, "cx": cx, "q": search_content, "num": num}
        result = client.get_json(url, params)

    except Exception as e:
        logger.error(f"call google search api error: \n{e}")
        logger.error(traceback.format_exc())
