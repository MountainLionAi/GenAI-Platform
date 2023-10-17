from sanic.handlers import ErrorHandler
from genaipf.exception.customer_exception import CustomerError
from genaipf.interfaces.common_response import fail


class CustomerErrorHandler(ErrorHandler):
    def default(self, request, exception):
        if isinstance(exception, CustomerError):
            return fail(exception.status_code, exception.message)
        return super().default(request, exception)
