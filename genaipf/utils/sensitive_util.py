from genaipf.constant.sensitive_words import WORDS
from genaipf.utils.log_utils import logger

async def isNormal(str):
    isNormal = True
    for word in WORDS:
        if word in str:
            logger.info('sensitive_words:'+word)
            isNormal = False
            break
    return isNormal