from google import genai
from google.genai.types import Tool, GenerateContentConfig, GoogleSearch
import os
import dotenv

dotenv.load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

client = genai.Client(
    api_key=GOOGLE_API_KEY
)
google_search_tool = Tool(
    google_search = GoogleSearch()
)
model_id = "gemini-2.0-flash-exp"
response = client.models.generate_content(
    model=model_id,
    contents="比特币当前价格?",
    config=GenerateContentConfig(
        tools=[google_search_tool],
        response_modalities=["TEXT"],
    )
)

for each in response.candidates[0].content.parts:
    print(each.text)
# Example response:
# The next total solar eclipse visible in the contiguous United States will be on ...

# To get grounding metadata as web content.
print(response.candidates[0].grounding_metadata.search_entry_point.rendered_content)

