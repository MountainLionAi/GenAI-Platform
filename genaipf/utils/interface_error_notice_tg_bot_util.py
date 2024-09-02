from genaipf.conf import tg_bot_conf
import aiogram
from genaipf.utils.log_utils import logger
from typing import List

interface_error_notice_bot = aiogram.Bot(token=tg_bot_conf.INTERFACE_ERROR_NOTICE_TG_BOT_TOKEN)

async def send_notice_message(user_name_arr: List[str], fileName: str, method: str, code: str, message: str):
    user_name_list = " ".join(['@'+ user_name for user_name in user_name_arr])
    text = f"""
{user_name_list}
ml接口代码发生异常
文件：{fileName}
方法：{method}
异常编码:{code}
异常信息:\n{message}
"""
    try:
        await interface_error_notice_bot.send_message(chat_id=tg_bot_conf.INTERFACE_ERROR_NOTICE_TG_BOT_CHAT_ID, text=text)
    except Exception as e:
        logger.error("send interface error notice message error: {e}")


