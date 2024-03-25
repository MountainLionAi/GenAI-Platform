# 功能：http请求工具
# 作者：zgc
# 时间：2024/2/19 16:21


import aiohttp
import asyncio
from typing import Any, Dict
from datetime import datetime
import json


class AsyncHTTPClient:
    def __init__(self, timeout: int = 30):
        self.timeout = aiohttp.ClientTimeout(total=timeout)

    async def post_json(self, url: str, data: Dict[str, Any], headers: Dict[str, str] = None) -> Dict[str, Any]:
        """
        异步发起POST请求并获取JSON响应（内容类型为application/json）。

        :param url: 请求的URL
        :param data: 发送的数据
        :param headers: 请求头
        :return: JSON响应数据
        """
        async with aiohttp.ClientSession(timeout=self.timeout) as session:
            async with session.post(url, json=data, headers=headers) as response:
                response.raise_for_status()  # 如果响应状态码不是200，将抛出异常
                return await response.json()

    async def post_form(self, url: str, data: Dict[str, Any], headers: Dict[str, str] = None) -> Dict[str, Any]:
        """
        异步发起POST请求并获取JSON响应（内容类型为application/x-www-form-urlencoded）。

        :param url: 请求的URL
        :param data: 发送的表单数据
        :param headers: 请求头
        :return: JSON响应数据
        """
        if headers is None:
            headers = {}
        headers["Content-Type"] = "application/x-www-form-urlencoded; charset=UTF-8"

        async with aiohttp.ClientSession(timeout=self.timeout) as session:
            async with session.post(url, data=data, headers=headers) as response:
                response.raise_for_status()  # 如果响应状态码不是200，将抛出异常
                return await response.json()

    async def post_form_receive_text(self, url: str, data: Dict[str, Any], headers: Dict[str, str] = None) -> str:
        """
        异步发起POST请求，请求内容类型为application/x-www-form-urlencoded; charset=UTF-8，
        响应内容类型为text/plain; charset=utf-8，并获取纯文本响应。
        """
        if headers is None:
            headers = {"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"}
        async with aiohttp.ClientSession(timeout=self.timeout) as session:
            async with session.post(url, data=data, headers=headers) as response:
                response.raise_for_status()
                # 确保响应内容类型为text/plain
                if response.headers.get("Content-Type") == "text/plain; charset=utf-8":
                    return await response.text()
                else:
                    raise ValueError("Unexpected content type in response")

    async def get_json(self, url: str, params: Dict[str, Any] = None, headers: Dict[str, str] = None) -> Dict[str, Any]:
        """
        异步发起GET请求并获取JSON响应。

        :param url: 请求的URL
        :param params: URL的查询参数
        :param headers: 请求头
        :return: JSON响应数据
        """
        async with aiohttp.ClientSession(timeout=self.timeout) as session:
            async with session.get(url, params=params, headers=headers) as response:
                response.raise_for_status()
                return await response.json()
    
    
    async def get_html(self, url: str, params: Dict[str, Any] = None, headers: Dict[str, str] = None) -> str:
        """
        异步发起GET请求并获取HTML响应。

        :param url: 请求的URL
        :param params: URL的查询参数
        :param headers: 请求头
        :return: HTML响应数据
        """
        async with aiohttp.ClientSession(timeout=self.timeout) as session:
            async with session.get(url, params=params, headers=headers) as response:
                response.raise_for_status()  # 如果响应状态码不是200，将抛出异常
                # 确保响应内容类型为text/html
                if "text/html" in response.headers.get("Content-Type", ""):
                    return await response.text()
                else:
                    raise ValueError("Unexpected content type in response")
                

# 使用示例
async def main():
    client = AsyncHTTPClient()
    # url = "https://httpbin.org/post"
    #
    # # JSON请求示例
    # json_data = {"key": "value"}
    # json_headers = {"Content-Type": "application/json"}
    # try:
    #     json_response = await client.post_json(url, json_data, json_headers)
    #     print("JSON response:", json_response)
    # except Exception as e:
    #     print(f"JSON请求发生错误：{e}")

    url = "https://www.techflowpost.com/ashx/newflash_index.ashx"
    # 获取当前时间
    now = datetime.now()
    # 格式化时间
    formatted_time = now.strftime("%Y/%m/%d %H:%M:%S")
    # Form请求示例
    # form_data = {"pageindex": 1, "pagesize": 10, "time": formatted_time}
    # try:
    #     form_response = await client.post_form(url, form_data)
    #     print("Form response:", form_response)
    # except Exception as e:
    #     print(f"Form请求发生错误：{e}")

    # Form请求，期待纯文本响应示例
    form_data = {"pageindex": 1, "pagesize": 10, "time": formatted_time}
    try:
        text_response = await client.post_form_receive_text(url, form_data)
        # print("Text response:", text_response)
        json_obj = json.loads(text_response)
        if json_obj and json_obj.get('success') == 'Y' and json_obj.get('content'):
            contents = json_obj.get('content')
            contents = [{'create_time': content.get('dcreate_time'), 'surl': content.get('surl'), 'content': content.get('scontent'), 'title': content.get('stitle'), 'abstract': content.get('sabstract'), 'newflash_id': content.get('nnewflash_id')} for content in contents]
            print(json.dumps(contents, ensure_ascii=False))
    except Exception as e:
        print(f"请求发生错误：{e}")


# 运行异步主函数
if __name__ == "__main__":
    asyncio.run(main())

