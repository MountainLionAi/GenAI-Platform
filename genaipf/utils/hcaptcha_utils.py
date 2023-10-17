import requests
import genaipf.conf.hcaptcha_conf as hcaptcha_conf
from genaipf.utils.log_utils import logger


def verify_hcaptcha(response, email):
    """
    验证 hCaptcha 响应。

    :param email: 需要进行人机检测的邮箱
    :param response: 客户端提交的 hCaptcha 响应。
    :return: 返回一个布尔值，指示验证是否成功。
    """
    hcaptcha_verification_url = hcaptcha_conf.VERIFY_URL
    payload = {
        "response": response,
        "secret": hcaptcha_conf.SECRET_KEY
    }
    logger.info(f'开始对email: {email}进行人机检测')
    response = requests.post(hcaptcha_verification_url, data=payload)
    result = response.json()
    logger.info(f'对email: {email}进行人机检测，结果为: {result}')
    return result.get("success")
