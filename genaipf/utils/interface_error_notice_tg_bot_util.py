from genaipf.conf import tg_bot_conf
import aiogram
from genaipf.utils.log_utils import logger
from typing import List
from genaipf.utils.redis_utils import RedisConnectionPool
from genaipf.utils.email_utils import send_email

redis_client = RedisConnectionPool().get_connection()

interface_error_notice_bot = aiogram.Bot(token=tg_bot_conf.INTERFACE_ERROR_NOTICE_TG_BOT_TOKEN)

INTERFACE_ERROR_NOTICE_NUMBER_PREFIX="INTERFACE_ERROR_NOTICE_NUMBER_PREFIX_"
INTERFACE_ERROR_NOTICE_SLEEP_PREFIX="INTERFACE_ERROR_NOTICE_SLEEP_PREFIX_"

async def send_notice_message(fileName: str, method: str, code: int, message: str, level: int):
    user_name_arr = [
        'speakjan1024'
    ]
    to_email_list = [
        '497000015@qq.com'
    ]
    user_name_list = " ".join(['@'+ user_name for user_name in user_name_arr])
    text = f"""
{user_name_list}
Mlion接口代码发生异常
文件：{fileName}
方法：{method}
异常编码:{code}
异常信息:\n{message}
"""
    try:
        INTERFACE_ERROR_NOTICE_SLEEP_KEY = INTERFACE_ERROR_NOTICE_SLEEP_PREFIX + fileName + "_" + method
        notice_sleep = redis_client.get(INTERFACE_ERROR_NOTICE_SLEEP_KEY)
        if notice_sleep:
            return
        INTERFACE_ERROR_NOTICE_NUMBER_KEY = INTERFACE_ERROR_NOTICE_NUMBER_PREFIX + fileName + "_" + method
        notice_num = redis_client.get(INTERFACE_ERROR_NOTICE_NUMBER_KEY)
        print(f"notice_num={notice_num}")
        if notice_num and int(notice_num) >= tg_bot_conf.INTERFACE_ERROR_NOTICE_ALLOW_NUM:
            redis_client.set(INTERFACE_ERROR_NOTICE_SLEEP_KEY, 1, tg_bot_conf.INTERFACE_ERROR_NOTICE_ALLOW_INTERVAL_SECONDS)
            redis_client.delete(INTERFACE_ERROR_NOTICE_NUMBER_KEY)
            logger.info(f'{fileName}_{method}_{code}报警次数超过{notice_num}次，睡眠{tg_bot_conf.INTERFACE_ERROR_NOTICE_ALLOW_INTERVAL_SECONDS}秒')
            return
        else:
            redis_client.incr(INTERFACE_ERROR_NOTICE_NUMBER_KEY)
            redis_client.expire(INTERFACE_ERROR_NOTICE_NUMBER_KEY, 600)
            await interface_error_notice_bot.send_message(chat_id=tg_bot_conf.INTERFACE_ERROR_NOTICE_TG_BOT_CHAT_ID, text=text)
            if to_email_list:
                await send_notice_email(to_email_list, fileName, method, code, message)
    except Exception as e:
        logger.error(f"send interface error notice message error: {e}")



async def send_notice_email(to_email_list: List[str], fileName: str, method: str, code: int, message: str):
    try:
        subject = "Mlion接口代码异常通知"
        content = f"""
<h2>Mlion接口代码发生异常</h2>
<p>
<b>文件</b>:\t{fileName}<br><br>
<b>方法</b>:\t{method}<br><br>
<b>异常编码</b>:\t{code}<br><br>
<b>异常信息<b>:<br><br>{message}
</p>
        """
        await send_email(subject, content, ",".join(to_email_list))
    except Exception as e:
        logger.error(f"send interface error notice email error: {e}")
    
