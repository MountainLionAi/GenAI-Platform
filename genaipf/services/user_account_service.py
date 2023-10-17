from utils.mysql_utils import CollectionPool
import threading

account_lock = threading.Lock()


# 新增用户账户
async def add_user_account(user_account):
    sql = 'INSERT INTO `user_account` (`id`, `userid`, `terminable_card_type`, `terminable_time`, ' \
          '`terminable_time_history_total`, `un_terminable_card_type`, `un_terminable_time`, ' \
          '`un_terminable_time_history_total`, `due_date`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)'
    res = await CollectionPool().insert(sql, user_account)
    return res


# 根据用户ID查询用户账户
async def select_user_account_by_userid(user_id):
    sql = 'select id, userid, terminable_card_type, terminable_time, terminable_time_history_total, ' \
          'un_terminable_card_type, un_terminable_time, un_terminable_time_history_total, due_date from user_account ' \
          'where userid=%s'
    result = await CollectionPool().query(sql, user_id)
    if result is None or len(result) == 0:
        return None
    return result[0]


# 根据用户ID更新用户账户的有期限的卡类型和有期限的卡次数和有期限的卡总充值次数
async def update_terminable_by_userid(user_id, terminable_card_type, terminable_time, terminable_time_history_total, due_date):
    with account_lock:
        sql = 'update `user_account` set `terminable_card_type` = %s, `terminable_time` = %s, ' \
              '`terminable_time_history_total` = %s, `due_date`=%s where `userid`=%s'
        res = await CollectionPool().update(sql, (terminable_card_type, terminable_time, terminable_time_history_total, due_date, user_id))
        return res


# 根据用户ID更新用户账户的有期限的卡次数
async def update_terminable_time_by_userid(user_id, terminable_time):
    with account_lock:
        sql = 'update `user_account` set `terminable_time` = %s where `userid`=%s'
        res = await CollectionPool().update(sql, (terminable_time, user_id))
        return res


# 根据用户ID更新用户账户的无期限的卡类型和无期限的卡次数和无期限的卡充值总次数
async def update_un_terminable_by_userid(user_id, un_terminable_card_type, un_terminable_time, un_terminable_time_history_total):
    with account_lock:
        sql = 'update `user_account` set `un_terminable_card_type` = %s, `un_terminable_time` = %s, ' \
              '`un_terminable_time_history_total` = %s where `userid`=%s'
        res = await CollectionPool().update(sql, (un_terminable_card_type, un_terminable_time, un_terminable_time_history_total, user_id))
        return res


# 根据用户ID更新用户账户的无期限的卡次数
async def update_un_terminable_time_by_userid(user_id, un_terminable_time):
    with account_lock:
        sql = 'update `user_account` set `un_terminable_time` = %s where `userid`=%s'
        res = await CollectionPool().update(sql, (un_terminable_time, user_id))
        return res