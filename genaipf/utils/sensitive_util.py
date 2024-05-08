from genaipf.constant.sensitive_words import WORDS

async def isNormal(str):
    isNormal = True
    for word in WORDS:
        if word in str:
            isNormal = False
            break
    return isNormal