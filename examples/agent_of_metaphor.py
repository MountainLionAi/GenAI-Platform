from typing import List
from genaipf.conf.server import os
import asyncio
from datetime import datetime
from genaipf.agent.llama_index import LlamaIndexAgent
from metaphor_python import Metaphor
from llama_index.llms import OpenAI, ChatMessage

METAPHOR_API_KEY = os.getenv("METAPHOR_API_KEY")

metaphor = Metaphor(api_key=METAPHOR_API_KEY)

import asyncio
from datetime import datetime
from genaipf.agent.llama_index import LlamaIndexAgent

def sync_to_async(fn):
    async def _async_wrapped_fn(*args, **kwargs):
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, lambda: fn(*args, **kwargs))
    return _async_wrapped_fn

asearch_of_metaphor = sync_to_async(metaphor.search)
aget_contents_of_metaphor = sync_to_async(metaphor.get_contents)

async def search(self, query: str) -> List[str]:
    """Search for a webpage based on the query."""
    self.metaphor_query = query
    print(f'>>>>>query: {query}')
    res = metaphor.search(f"{query}")
    ids = [x.id for x in res.results]
    results = await aget_contents_of_metaphor(ids)
    self.metaphor_results = results
    self.is_stopped = True
    return results


system_prompt = """
用户问的问题可能是比较简单的表述，直接搜索的结果不好，
你扩充丰富一下形成一个全面完整的问题再触发 search 工具，
"""
chat_history = [
    ChatMessage(role="user", content="我买什么币好？"),
    ChatMessage(role="assistant", content="BTC")
]
agent = LlamaIndexAgent([search], system_prompt=system_prompt, chat_history=chat_history, verbose=False)

agent.start_chat("最近它有什么新闻？")

async for x in agent.async_response_gen():
    # print(x)
    pass

print(f'扩充后的问题: {agent.metaphor_query}')
print(f'可以在 agent.metaphor_results 看结果: {agent.metaphor_results.contents[0].title}')