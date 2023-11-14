from sanic.request import Request
from sanic.response import json

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