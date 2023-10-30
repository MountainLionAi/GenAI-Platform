from genaipf.services import daily_allowance_service, user_account_service, user_service
from datetime import datetime
from genaipf.utils.redis_lock_utils import acquire_lock, release_lock
from genaipf.utils.log_utils import logger


async def query_user_account_by_userid(user_id):
    """
    获取用户账户信息（包含每日限免次数）
    :param user_id:
    :return:
    """
    is_new_user = True
    user_infos = await user_service.get_user_info_by_userid(user_id)
    if user_infos:
        user_info = user_infos[0]
        time1 = user_info['create_time'].strftime('%Y-%m-%d')
        time2 = datetime.now().strftime('%Y-%m-%d')
        is_new_user = time1 == time2
    allowance_num = await daily_allowance_service.get_daily_allowance(user_id, is_new_user)
    user_account = await user_account_service.select_user_account_by_userid(user_id)
    if user_account is not None and user_account['due_date'] is not None and datetime.now() > user_account['due_date']:
        await expire_due_date_reset(user_id)
        user_account['due_date'] = None
        user_account['terminable_card_type'] = None
        user_account['terminable_time'] = None
        user_account['terminable_time_history_total'] = None
    return {
        "allowance_num": allowance_num,
        "user_account": user_account
    }


async def get_user_can_use_time(user_id):
    """
    获取用户可以使用的次数
    :param user_id:
    :return:
    """
    result = 0
    user_account_wrapper = await query_user_account_by_userid(user_id)
    user_account = user_account_wrapper['user_account']
    if user_account is not None:
        if user_account['due_date'] is not None and datetime.now() < user_account['due_date']:
            terminable_time = user_account['terminable_time']
            if terminable_time is not None and terminable_time > 0:
                result += terminable_time
        un_terminable_time = user_account['un_terminable_time']
        if un_terminable_time is not None and un_terminable_time > 0:
            result += un_terminable_time
    allowance_num = user_account_wrapper['allowance_num']
    if allowance_num > 0:
        result += allowance_num
    return result


async def expire_due_date_reset(user_id):
    """
    超期设置用户有期限属性为None
    :param user_id: 用户ID
    :return:
    """
    await user_account_service.update_terminable_by_userid(user_id, None, None, None, None)


async def minus_one_user_can_use_time(user_id):
    """
    用户可使用次数减1
    :param user_id: 用户ID
    :return:
    """
    global lock_identifier, lock_name
    try:
        lock_name = "minus_one_user_can_use_time_" + str(user_id)
        lock_identifier = acquire_lock(lock_name)
        user_account_wrapper = await query_user_account_by_userid(user_id)
        if lock_identifier:
            free_minus_status = await daily_allowance_service.daily_allowance_minus_one(user_id)
            if free_minus_status:
                return
            user_account = user_account_wrapper['user_account']
            if user_account is not None:
                terminable_time = user_account['terminable_time']
                if terminable_time is not None and terminable_time > 0:
                    await user_account_service.update_terminable_time_by_userid(user_id, terminable_time - 1)
                    return
                un_terminable_time = user_account['un_terminable_time']
                if un_terminable_time is not None and un_terminable_time > 0:
                    await user_account_service.update_un_terminable_time_by_userid(user_id, un_terminable_time - 1)
                    return
    finally:
        if lock_identifier:
            # 释放锁
            release_lock(lock_name, lock_identifier)
            logger.info("minus_one_user_can_use_time Lock released.")
