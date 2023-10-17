from utils.mysql_utils import CollectionPool


# 查询会员卡信息
async def select_pay_card_all():
    sql = 'select card_type, card_name, real_price, display_price, `time` from pay_card where status=0'
    result = await CollectionPool().query(sql)
    return result


# 根据card_type查询会员卡信息
async def select_pay_card_by_card_type(card_type):
    sql = 'select card_type, real_price, display_price, `time` from pay_card where card_type=%s'
    result = await CollectionPool().query(sql, card_type)
    if result is None or len(result) == 0:
        return None
    return result[0]
