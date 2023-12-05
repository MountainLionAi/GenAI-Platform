from sanic import response
from genaipf.constant.error_code import ERROR_CODE, ERROR_MESSAGE


# 成功返回
def success(data, message="success", status="true", code=200):
    format_response = {
        "code": code,
        "data": data,
        "message": message,
        "status": status
    }
    return response.json(format_response)


# 错误返回
def fail(code=500, message="fail", status="false"):
    format_response = {
        "code": code,
        "message": ERROR_MESSAGE[code] + " " + message,
        "status": status
    }
    return response.json(format_response)
