from genaipf.conf.server import os

SMTP_HOST = os.getenv("SMTP_HOST")
SMTP_PORT = int(os.getenv("SMTP_PORT"))
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
SMTP_USER_SWFTGPT = os.getenv("SMTP_USER_SWFTGPT")
SMTP_PASSWORD_SWFTGPT = os.getenv("SMTP_PASSWORD_SWFTGPT")
SMTP_USE_TLS = True
