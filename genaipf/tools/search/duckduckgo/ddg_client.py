import asyncio
from genaipf.utils.log_utils import logger
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
        results = await self._client.atext(word, timelimit='w', max_results=results_num)
        return self.parse_results(results)

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
