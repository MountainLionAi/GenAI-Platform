from genaipf.utils.mysql_utils import CollectionPool


# 记录一条新消息
async def add_gpt_message(gpt_message):
    sql = "INSERT INTO `gpt_messages` (`content`, `type`, `userid`, `msggroup`, `device_no`) VALUES(%s, %s, %s, %s, %s)"
    res = await CollectionPool().insert(sql, gpt_message)
    return res

async def add_gpt_message_with_code(gpt_message):
    sql = "INSERT INTO `gpt_messages` (`content`, `type`, `userid`, `msggroup`, `code`, `device_no`, `base64_type`, `base64_content`, `quote_info`, `file_type`, `agent_id`, `regenerate_response`, `chat_time`) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    res = await CollectionPool().insert(sql, gpt_message)
    return res


async def add_gpt_message_with_code_from_share_batch(gpt_messages):
    sql = "INSERT INTO `gpt_messages` (`content`, `type`, `userid`, `msggroup`, `code`, `device_no`, `file_type`, `agent_id`) VALUES(%s, %s, %s, %s, %s, %s, %s, %s)"
    res = await CollectionPool().insert_batch(sql, gpt_messages)
    return res


# 获取用户消息列表
async def get_gpt_message(userid, msggroup):
    sql = 'SELECT id, content, type, msggroup, create_time, code FROM gpt_messages WHERE ' \
          'userid=%s AND msggroup=%s and deleted=0'
    result = await CollectionPool().query(sql, (userid, msggroup))
    return result

# 获取用户某个类型最后一条消息
async def get_gpt_message_last_by_type(userid, msggroup, type):
    sql = 'SELECT id, content, type, msggroup, create_time, code FROM gpt_messages WHERE ' \
          'userid=%s AND msggroup=%s and deleted=0 and type=%s ORDER BY id DESC LIMIT 1'
    result = await CollectionPool().query(sql, (userid, msggroup, type))
    return result

# 获取用户消息列表用作上下文
async def get_gpt_message_limit(userid, msggroup, limit):
    sql = 'SELECT id, content, type, msggroup, create_time, code, base64_type, base64_content as base64content, quote_info as quoteInfo, file_type, agent_id,regenerate_response, chat_time FROM gpt_messages WHERE ' \
          'userid=%s AND msggroup=%s and deleted=0 ORDER BY id DESC LIMIT %s'
    result = await CollectionPool().query(sql, (userid, msggroup, limit))
    if len(result) > 0 :
        result.reverse()
        if result[0]['type'] != 'user' :
            result.pop(0)
    return result

# 获取用户对话列表
async def get_msggroup(userid):
    sql = "SELECT id, content, type, msggroup, agent_id FROM gpt_messages WHERE " \
          "userid=%s and type = 'user' and deleted=0 GROUP BY msggroup"
    result = await CollectionPool().query(sql, (userid))
    return result

# 删除用户对话列表
async def del_msggroup(userid, msggroup):
    sql = 'update gpt_messages set deleted=1 WHERE ' \
          'userid=%s AND msggroup in %s and deleted=0'
    result = await CollectionPool().update(sql, (userid, msggroup))
    return result

# 删除用户对话列表
async def tw_del_msggroup(msggroup):
    sql = 'update gpt_messages set deleted=1 WHERE ' \
          'msggroup in %s and deleted=0'
    result = await CollectionPool().update(sql, (msggroup,))
    return result

async def get_predict(coin):
    sql = "SELECT date, open, high, low, close FROM kline_predictd where symbol='{}USDT' order by date desc limit 3".format(coin)
    result = await CollectionPool().query(sql)
    return result

async def set_gpt_gmessage_rate_by_id(rate, comment, code):
    sql = 'UPDATE gpt_messages set user_rate=%s, comment=%s WHERE code=%s and deleted=0'
    result = await CollectionPool().update(sql, (rate, comment, code))
    return result

async def del_gpt_message_by_code(userid,codes):
    sql = 'update gpt_messages set deleted = 1 WHERE userid=%s and code in %s and deleted=0'
    result = await CollectionPool().update(sql,(userid,codes))
    return result

async def add_share_message(code, messages, userid, summary):
    sql = "INSERT INTO `share_messages` (`code`, `messages`, `userid`, `summary`) VALUES(%s, %s, %s, %s)"
    result = await CollectionPool().insert(sql, (code, messages, userid, summary))
    return result

async def get_share_msg(code):
    sql = 'SELECT sm.id, sm.code, sm.messages, sm.summary, ui.user_name, ui.avatar_url FROM share_messages sm left join user_infos ui on sm.userid=ui.id WHERE ' \
          'code=%s'
    result = await CollectionPool().query(sql, (code))
    return result

# 获取用户某条消息
async def get_gpt_message_by_id(userid, message_id):
    sql = 'SELECT id, content, type, msggroup, create_time, code FROM gpt_messages WHERE ' \
          'userid=%s AND id=%s and deleted=0'
    result = await CollectionPool().query(sql, (userid, message_id))
    return result

# 修改用户某条消息
async def update_gpt_message_content(userid, message_id, content):
    sql = 'UPDATE gpt_messages SET content=%s WHERE ' \
          'userid=%s AND id=%s and deleted=0'
    result = await CollectionPool().update(sql, (content, userid, message_id))
    return result

# 获取用户某条消息
async def get_gpt_message_by_code(userid, code):
    sql = 'SELECT id, content, type, msggroup, create_time, code FROM gpt_messages WHERE ' \
          'userid=%s AND code=%s and deleted=0'
    result = await CollectionPool().query(sql, (userid, code))
    return result

# 修改用户某条消息
async def update_gpt_message_content_by_code(userid, code, content):
    sql = 'UPDATE gpt_messages SET content=%s WHERE ' \
          'userid=%s AND code=%s and deleted=0'
    result = await CollectionPool().update(sql, (content, userid, code))
    return result