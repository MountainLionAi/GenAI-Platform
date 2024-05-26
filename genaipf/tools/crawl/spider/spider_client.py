from spider import Spider
import os
from genaipf.conf.server import SPIDER_API_KEY

class SpiderClient:
    _api_key = None
    _instance = None
    _client = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(SpiderClient, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        self._api_key = SPIDER_API_KEY
        self._client = Spider(api_key=self._api_key)

    def get_client(self):
        if self._client is not None:
            return self._client
        else:
            self._api_key = SPIDER_API_KEY
            self._client = Spider(api_key=self._api_key)
            return self._client

    async def crawl_url(self, url, limit=1):
        crawl_params = {
            'limit': limit,
            'request': 'smart_mode'
        }
        crawl_result = self._client.crawl_url(url, params=crawl_params)
        return crawl_result

    async def scrape_url(self, url, limit=1):
        scrape_result = self._client.scrape_url(url)
        return scrape_result