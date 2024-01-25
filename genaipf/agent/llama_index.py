import asyncio
from inspect import signature
from typing import TYPE_CHECKING, Any, Awaitable, Callable, Optional, Type, List, AsyncGenerator
from llama_index.llms import OpenAI, ChatMessage
from llama_index.tools import BaseTool, FunctionTool, ToolMetadata
from llama_index.tools.utils import create_schema_from_function
from llama_index.agent import OpenAIAgent
from llama_index.llms import OpenAI
from llama_index.llms.openai import DEFAULT_TEMPERATURE
from genaipf.conf.server import OPENAI_API_KEY
from genaipf.dispatcher.api import get_format_output
from genaipf.agent.utils import create_function_from_method

AsyncCallable = Callable[..., Awaitable[Any]]

class LlamaIndexAgent:
    def __init__(
        self, async_tools: List[AsyncCallable],
        system_prompt: Optional[str]=None,
        chat_history: Optional[List[ChatMessage]] = None,
        verbose: bool = False,
        temperature: float = DEFAULT_TEMPERATURE,
        max_tokens: int = None
    ):
        self.output_q = asyncio.Queue()
        self.tool_q = asyncio.Queue()
        self.is_stopped = False
        self.traceable_tools: List[FunctionTool] = list()
        self.tools_to_traceable_tools(async_tools)
        llm = OpenAI(
            model="gpt-4-1106-preview", 
            api_key=OPENAI_API_KEY, 
            temperature=temperature,
            max_tokens=max_tokens
        )
        self.agent = OpenAIAgent.from_tools(
            self.traceable_tools, llm=llm,
            chat_history=chat_history, verbose=verbose,
            system_prompt=system_prompt
        )
        
    def tools_to_traceable_tools(self, async_tools: List[AsyncCallable]) -> None:
        def _wrap(fn: AsyncCallable, fn_name: str):
            async def _wrapped_fn(*args: Any, **kwargs: Any) -> Any:
                await self.tool_q.put({"fn_name": fn_name, "step": "start", "res": {"args": args, "kwargs": kwargs}})
                res = await fn(self, *args, **kwargs)
                await self.tool_q.put({"fn_name": fn_name, "step": "end", "res": res})
                return res
            return _wrapped_fn
        for fn in async_tools:
            formated_fn = create_function_from_method(fn)
            name = formated_fn.__name__
            docstring = formated_fn.__doc__
            description = f"{name}{signature(formated_fn)}\n{docstring}"
            fn_schema = create_schema_from_function(
                f"{name}", formated_fn, additional_fields=None
            )
            tool_metadata = ToolMetadata(
                name=name, description=description, fn_schema=fn_schema
            )
            self.traceable_tools.append(FunctionTool(
                fn=None,
                metadata=tool_metadata,
                async_fn=_wrap(fn, name)
            ))
 
    def start_chat(self, message: str):
        async def tool_q_to_output_q():
            while True:
                item = await self.tool_q.get()
                if item is None:
                    break
                # yield item
                if item["step"] == "start":
                    await self.output_q.put({"role": "tool", "type": item["fn_name"], "format": "start", "version": "v001", "content": item["res"]})
                elif item["step"] == "end":
                    await self.output_q.put({"role": "tool", "type": item["fn_name"], "format": "end", "version": "v001", "content": item["res"]})
        _t = asyncio.create_task(tool_q_to_output_q())
        
        def task_callback(task):
            resp = task.result()
            resp_gen = resp.async_response_gen()
            async def response_wrapper(response_gen: AsyncGenerator):
                if self.is_stopped:
                    self.is_stopped = False
                    await response_gen.aclose()
                    await self.tool_q.put(None)
                    await self.output_q.put(get_format_output("step", "done"))
                    await self.output_q.put(None)
                    return
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
    
    
        
        

        

        
        

    