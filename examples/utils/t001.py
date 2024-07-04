import asyncio
from genaipf.dispatcher.utils import async_simple_chat

messages = [
    {"role": "system", "content": "you are smart"},
    {"role": "user", "content": "1 + 1 = ?"},
    {"role": "assistant", "content": "2"},
    {"role": "user", "content": "what did i ask?"},
]

async def test1():
    x = await async_simple_chat(messages)
    print(x)
    
asyncio.run(test1())