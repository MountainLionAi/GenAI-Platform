from google import genai

import os
import dotenv

dotenv.load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

client = genai.Client(api_key=GOOGLE_API_KEY, http_options={'api_version': 'v1alpha'})
model_id = "gemini-2.0-flash-exp"
config = {"response_modalities": ["TEXT"]}

async def multimodallive():
    async with client.aio.live.connect(model=model_id, config=config) as session:
        message = "你好? Gemini, 在吗?"
        print("> ", message, "\n")
        await session.send(message, end_of_turn=True)

        async for response in session.receive():
            print(response)
            print(response.text)
            
import asyncio

asyncio.run(multimodallive())