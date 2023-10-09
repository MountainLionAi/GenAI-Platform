import aiohttp


# 异步请求的http库
class AsyncHttpClient:
    def __init__(self):
        self.session = aiohttp.ClientSession()

    async def get(self, url, params=None, **kwargs):
        async with self.session.get(url, params=params, **kwargs) as response:
            return await response.text()

    async def post(self, url, data=None, json=None, **kwargs):
        async with self.session.post(url, data=data, json=json, **kwargs) as response:
            return await response.text()

    async def close(self):
        await self.session.close()
