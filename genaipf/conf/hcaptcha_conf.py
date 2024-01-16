from genaipf.conf.server import os

SECRET_KEY = os.getenv("hcaptcha_SECRET_KEY")
VERIFY_URL = os.getenv("hcaptcha_VERIFY_URL")
