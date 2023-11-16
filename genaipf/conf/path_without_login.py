from importlib import import_module
from genaipf.conf.server import PLUGIN_NAME

# 不需要登陆态的接口元组
PATH_WITHOUT_LOGIN = (
    '/v1/api/sendVerifyCode',
    '/v1/api/userLogin',
    '/v1/api/register',
    '/v1/api/getCaptcha',
    '/v1/api/testVerifyCode',
    '/v1/api/sendEmailCode',
    '/v1/api/modifyPassword',
    '/v1/api/sendChat',
    '/v1/api/getMessageList',
    '/v1/api/getMsgGroupList',
    '/v1/api/sendStremChat',
    '/v1/api/getShareMessages',
    '/v1/api/pay/cardInfo',
    '/v1/api/pay/callback',
    
    '/v1/api/assistantChat',
    '/v1/api/getConversationHistory',
)

if PLUGIN_NAME:
    plugin_submodule_name = f'{PLUGIN_NAME}.routers.without_login'
    plugin_submodule = import_module(plugin_submodule_name)
    without_login = plugin_submodule.WITHOUT_LOGIN
    PATH_WITHOUT_LOGIN = PATH_WITHOUT_LOGIN + without_login