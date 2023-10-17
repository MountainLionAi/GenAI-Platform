from utils.mysql_utils import CollectionPool

async def save_user_log(user_id,request_ip,request_path):
    sql = "insert into user_log (user_id, user_ip, request_path) values (%s, %s, %s)"
    result = await CollectionPool().insert(sql,(user_id, request_ip, request_path))
    return result