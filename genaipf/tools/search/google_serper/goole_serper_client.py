from genaipf.tools.search.utils.apikey_manager import get_api_key_by_type, set_api_key_unavaiable
from genaipf.utils.log_utils import logger
from genaipf.utils.http_util import AsyncHTTPClient
from genaipf.tools.search.rerank.cohere_client import CohereClient
import asyncio
from genaipf.utils.interface_error_notice_tg_bot_util import send_notice_message

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

    async def search_origin(self, question, time, k=5):
        logger.info(f'google serper search current key is {self._api_key}')
        search_result = []
        try:
            client = AsyncHTTPClient()
            payload = {
                "q": question,
                "tbs": f"qdr:{time}"
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
            if result and len(result['organic']) != 0:
                search_result = result['organic']
        except Exception as e:
            if '429' in str(e):
                set_api_key_unavaiable(self._api_key, CLIENT_TYPE)
            logger.error(f'google serper search error: {str(e)}')
            await send_notice_message('google_serper_client', 'search_origin', 0, err_message, 3)
        return search_result

    async def multi_search(self, question, language):
        search_task = []
        search_sources = []
        sources_content = []
        final_sources = []
        search_task.append(self.search_origin(question, 'd', 8))
        search_task.append(self.search_origin(question, 'w', 5))
        search_task.append(self.search_origin(question, 'm', 3))
        search_res = await asyncio.gather(*search_task)
        title_keys = []
        for search_info in search_res:
            search_sources.extend(search_info)
        if search_sources and len(search_sources) != 0:
            final_sources = search_sources
            # for search_source in search_sources:
            #     if search_source['title'] in title_keys:
            #         continue
            #     sources_content.append(search_source['snippet'])
            # cohere_client = CohereClient()
            # rerank_indexes = await cohere_client.rerank(question, sources_content, language)
            # if rerank_indexes and len(rerank_indexes) != 0:
            #     for rerank_index in rerank_indexes:
            #         final_sources.append(search_sources[rerank_index])
        format_final_sources = []
        if final_sources and len(final_sources) != 0:
            for final_source in final_sources:
                tmp_source = {
                    "title": final_source['title'],
                    "href": final_source['link'],
                    "body": final_source['snippet']
                }
                format_final_sources.append(tmp_source)
        return format_final_sources


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
