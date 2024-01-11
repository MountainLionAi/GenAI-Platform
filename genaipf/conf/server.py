import os
from dotenv import load_dotenv
load_dotenv(override=True)

SERVICE_NAME = os.getenv("SERVICE_NAME", "GenAI")
PLUGIN_NAME = os.getenv("PLUGIN_NAME", None)
REQUEST_TIMEOUT = 180
RESPONSE_TIMEOUT = 180
KEEP_ALIVE_TIMEOUT = 180
KEEP_ALIVE = True
PORT = int(os.getenv("SERVER_PORT"))
HOST = "0.0.0.0"
LOG_PATH = os.getenv("SERVER_LOG_PATH")
PROJ_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONT_PATH = f"{PROJ_PATH}/static/arial.ttf"
IS_INNER_DEBUG = True if os.getenv("IS_INNER_DEBUG") else False
IS_UNLIMIT_USAGE = True if os.getenv("IS_UNLIMITED_USAGE") else False
STATIC_PATH = os.getenv("STATIC_PATH")
METAPHOR_API_KEY = os.getenv("METAPHOR_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
BING_SUBSCRIPTION_KEY = os.getenv("BING_SUBSCRIPTION_KEY")
BING_SEARCH_URL = os.getenv("BING_SEARCH_URL")