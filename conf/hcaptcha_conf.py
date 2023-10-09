import os
from dotenv import load_dotenv
load_dotenv()
# os.getenv("")

SECRET_KEY = os.getenv("hcaptcha_SECRET_KEY")
VERIFY_URL = os.getenv("hcaptcha_VERIFY_URL")
