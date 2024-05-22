import os
import asyncio
import autogen
from typing_extensions import Annotated
from datetime import datetime
from genaipf.dispatcher.tool_agent import fake_example_func

async def main():
    messages = [
        {"user": "please calculate the result of this math expression '2 + 3 * 5' "}
    ]
    async for x in fake_example_func(messages, None, None, None, None, None, None):
        print(x)

asyncio.run(main())