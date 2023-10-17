import aiosmtplib
import genaipf.conf.email_conf as email_conf
from genaipf.utils.log_utils import logger
import aiofiles
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from genaipf.constant.redis_keys import REDIS_KEYS
from genaipf.utils.redis_utils import RedisConnectionPool

LIMIT_TIME_10MIN = {
    'REGISTER': 8,
    'FORGET_PASSWORD': 8
}

EMAIL_SCENES = {
    'REGISTER': 'REGISTER',
    'FORGET_PASSWORD': 'FORGET_PASSWORD'
}


# 发送邮件的异步方法
async def send_email(subject, content, to_email):
    message = MIMEMultipart()
    message["From"] = email_conf.SMTP_USER
    message["To"] = to_email
    message["Subject"] = subject
    message.attach(MIMEText(content, 'html'))
    logger.info(f'Send verify_code email to user: {message}')
    await aiosmtplib.send(
        message,
        hostname=email_conf.SMTP_HOST,
        port=email_conf.SMTP_PORT,
        username=email_conf.SMTP_USER,
        password=email_conf.SMTP_PASSWORD,
        use_tls=email_conf.SMTP_USE_TLS,
    )


async def format_captcha_email(email, captcha_code, language, scene):
    if language == 'zh':
        if scene == EMAIL_SCENES['REGISTER']:
            html_path = 'static/email_template_zh.html'
        else:
            html_path = 'static/email_template_zh_forget.html'
    else:
        if scene == EMAIL_SCENES['REGISTER']:
            html_path = 'static/email_template_en.html'
        else:
            html_path = 'static/email_template_en_forget.html'
    f = await aiofiles.open(html_path, mode='r')
    email_content = await f.read()
    email_content = email_content.replace('{{email}}', email)
    email_content = email_content.replace('{{emailCode}}', captcha_code)
    return email_content


# 设置某种类型邮件的发送次数
async def add_email_times(email, scene):
    limit_key = REDIS_KEYS['USER_KEYS']['EMAIL_LIMIT'].format(scene, email)
    redis_client = RedisConnectionPool().get_connection()
    redis_client.incr(limit_key, 1)
    redis_client.expire(limit_key, 60 * 10)
    return True


# 获取某种类型的邮件的发送次数
async def get_email_times(email, scene):
    limit_key = REDIS_KEYS['USER_KEYS']['EMAIL_LIMIT'].format(scene, email)
    redis_client = RedisConnectionPool().get_connection()
    times = redis_client.get(limit_key)
    if times is None:
        return 0
    else:
        return int(times)


# 比较发送的数量是否达到限额
def check_time(current, limit):
    if current < limit:
        return True
    else:
        return False
