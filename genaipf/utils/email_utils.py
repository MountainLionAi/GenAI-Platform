import aiosmtplib
import genaipf.conf.email_conf as email_conf
from genaipf.utils.log_utils import logger
import aiofiles
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from genaipf.constant.redis_keys import REDIS_KEYS
from genaipf.utils.redis_utils import RedisConnectionPool
import os
from jinja2 import Environment, FileSystemLoader, select_autoescape
import asyncio

EMAIL_SOURCE = {
    'SWFTGPT': 'SWFTGPT',
    'MLAPP': 'Mlion'
}

LIMIT_TIME_10MIN = {
    'REGISTER': 8,
    'FORGET_PASSWORD': 8,
    'WITHDRAW': 8,
}

EMAIL_SCENES = {
    'REGISTER': 'REGISTER',
    'FORGET_PASSWORD': 'FORGET_PASSWORD',
    'WITHDRAW': 'WITHDRAW',
}


# 发送邮件的异步方法
async def send_email(subject, content, to_email, source='', option_params=None):
    if option_params is None:
        option_params = {}
    username = email_conf.SMTP_USER
    password = email_conf.SMTP_PASSWORD
    if source == EMAIL_SOURCE['SWFTGPT'] and option_params.get('source', 'Mlion') == EMAIL_SOURCE['SWFTGPT']:
        username = email_conf.SMTP_USER_SWFTGPT
        password = email_conf.SMTP_PASSWORD_SWFTGPT
    message = MIMEMultipart()
    message["From"] = username
    message["To"] = to_email
    message["Subject"] = subject
    message.attach(MIMEText(content, 'html'))
    logger.info(f'Send verify_code email to user: {message}')
    await aiosmtplib.send(
        message,
        hostname=email_conf.SMTP_HOST,
        port=email_conf.SMTP_PORT,
        username=username,
        password=password,
        use_tls=email_conf.SMTP_USE_TLS,
    )
static_dir = os.getenv('GENAI_STATIC_PATH')
# 配置Jinja2环境
env = Environment(
    loader=FileSystemLoader(static_dir),  # 指定模板文件夹
    autoescape=select_autoescape(['html', 'xml'])
)

async def format_captcha_email(email, captcha_code, language, scene, option_params = {}, source = ''):
    if language == 'zh' or language == 'cn':
        if scene == EMAIL_SCENES['REGISTER']:
            template_file = 'email_template_zh.html'
        elif scene == EMAIL_SCENES['FORGET_PASSWORD']:
            template_file = 'email_template_zh_forget.html'
        else:
            template_file = 'email_template_zh_withdraw.html'
    else:
        if scene == EMAIL_SCENES['REGISTER']:
            template_file = 'email_template_en.html'
        elif scene == EMAIL_SCENES['FORGET_PASSWORD']:
            template_file = 'email_template_en_forget.html'
        else:
            template_file = 'email_template_en_withdraw.html'
    
    company_name = os.getenv("COMPANY_NAME")
    company_url = os.getenv("COMPANY_URL")
    if source == EMAIL_SOURCE['SWFTGPT'] and option_params['source'] == EMAIL_SOURCE['SWFTGPT']:
        company_name = os.getenv("COMPANY_NAME_SWFTGPT")

    template = env.get_template(template_file)
    if scene not in [EMAIL_SCENES['REGISTER'], EMAIL_SCENES['FORGET_PASSWORD']]:
        loop = asyncio.get_event_loop()
        option_params['company_name'] = company_name
        option_params['company_url'] = company_url
        option_params['emailCode'] = captcha_code
        email_content = await loop.run_in_executor(
            None,
            template.render,
            option_params
        )
    else:
        loop = asyncio.get_event_loop()
        email_content = await loop.run_in_executor(
            None,
            template.render,
            {
                'email': email,
                'emailCode': captcha_code,
                'company_name': company_name,
                'company_url': company_url
            }
        )
    if source == EMAIL_SOURCE['SWFTGPT'] and option_params['source'] == EMAIL_SOURCE['SWFTGPT']:
        email_content = email_content.replace(f'<a href="{company_url}">', '')
        email_content = email_content.replace('</a>', '')
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
