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


def success_for_path(data, message="Success", code='100'):
    format_response = {
        "resCode": code,
        "resMsg": message,
        "data": data,
    }
    return response.json(format_response)

# 错误返回
def fail_for_path(code='500', message="fail", data=''):
    format_response = {
        "resCode": code,
        "resMsg": f'{data} {message}',
    }
    return response.json(format_response)
