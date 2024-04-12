from genaipf.conf.server import os

# client choose
RAG_SEARCH_CLIENT=os.getenv("RAG_SEARCH_CLIENT", "SERPER")

# google search
GOOGLE_SEARCH_URL = os.getenv("GOOGLE_SEARCH_URL")
API_KEY = os.getenv("API_KEY")
CX = os.getenv("CX")

# chromium  (1.sudo apt install chromium-browser 2.whereis chromium)
CHROMIUM_EXECUTABLEPATH = os.getenv("CHROMIUM_EXECUTABLEPATH", None)
