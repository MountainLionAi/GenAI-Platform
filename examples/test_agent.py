import asyncio
from datetime import datetime
from genaipf.agent.llama_index import LlamaIndexAgent

async def multiply(a: int, b: int) -> int:
    """Multiple two integers and returns the result integer"""
    return a * b

async def add(a: int, b: int) -> int:
    """Add two integers and returns the result integer"""
    return a + b

# agent = LlamaIndexAgent([multiply, add], system_prompt="Answer me with only one word.")
# agent = LlamaIndexAgent([])
agent = LlamaIndexAgent([multiply, add])

agent.start_chat("What is (121 * 3) + 42?")

async for x in agent.async_response_gen():
    print(x)