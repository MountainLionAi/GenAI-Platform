import json

from genaipf.tools.search.utils.apikey_manager import get_api_key_by_type, set_api_key_unavaiable
from genaipf.utils.log_utils import logger
import cohere

CLIENT_TYPE = 'cohere'
DEFAULT_MODEL = 'rerank-english-v3.0'
MULTI_MODEL = 'rerank-multilingual-v3.0'
TOP_N = 4
DEFAULT_SCORE = 0.6


class CohereClient:
    _api_key = None
    _instance = None
    _client = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(CohereClient, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        self._api_key = get_api_key_by_type(CLIENT_TYPE)
        self._client = cohere.AsyncClient(self._api_key, timeout=10)

    def get_current_api_key(self):
        return self._api_key

    async def rerank(self, question, related_sources, language):
        logger.info(f'cohere rerank function current key is {self._api_key}')
        model = DEFAULT_MODEL
        if language != 'en':
            model = MULTI_MODEL
        results = []
        try:
            response = await self._client.rerank(
                model=model,
                query=question,
                documents=related_sources,
                top_n=TOP_N)
            logger.info(f'cohere rerank的返回值是: {response}')
            if response:
                response = response.json()
                response = json.loads(response)
                results = response['results']
                results = filter_rerank_info(results, question, related_sources)
            return results
        except Exception as e:
            if '429' in str(e):
                set_api_key_unavaiable(self._api_key, CLIENT_TYPE)
            logger.error(f'cohere rerank error: {str(e)}')
        return results


def filter_rerank_info(rerank_results, question, related_sources: list):
    final_sources = []
    if rerank_results and len(rerank_results) != 0:
        for rerank_result in rerank_results:
            if float(rerank_result['relevance_score']) > DEFAULT_SCORE:
                final_sources.append(related_sources[rerank_result['index']])
    logger.info(f'和问题:{question}关联度比较高的数据是: {json.dumps(final_sources)}')
    return final_sources
