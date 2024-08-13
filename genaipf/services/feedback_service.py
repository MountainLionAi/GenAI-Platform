from genaipf.utils.mysql_utils import CollectionPool

async def save_feedback(info):
    sql = "INSERT INTO `feedback` (`seriousness`, `type`, `bug_location`, `content`, `base64_content`, `userid`, `contact`) VALUES(%s, %s, %s, %s, %s, %s, %s)"
    res = await CollectionPool().insert(sql, info)
    return res