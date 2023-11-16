from genaipf.utils.mysql_utils import CollectionPool
from genaipf.utils.time_utils import get_format_time
from collections import namedtuple


# 新加用户
async def add_assistant_user(user_info):
    sql = """INSERT INTO `gpt_assistant_account` (
`outer_user_id`,
`biz_id`,
`source`,
`thread_id`,
`create_time`) VALUES(%s, %s, %s, %s, %s)"""
    res = await CollectionPool().insert(sql, user_info)
    return res


# 根据 `outer_user_id`,`biz_id`,`source`, 获取用户信息
async def get_assistant_user_info_from_db(outer_user_id, biz_id, source):
    sql = '''SELECT outer_user_id, biz_id, source, thread_id
FROM gpt_assistant_account WHERE
outer_user_id=%s
AND biz_id=%s
AND source=%s'''
    result = await CollectionPool().query(sql, (outer_user_id, biz_id, source))
    return result