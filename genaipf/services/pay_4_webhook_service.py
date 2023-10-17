import decimal

from services import pay_order_service, user_account_service, pay_card_service
from utils.id_util import generate_snowflake_id
import traceback
from utils.log_utils import logger
from utils.redis_lock_utils import acquire_lock, release_lock
from datetime import datetime, timedelta


def computeDay2Add(card_type):
    if card_type == 3:
        return 30
    elif card_type == 4:
        return 90
    elif card_type == 5:
        return 360
    else:
        return 0


# 保存订单信息
async def saveOrder(userid: int, email: str, order_no: str, card_type: int, amount: decimal.Decimal, pay_type: str, status=2):
    """
    生成订单
    :param userid: 用户ID
    :param email: 用户支付预留邮件
    :param order_no: 订单号
    :param card_type: 卡类型：1-1次；2-15次；3-月卡；4-季卡；5-年卡
    :param amount: 金额
    :param pay_type: 支付类型：1-银行卡、2-微信、3-支付宝（这个是临时编的，看真实的都有哪些，再编码）
    :param status: 状态：1-未支付；2-已支付；3-支付失败
    :return:
    """
    global lock_name, lock_identifier
    try:
        logger.info(
            f"saveOrder params:\n userid={str(userid)}, email={email}, order_no={order_no}, card_type={str(card_type)}, amount={str(amount)}, pay_type={str(pay_type)}, status={str(status)}")
        if status != 2:  # 只有支付成功的处理，其余状态的由支付中心记录
            return
        lock_name = "save_order_" + str(userid)
        lock_identifier = acquire_lock(lock_name)
        if lock_identifier:
            order_id = generate_snowflake_id()
            pay_order = (order_id, userid, email, order_no, pay_type, card_type, amount, status)
            await pay_order_service.add_pay_order(pay_order)
            user_account = await user_account_service.select_user_account_by_userid(userid)
            pay_card = await pay_card_service.select_pay_card_by_card_type(card_type)
            if pay_card is None:
                logger.error(f'card_type={card_type} is invalid')
                return
            _day2add = computeDay2Add(card_type)
            if user_account is None or len(user_account) == 0:
                user_account_id = generate_snowflake_id()
                if card_type == 1 or card_type == 2:
                    un_terminable_card_type = card_type
                    un_terminable_time = pay_card.get('time')
                    un_terminable_time_history_total = pay_card.get('time')
                    due_date = None
                    terminable_card_type = None
                    terminable_time = None
                    terminable_time_history_total = None
                elif card_type == 3 or card_type == 4 or card_type == 5:
                    terminable_card_type = card_type
                    terminable_time = pay_card.get('time')
                    terminable_time_history_total = pay_card.get('time')
                    due_date = datetime.now() + timedelta(_day2add)
                    due_date = due_date.strftime("%Y-%m-%d %H:%M:%S")
                    un_terminable_card_type = None
                    un_terminable_time = None
                    un_terminable_time_history_total = None
                user_account = (user_account_id, userid, terminable_card_type, terminable_time, terminable_time_history_total, un_terminable_card_type,
                                un_terminable_time, un_terminable_time_history_total, due_date)
                await user_account_service.add_user_account(user_account)
            else:
                if card_type == 1 or card_type == 2:
                    un_terminable_card_type = card_type
                    _un_terminable_time = user_account.get('un_terminable_time')
                    _un_terminable_time = _un_terminable_time if _un_terminable_time is not None else 0
                    un_terminable_time = _un_terminable_time + pay_card.get('time')
                    _un_terminable_time_history_total = user_account.get('un_terminable_time_history_total')
                    _un_terminable_time_history_total = _un_terminable_time_history_total if _un_terminable_time_history_total is not None else 0
                    un_terminable_time_history_total = _un_terminable_time_history_total + pay_card.get('time')
                    await user_account_service.update_un_terminable_by_userid(userid, un_terminable_card_type,
                                                                              un_terminable_time, un_terminable_time_history_total)
                elif card_type == 3 or card_type == 4 or card_type == 5:
                    terminable_card_type = card_type
                    _terminable_time = user_account.get('terminable_time')
                    _terminable_time = _terminable_time if _terminable_time is not None else 0
                    terminable_time = _terminable_time + pay_card.get('time')
                    _terminable_time_history_total = user_account.get('terminable_time_history_total')
                    _terminable_time_history_total = _terminable_time_history_total if _terminable_time_history_total is not None else 0
                    terminable_time_history_total = _terminable_time_history_total + pay_card.get('time')
                    _due_date = user_account.get('due_date')
                    _due_date = _due_date if _due_date is not None else datetime.now()
                    due_date = _due_date + timedelta(_day2add)
                    due_date = due_date.strftime("%Y-%m-%d %H:%M:%S")
                    await user_account_service.update_terminable_by_userid(userid, terminable_card_type,
                                                                           terminable_time, terminable_time_history_total, due_date)
        else:
            logger.info("Failed to acquire lock.")
    except Exception as e:
        logger.error(traceback.format_exc())
    finally:
        if lock_identifier:
            # 释放锁
            release_lock(lock_name, lock_identifier)
            logger.info("saveOrder Lock released.")
