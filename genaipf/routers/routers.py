from sanic import Blueprint
from genaipf.controller import gpt, user, gptstrem, userRate, pay
from importlib import import_module
from genaipf.conf.server import PLUGIN_NAME
from genaipf.controller import assistant_api

# chatbot相关接口
blueprint_chatbot = Blueprint(name="chat_bot", url_prefix="/mpcbot")
# blueprint_chatbot.add_route(gpt.http, "/sendchat", methods=["POST"])
blueprint_chatbot.add_route(gpt.http4gpt4, "/sendchat_gpt4", methods=["POST"])


# v1版本相关接口内容
blueprint_v1 = Blueprint(name="v1_versions", url_prefix="api", version=1)

# gpt相关接口
# blueprint_v1.add_route(gpt.send_chat, "sendChat", methods=["POST"])
blueprint_v1.add_route(gpt.get_message_list, "getMessageList", methods=["GET"])
blueprint_v1.add_route(gpt.get_msggroup_list, "getMsgGroupList", methods=["GET"])
blueprint_v1.add_route(gpt.del_msggroup_list, "delMsgGroupList", methods=["POST"])
blueprint_v1.add_route(gptstrem.send_strem_chat, "sendStremChat", methods=["POST"])
blueprint_v1.add_route(userRate.user_rate, 'userRate', methods=["POST"])
blueprint_v1.add_route(userRate.del_message_by_codes, 'delMessages', methods=["POST"])
blueprint_v1.add_route(userRate.share_message, 'shareMessages', methods=["POST"])
blueprint_v1.add_route(userRate.get_share_message, 'getShareMessages', methods=["POST"])

# Assistant API 相关接口
blueprint_v1.add_route(assistant_api.assistant_chat, "assistantChat", methods=["POST"])
blueprint_v1.add_route(assistant_api.get_user_history, "getConversationHistory", methods=["POST"])


# 用户相关接口
blueprint_v1.add_route(user.login, "userLogin", methods=["POST"])
blueprint_v1.add_route(user.check_login, "checkLogin", methods=["GET"])
blueprint_v1.add_route(user.register, "register", methods=["POST"])
blueprint_v1.add_route(user.login_out, "loginOut", methods=["GET"])
blueprint_v1.add_route(user.send_verify_code, "sendVerifyCode", methods=["POST"])
blueprint_v1.add_route(user.send_verify_code_new, "sendEmailCode", methods=["POST"])
blueprint_v1.add_route(user.get_captcha, "getCaptcha", methods=["GET"])
blueprint_v1.add_route(user.verify_captcha_code, "testVerifyCode", methods=["POST"])
blueprint_v1.add_route(user.modify_password, "modifyPassword", methods=["POST"])

# 支付相关接口
blueprint_v1.add_route(pay.query_pay_card, "pay/cardInfo", methods=["GET"])
blueprint_v1.add_route(pay.check_order, "pay/orderCheck", methods=["GET"])
blueprint_v1.add_route(pay.query_user_account, "pay/account", methods=["GET"])
blueprint_v1.add_route(pay.pay_success_callback, "pay/callback", methods=["POST"])

if PLUGIN_NAME:
    plugin_submodule_name = f'{PLUGIN_NAME}.routers.entry'
    plugin_submodule = import_module(plugin_submodule_name)
    plugin_router_mapping = plugin_submodule.plugin_router_mapping
    for v in plugin_router_mapping.values():
        blueprint_v1.add_route(v["handler"], v["uri"], v["methods"])