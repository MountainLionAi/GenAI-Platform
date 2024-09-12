import asyncio
from genaipf.utils.log_utils import logger
from genaipf.tools.search.rerank.cohere_client import CohereClient
from duckduckgo_search import AsyncDDGS


class DuckduckgoClient:
    _instance = None
    _client = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(DuckduckgoClient, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        self._client = AsyncDDGS(proxy=None)

    async def aget_results(self, word, time_period='w', results_num=5):
        try:
            results = await self._client.atext(word, timelimit='w', max_results=results_num)
            return self.parse_results(results)
        except Exception as e:
            logger.error(f"ddg搜索失败{e}")
            return [], ""

    async def aget_results_origin(self, word, time_period='w', results_num=5):
        try:
            results = await self._client.atext(word, timelimit=time_period, max_results=results_num)
            return results
        except Exception as e:
            logger.error(f"ddg搜索原始信息失败{e}")
            return []

    async def multi_search(self, word, language):
        search_task = []
        search_sources = []
        sources_content = []
        final_sources = []
        search_task.append(self.aget_results_origin(word, time_period='d', results_num=8))
        search_task.append(self.aget_results_origin(word, time_period='w', results_num=5))
        search_task.append(self.aget_results_origin(word, time_period='m', results_num=3))
        search_res = await asyncio.gather(*search_task)
        title_keys = []
        for search_info in search_res:
            search_sources.extend(search_info)
        if search_sources and len(search_sources) != 0:
            for search_source in search_sources:
                if search_source['title'] in title_keys:
                    continue
                title_keys.append(search_source['title'])
                sources_content.append(search_source['body'])
            cohere_client = CohereClient()
            rerank_indexes = await cohere_client.rerank(word, sources_content, language)
            if rerank_indexes and len(rerank_indexes) != 0:
                for rerank_index in rerank_indexes:
                    final_sources.append(search_sources[rerank_index])
        return final_sources

    def parse_results(self, results):
        sources = []
        content = ''
        if results and len(results) != 0:
            for result in results:
                sources.append(
                    {"title": result["title"], "url": result["href"]}
                )
                content += result["body"] + "\n引用地址" + result["href"] + "\n"

        return sources, content
