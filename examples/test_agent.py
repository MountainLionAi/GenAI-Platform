import asyncio
from datetime import datetime
from genaipf.agent.llama_index import LlamaIndexAgent

async def multiply(self, a: int, b: int) -> int:
    """Multiple two integers and returns the result integer"""
    print(self.traceable_tools) # 这里 self 是 LlamaIndexAgent 对象，你可以用里面的任何内容
    return a * b

async def add(self, a: int, b: int) -> int:
    """Add two integers and returns the result integer"""
    print(self.traceable_tools) # 这里 self 是 LlamaIndexAgent 对象，你可以用里面的任何内容
    return a + b

# agent = LlamaIndexAgent([multiply, add], system_prompt="Answer me with only one word.")
# agent = LlamaIndexAgent([])
agent = LlamaIndexAgent([multiply, add], verbose=True)

agent.start_chat("What is (121 * 3) + 42?")

async for x in agent.async_response_gen():
    print(x)