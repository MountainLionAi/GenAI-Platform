import json

from utils.mysql_utils import CollectionPool
from utils.log_utils import logger


# 新增订单
async def add_pay_order(pay_order):
    sql = 'INSERT INTO `pay_order` (`id`, `userid`, `email`, `order_no`, `pay_type`, `card_type`, `amount`, ' \
          '`status`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)'
    res = await CollectionPool().insert(sql, pay_order)
    return res


# 根据用户ID和订单号查询订单
async def select_pay_order_by_order_no(userid, order_no):
    sql = 'SELECT id, userid, order_no, pay_type, card_type, amount, `status` from pay_order where userid=%s and ' \
          'order_no=%s'
    result = await CollectionPool().query(sql, userid, order_no)
    return result


# 根据订单号更新订单状态
async def update_pay_order_status_by_order_no(order_no, status):
    sql = 'UPDATE `pay_order` set `status` = %s where `order_no`=%s'
    res = await CollectionPool().update(sql, (status, order_no))
    return res


