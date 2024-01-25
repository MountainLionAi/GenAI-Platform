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

async def search(self, one_line_user_question: str) -> List[str]:
    """Search for a webpage based on the one_line_user_question."""
# A query is simply a sentence; there should be no line breaks before or after query."""
    self.metaphor_query = one_line_user_question
    print(f'>>>>>search query: {one_line_user_question}')
    res = await asearch_of_metaphor(f"{one_line_user_question}")
    ids = [x.id for x in res.results]
    results = await aget_contents_of_metaphor(ids)
    self.metaphor_results = results
    # self.is_stopped = True
    titles = [x.title for x in self.metaphor_results.contents]
    return titles

async def show_related_questions(self, related_questions: List[str]) -> List[str]:
    """Based on the user's latest question and chat history, 
    display 5 questions that the user might be interested in."""
    self.related_questions = related_questions
    print(f'>>>>>show_related_questions related_questions: {related_questions}')
    self.is_stopped = True
    return []

tools = [search, show_related_questions]

system_prompt = f"""
今天是 {datetime.now()}，你是个工具人，你既能联网，也能给用户推荐其他感兴趣的问题，必须调用工具 function，有 2 种情况 SCENE_1 和 SCENE_2：
### SCENE_1
用户问的问题最好联网搜索才能回答更好，
用户问的问题可能是比较简单的表述，直接网络搜索的结果不好，
你扩充丰富一下形成一个全面完整的问题再触发 search 工具 function (完整的问题 query 一定要信息丰富但不要超过100个字符，query里(包括它前后)不要有换行符)
然后再生成 5 个用户可能感兴趣的问题，调用 show_related_questions。
### SCENE_2
调用 show_related_questions, 直接生成 5 个用户可能感兴趣的问题。

show_related_questions 中 related_questions 列出的相关问题需要和 user 问句和 user 历史对话用的语言一致，比如 user 之前用的汉语 show_related_questions 就是汉语，user 之前用的英语 show_related_questions 就是英语

你在不能直接回答用户问题，在回答用户前必须按情况 SCENE_1 或 SCENE_2 的流程调用 gpt function。
不要直接回答问题，即使用户说些无聊的对话也要根据用户的历史对话执行 SCENE_2 的 show_related_questions (而不是回答 "SCENE_2")
"""

# 记住不论情况 1 还是 2，不论是否调用 search, 一定要在最后调用 show_related_questions。
# 用户用什么语言，你就返回什么语言

async def test1():
    chat_history = [
        ChatMessage(role="user", content="我买什么币好？"),
        ChatMessage(role="assistant", content="BTC")
    ]
    agent = LlamaIndexAgent(
        tools,
        system_prompt=system_prompt,
        chat_history=chat_history,
        # chat_history=None,
        verbose=True,
        # temperature=0.2,
        max_tokens=300
    )
    agent.metaphor_query = ""
    agent.metaphor_results = None
    agent.related_questions = []
    # agent.start_chat("最近它有什么新闻？")
    # agent.start_chat("你好")
    # agent.start_chat("再回答一遍")
    agent.start_chat("BTC后续价格")

    _tmp_text = ""
    async for x in agent.async_response_gen():
        if x["role"] == "gpt":
            _tmp_text += str(x["content"])
        pass

    print(f'_tmp_text: {_tmp_text}')
    print(f'扩充后的问题: {agent.metaphor_query}')
    if agent.metaphor_results:
        print(f'可以在 agent.metaphor_results 看结果: {agent.metaphor_results.contents[0].title}')
    print(f'可以在 agent.related_questions 看结果: {agent.related_questions}')


asyncio.run(test1())