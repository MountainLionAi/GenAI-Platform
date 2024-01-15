import asyncio
from inspect import signature
from typing import TYPE_CHECKING, Any, Awaitable, Callable, Optional, Type, List, AsyncGenerator
from llama_index.llms import OpenAI, ChatMessage
from llama_index.tools import BaseTool, FunctionTool, ToolMetadata
from llama_index.tools.utils import create_schema_from_function
from llama_index.agent import OpenAIAgent
from llama_index.llms import OpenAI
from genaipf.conf.server import OPENAI_API_KEY
from genaipf.dispatcher.api import get_format_output

AsyncCallable = Callable[..., Awaitable[Any]]

class LlamaIndexAgent:
    def __init__(
        self, async_tools: List[AsyncCallable],
        system_prompt: Optional[str]=None,
        chat_history: Optional[List[ChatMessage]] = None,
        verbose: bool = False,
    ):
        self.output_q = asyncio.Queue()
        self.tool_q = asyncio.Queue()
        self.traceable_tools: List[FunctionTool] = list()
        self.tools_to_traceable_tools(async_tools)
        llm = OpenAI(model="gpt-4-1106-preview", api_key=OPENAI_API_KEY)
        self.agent = OpenAIAgent.from_tools(
            self.traceable_tools, llm=llm,
            chat_history=chat_history, verbose=verbose,
            system_prompt=system_prompt
        )
        
    def tools_to_traceable_tools(self, async_tools: List[AsyncCallable]) -> None:
        def _wrap(fn: AsyncCallable, fn_name: str):
            async def _wrapped_fn(*args: Any, **kwargs: Any) -> Any:
                await self.tool_q.put({"fn_name": fn_name, "step": "start", "res": {}})
                res = await fn(*args, **kwargs)
                await self.tool_q.put({"fn_name": fn_name, "step": "end", "res": res})
                return res
            return _wrapped_fn
        for fn in async_tools:
            name = fn.__name__
            docstring = fn.__doc__
            description = f"{name}{signature(fn)}\n{docstring}"
            fn_schema = create_schema_from_function(
                f"{name}", fn, additional_fields=None
            )
            tool_metadata = ToolMetadata(
                name=name, description=description, fn_schema=fn_schema
            )
            self.traceable_tools.append(FunctionTool(
                fn=None,
                metadata=tool_metadata,
                async_fn=_wrap(fn, name)
            ))
    
    async def merge_async_generators(self, gen1, gen2):
        async def producer(queue, agen):
            async for item in agen:
                await queue.put(item)
            await queue.put(None)  # 使用 None 作为生成器结束的信号

        queue = asyncio.Queue()
        # 启动两个协程作为生产者，分别消费两个异步生成器
        producers = [
            asyncio.create_task(producer(queue, gen1)),
            asyncio.create_task(producer(queue, gen2))
        ]
        finished_producers = 0
        while finished_producers < len(producers):
            item = await queue.get()
            if item is None:
                # 一个生成器已经完成
                finished_producers += 1
            else:
                yield item
    
    async def merge_queue_with_generator(self, q: asyncio.Queue, g: AsyncGenerator):
        async def queue_to_async_gen(queue):
            while True:
                item = await queue.get()
                if item is None:
                    break
                # yield item
                if item["step"] == "start":
                    yield {"role": "step", "type": "text", "format": "text", "version": "v001", "content": item["fn_name"]}
                elif item["step"] == "end":
                    yield {"role": "tool", "type": item["fn_name"], "format": "json", "version": "v001", "content": item["res"]}

        queue_gen = queue_to_async_gen(q)
        async_gen = g

        async for item in self.merge_async_generators(queue_gen, async_gen):
            yield item
        
    def start_chat(self, message: str):
        async def tool_q_to_output_q():
            while True:
                item = await self.tool_q.get()
                if item is None:
                    break
                # yield item
                if item["step"] == "start":
                    await self.output_q.put({"role": "step", "type": "text", "format": "text", "version": "v001", "content": item["fn_name"]})
                elif item["step"] == "end":
                    await self.output_q.put({"role": "tool", "type": item["fn_name"], "format": "json", "version": "v001", "content": item["res"]})
        _t = asyncio.create_task(tool_q_to_output_q())
        
        def task_callback(task):
            resp = task.result()
            resp_gen = resp.async_response_gen()
            async def response_wrapper(response_gen):
                await self.output_q.put(get_format_output("step", "llm_yielding"))
                async for item in response_gen:
                    await self.output_q.put(get_format_output("gpt", item))
                await self.tool_q.put(None)
                await self.output_q.put(get_format_output("step", "done"))
                await self.output_q.put(None)
            asyncio.create_task(response_wrapper(resp_gen))
        task = asyncio.create_task(self.agent.astream_chat(message))
        task.add_done_callback(task_callback)

    async def async_response_gen(self):
        while True:
            x = await self.output_q.get()
            if x is None:
                break
            yield x
    
    
        
        

        

        
        

    