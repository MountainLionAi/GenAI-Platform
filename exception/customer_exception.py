from sanic import SanicException


class CustomerError(SanicException):
    status_code = 500
