import asyncio
from inspect import signature
from typing import TYPE_CHECKING, Any, Awaitable, Callable, Optional, Type, List, AsyncGenerator

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