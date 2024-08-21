import argparse
from sanic import Sanic

from genaipf.conf import server
from genaipf.routers import routers
from genaipf.exception.customer_error_handler import CustomerErrorHandler
from sanic_cors import CORS
from genaipf.middlewares.user_token_middleware import check_user
from genaipf.middlewares.user_log_middleware import save_user_log
from genaipf.middlewares.api_key_middleware import check_api_key
from sanic_session import Session
from genaipf.bot.tg.tg_ai_bot import tgAiBot

Sanic(server.SERVICE_NAME)
app = Sanic.get_app()
# print(sanic.log.LOGGING_CONFIG_DEFAULTS)
# 增加自定义异常处理handler
app.error_handler = CustomerErrorHandler()

# 增加跨域相关组件
CORS(app, resources={
    r"/v1/api/*": {"origins": "*"},  # 允许所有来源访问 /v1/api/ 下的路径
    r"/static": {"origins": "*"}      # 允许所有来源访问 /static 路径
}, supports_credentials=True)
Session(app)

# 加载服务器配置
app.config.REQUEST_TIMEOUT = server.REQUEST_TIMEOUT
app.config.RESPONSE_TIMEOUT = server.RESPONSE_TIMEOUT
app.config.KEEP_ALIVE_TIMEOUT = server.KEEP_ALIVE_TIMEOUT
app.config.KEEP_ALIVE = server.KEEP_ALIVE
app.config.REAL_IP_HEADER = "X-Forwarded-For"

app.static('/static', server.STATIC_PATH)

# 加载路由
app.blueprint(routers.blueprint_v1)
app.blueprint(routers.blueprint_chatbot)
app.register_middleware(check_api_key, "request")
app.register_middleware(check_user, "request")
app.register_middleware(save_user_log, "request")

# parameter for different modes
parser = argparse.ArgumentParser(description=f"{server.SERVICE_NAME} usage",
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("-a", "--addvectordb", action="store_true", help="add vector db mode")
parser.add_argument("-b", "--nobot", action="store_true", help="disable bot mode")
args = parser.parse_args()
# args.addvectordb
config = vars(args)

@app.listener('after_server_start')
async def start_bot(app, loop):
    if not args.nobot:
        await tgAiBot.startup()

if __name__ == "__main__":
    '''
    python app.py -a # add dispatcher/vdb_pairs to vector db
    python app.py # run server
    python app.py -b # run server without bot
    '''
    if args.addvectordb:
        from genaipf.dispatcher.create_vdb import update_all_vdb
        update_all_vdb()
    else:
        if server.IS_INNER_DEBUG:
            app.run(host=server.HOST, port=server.PORT)
        else:
            # workers的数量可以单独设置，如果设置为fast则默认为8
            # app.run(host=server.HOST, port=server.PORT, fast=True)
            app.run(host=server.HOST, port=server.PORT, workers=2)
