from sanic import Request
import traceback
from genaipf.services import pay_card_service, pay_order_service, user_account_service_wrapper, pay_4_webhook_service
from genaipf.utils.log_utils import logger
from genaipf.interfaces.common_response import success, fail
from genaipf.constant.error_code import ERROR_CODE
from genaipf.exception.customer_exception import CustomerError


# 查询支付卡类型
async def query_pay_card(rqeuest: Request):
    try:
        pay_cards = await pay_card_service.select_pay_card_all()
        for pay_card in pay_cards:
            pay_card['real_price'] = str(pay_card['real_price'])
            pay_card['display_price'] = str(pay_card['display_price'])
        return success(pay_cards)
    except Exception as e:
        logger.error(traceback.format_exc())
        raise CustomerError(status_code=ERROR_CODE['SYSTEM_ERROR'])


# 验证订单是否成功
async def check_order(request: Request):
    userid = request.ctx.user['id']
    order_no = request.args.get('order_no')
    if order_no is None:
        raise CustomerError(status_code=ERROR_CODE['PARAMS_ERROR'])
    pay_order = pay_order_service.select_pay_order_by_order_no(userid, order_no)
    if pay_order is None:
        raise CustomerError(status_code=ERROR_CODE['ORDER_NOT_EXIST'])
    return success(pay_order.get('status'))


# 查询用户账户信息
async def query_user_account(request: Request):
    user_info = request.ctx.user
    if not user_info:
        userid = None
    else:
        userid = user_info['id']
    import ml4gp.services.points_service as points_service
    user_account_wrapper = await points_service.get_user_query_times(userid)
    # user_account = user_account_wrapper['user_account']
    # if user_account is not None:
    #     if user_account['due_date'] is not None:
    #         user_account['due_date'] = user_account['due_date'].strftime('%Y-%m-%d %H:%M:%S')
    #     if user_account['un_terminable_time'] == 0:
    #         user_account['un_terminable_time'] = None
    return success(user_account_wrapper)


# 支付中心的成功回调
async def pay_success_callback(request: Request):
    """
        支付回调
        :param request:
        :return:
        """
    param = request.json
    _userid = int(param.get('userid'))
    _email = param.get('email')
    _order_no = param.get('order_no')
    _card_type = int(param.get('card_type'))
    _amount = param.get('amount')
    _pay_type = param.get('pay_type')
    _status = int(param.get('status'))
    await pay_4_webhook_service.saveOrder(_userid, _email, _order_no, _card_type, _amount, _pay_type, _status)
    return success(None)
