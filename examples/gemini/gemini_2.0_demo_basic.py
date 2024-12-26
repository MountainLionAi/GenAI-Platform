from google import genai
import os
import dotenv

dotenv.load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

client = genai.Client(
    api_key=GOOGLE_API_KEY
)
response = client.models.generate_content(
    model='gemini-2.0-flash-exp', contents='你好，比特币当前价格'
)
print(response.text)

