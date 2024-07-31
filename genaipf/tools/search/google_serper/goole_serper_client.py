from genaipf.tools.search.utils.apikey_manager import get_api_key_by_type, set_api_key_unavaiable
from metaphor_python import Metaphor
from genaipf.utils.common_utils import sync_to_async
from genaipf.utils.log_utils import logger
from genaipf.utils.http_util import AsyncHTTPClient
from genaipf.dispatcher.prompts_common import LionPromptCommon
from genaipf.dispatcher.utils import simple_achat

CLIENT_TYPE = 'google_serper'
REQUEST_URL = 'https://google.serper.dev/search'
REQUEST_URL_NEWS = 'https://google.serper.dev/news'

class GoogleSerperClient:
    _api_key = None
    _instance = None
    _client = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(GoogleSerperClient, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        self._api_key = get_api_key_by_type(CLIENT_TYPE)

    def get_current_api_key(self):
        return self._api_key

    async def search(self, question, k=5):
        logger.info(f'google serper search current key is {self._api_key}')
        type: Literal["news", "search", "places", "images"] = "search"
        search_result = []
        try:
            client = AsyncHTTPClient()
            payload = {
                "q": question,
            }
            # recent_search = LionPromptCommon.get_prompted_messages("recent_search", question)
            # is_recent = await simple_achat(recent_search)
            # if is_recent:
            #     payload["tbs"] = "qdr:w"
            logger.info(f'google serper search payload: {payload}')
            headers = {
                'X-API-KEY': self._api_key,
                'Content-Type': 'application/json'
            }
            result = await client.post_json(REQUEST_URL, payload, headers)
            return self.parse_snippets(result, type, k)
        except Exception as e:
            if '429' in str(e):
                set_api_key_unavaiable(self._api_key, CLIENT_TYPE)
            logger.error(f'google serper search error: {str(e)}')
            return search_result, ''

    async def news(self, question, k=5):
        logger.info(f'google serper search current key is {self._api_key}')
        type: Literal["news", "search", "places", "images"] = "news"
        search_result = []
        try:
            client = AsyncHTTPClient()
            payload = {
                "q": question
            }
            headers = {
                'X-API-KEY': self._api_key,
                'Content-Type': 'application/json'
            }
            result = await client.post_json(REQUEST_URL_NEWS, payload, headers)
            return self.parse_snippets(result, type, k)
        except Exception as e:
            if '429' in str(e):
                set_api_key_unavaiable(self._api_key, CLIENT_TYPE)
            logger.error(f'google serper search error: {str(e)}')
            return search_result, ''

    def parse_snippets(self, results, type, k):
        result_key_for_type = {
            "news": "news",
            "places": "places",
            "images": "images",
            "search": "organic",
        }
        sources = []
        content = ""

        if type not in result_key_for_type:
            logger.error("error type for serper tools")
            return sources, content

        if results.get("answerBox"):
            answer_box = results.get("answerBox", {})
            if answer_box.get("answer"):
                content += answer_box.get("answer")
            elif answer_box.get("snippet"):
                content += answer_box.get("snippet").replace("\n", " ")
            elif answer_box.get("snippetHighlighted"):
                content += answer_box.get("snippetHighlighted")
            content += "\n"

        for result in results[result_key_for_type[type]][: k]:
            if "snippet" in result:
                sources.append(
                    {"title": result["title"], "url": result["link"], 'snippet':result["snippet"]}
                )
                content += result["snippet"] + "\n引用地址" + result["link"] + "\n"
        logger.info(f'google serper search sources {sources}')
        logger.info(f'google serper search content {content}')
        return sources, content
