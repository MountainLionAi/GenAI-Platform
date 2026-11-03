import aiohttp

# 默认超时，避免上游挂死拖住请求（调用方可在 kwargs 覆盖 timeout）
_DEFAULT_TIMEOUT = aiohttp.ClientTimeout(total=15, sock_connect=5)


# 异步请求的http库
class AsyncHttpClient:
    def __init__(self, timeout=None):
        self.session = aiohttp.ClientSession(timeout=timeout or _DEFAULT_TIMEOUT)

    async def get(self, url, params=None, **kwargs):
        async with self.session.get(url, params=params, **kwargs) as response:
            return await response.text()

    async def post(self, url, data=None, json=None, **kwargs):
        async with self.session.post(url, data=data, json=json, **kwargs) as response:
            return await response.text()

    async def close(self):
        await self.session.close()
