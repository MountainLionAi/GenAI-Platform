from sanic.request import Request
from concurrent.futures import ThreadPoolExecutor
from sanic.response import json
import os
from dotenv import load_dotenv
load_dotenv(override=True)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

proxy = { 'https' : '127.0.0.1:8001'}

executor = ThreadPoolExecutor(max_workers=10)

async def assistant_api(request: Request):
    # 解析请求体中的JSON数据
    request_params = request.json
    userid = request_params.get("userid", "")
    biz = request_params.get("biz", "")
    source = request_params.get("source", "")
    type_ = request_params.get("type", "")
    format_ = request_params.get("format", "")
    version = request_params.get("version", "")
    content = request_params.get("content", "")

    # 业务逻辑code

    # 构造输出JSON响应
    response_data = {
        "type": type_,
        "format": format_,
        "version": version,
        "content": content
    }

    return json(response_data)