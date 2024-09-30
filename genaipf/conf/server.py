import os
import genaipf
from pathlib import Path
from dotenv import load_dotenv
try:
    _env_path = Path(Path(genaipf.__path__[0]).parent, ".env")
    load_dotenv(_env_path, override=True)
except Exception as e:
    print(f'genaipf/conf/server.py, {e}')
    _env_path = ".env"
    load_dotenv(override=True)

SERVICE_NAME = os.getenv("SERVICE_NAME", "GenAI")
PLUGIN_NAME = os.getenv("PLUGIN_NAME", None)
SUB_VDB_QA_PREFIX = os.getenv("SUB_VDB_QA_PREFIX", "")
SUB_VDB_GPT_FUNC_PREFIX = os.getenv("SUB_VDB_GPT_FUNC_PREFIX", "")
REQUEST_TIMEOUT = 1800
RESPONSE_TIMEOUT = 1800
KEEP_ALIVE_TIMEOUT = 1800
KEEP_ALIVE = True
PORT = int(os.getenv("SERVER_PORT"))
HOST = "0.0.0.0"
LOG_PATH = os.getenv("SERVER_LOG_PATH")
PROJ_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONT_PATH = f"{PROJ_PATH}/static/arial.ttf"
IS_INNER_DEBUG = True if os.getenv("IS_INNER_DEBUG") else False
IS_UNLIMIT_USAGE = True if os.getenv("IS_UNLIMIT_USAGE") else False
STATIC_PATH = os.getenv("STATIC_PATH")
PROXY_URL = os.getenv("PROXY_URL")
METAPHOR_API_KEY = os.getenv("METAPHOR_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
BING_SUBSCRIPTION_KEY = os.getenv("BING_SUBSCRIPTION_KEY")
BING_SEARCH_URL = os.getenv("BING_SEARCH_URL")
PER_PLE_API_KEY = os.getenv("PER_PLE_API_KEY")
PER_PLE_URL = os.getenv("PER_PLE_URL")
GOOGLE_SERPER_API_KEY = os.getenv("GOOGLE_SERPER_API_KEY")
BSC_SCAN_KEY = os.getenv("BSC_SCAN_KEY")
AI_ANALYSIS_USE_MODEL = os.getenv("AI_ANALYSIS_USE_MODEL", "claude")
SPIDER_API_KEY = os.getenv("SPIDER_API_KEY")
GRAPH_RAG_PATH = os.getenv("GRAPH_RAG_PATH")
ZHIPU_GLM_API_KEY = os.getenv("ZHIPU_GLM_API_KEY")