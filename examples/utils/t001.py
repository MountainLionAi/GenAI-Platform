import asyncio
from genaipf.dispatcher.utils import async_simple_chat, async_simple_chat_stream

messages = [
    {"role": "system", "content": "you are smart"},
    {"role": "user", "content": "1 + 1 = ?"},
    {"role": "assistant", "content": "2"},
    {"role": "user", "content": "what did i ask?"},
]

async def test1():
    x = await async_simple_chat(messages)
    print(x)

async def test2():
    x = await async_simple_chat(messages, True)
    async for y in x:
        print(y)

async def test3():
    x = await async_simple_chat_stream(messages)
    async for y in x:
        print(y)

# asyncio.run(test1())
asyncio.run(test2())