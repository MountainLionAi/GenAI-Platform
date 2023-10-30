from genaipf.utils.redis_utils import RedisConnectionPool
from genaipf.utils import time_utils
import json

DAILY_ALLOWANCE_PREFIX = 'DAILY_ALLOWANCE_'
redis_client = RedisConnectionPool().get_connection()


async def get_daily_allowance(userid, is_new_user):
    """
    查询用户每天限免次数
    :param userid: 用户ID
    :param is_new_user: 是否是当天注册新用户
    :return: 每天限免次数
    """
    num = 2
    if is_new_user:
        num = 5

    daily_allowance_key = DAILY_ALLOWANCE_PREFIX + str(userid)
    dailyAllowance = redis_client.get(daily_allowance_key)
    if dailyAllowance is None or dailyAllowance == '':
        dailyAllowance = {
            "date": time_utils.get_format_time_YYYY_mm_dd(),
            "num": num
        }
        redis_client.set(daily_allowance_key, json.dumps(dailyAllowance), 60 * 60 * 24)
        return num
    else:
        _dailyAllowance = json.loads(dailyAllowance)
        if _dailyAllowance['date'] == time_utils.get_format_time_YYYY_mm_dd():
            return _dailyAllowance['num']
        else:
            dailyAllowance = {
                "date": time_utils.get_format_time_YYYY_mm_dd(),
                "num": num
            }
            redis_client.set(daily_allowance_key, json.dumps(dailyAllowance), 60 * 60 * 24)
            return num


async def daily_allowance_minus_one(userid):
    """
    用户每天限免次数减1
    :param userid:
    :return:
    """
    daily_allowance_key = DAILY_ALLOWANCE_PREFIX + str(userid)
    dailyAllowance = redis_client.get(daily_allowance_key)
    minus_status = False
    if dailyAllowance is None or dailyAllowance == '':
        dailyAllowance = {
            "date": time_utils.get_format_time_YYYY_mm_dd(),
            "num": 1
        }
        redis_client.set(daily_allowance_key, json.dumps(dailyAllowance), 60 * 60 * 24)
        minus_status = True
    else:
        _dailyAllowance = json.loads(dailyAllowance)
        if _dailyAllowance['date'] == time_utils.get_format_time_YYYY_mm_dd():
            if _dailyAllowance['num'] != 0:
                _dailyAllowance['num'] = _dailyAllowance['num'] - 1
                redis_client.set(daily_allowance_key, json.dumps(_dailyAllowance), 60 * 60 * 24)
                minus_status = True
        else:
            dailyAllowance = {
                "date": time_utils.get_format_time_YYYY_mm_dd(),
                "num": 1
            }
            redis_client.set(daily_allowance_key, json.dumps(dailyAllowance), 60 * 60 * 24)
            minus_status = True
    return minus_status
