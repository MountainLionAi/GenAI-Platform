from sanic import Sanic

from conf import server
from routers import routers
from exception.customer_error_handler import CustomerErrorHandler
from sanic_cors import CORS
from middlewares.user_token_middleware import check_user
from middlewares.user_log_middleware import save_user_log
from sanic_session import Session

Sanic(server.SERVICE_NAME)
app = Sanic.get_app()

# 增加自定义异常处理handler
app.error_handler = CustomerErrorHandler()

# 增加跨域相关组件
CORS(app, supports_credentials=True)
Session(app)

# 加载服务器配置
app.config.REQUEST_TIMEOUT = server.REQUEST_TIMEOUT
app.config.RESPONSE_TIMEOUT = server.RESPONSE_TIMEOUT
app.config.KEEP_ALIVE_TIMEOUT = server.KEEP_ALIVE_TIMEOUT
app.config.KEEP_ALIVE = server.KEEP_ALIVE
app.config.REAL_IP_HEADER = "X-Forwarded-For"

# 加载路由
app.blueprint(routers.blueprint_v1)
app.blueprint(routers.blueprint_chatbot)
app.register_middleware(check_user, "request")
app.register_middleware(save_user_log, "request")

# workers的数量可以单独设置，如果设置为fast则默认为8

if __name__ == "__main__":
    app.run(host=server.HOST, port=server.PORT, fast=True)
