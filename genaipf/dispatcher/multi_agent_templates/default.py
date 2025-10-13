import os
import asyncio
import autogen
from typing_extensions import Annotated
from datetime import datetime
from genaipf.conf.server import OPENAI_API_KEY

openai_api_key = OPENAI_API_KEY

llm_config = {
    "config_list": [{"model": "gpt-5", "api_key": openai_api_key}],
    "cache_seed": "abc123",
    "temperature": 0.1,
    "timeout": 5 * 60,
}

async def pack(
    self,
    goods_name: Annotated[str, "what has been packed"],
) -> str:
    await asyncio.sleep(1)
    return f'''
pack {goods_name}
'''

async def deliver(
    self,
    goods_name: Annotated[str, "what has been packed"],
) -> str:
    await asyncio.sleep(1)
    return f'''
deliver {goods_name}
'''

Planner_system_message = """
Planner. Suggest a plan for sales.
The plan may involve 2 workers,
Packer, Responsible for pack what consumer want;
Courier, Responsible for deliver what Packer has packed;
Explain the plan first. Be clear which step is performed by which role.
You need not give a result, just give a plan.
"""
Packer_system_message = """
Packer. You follow an approved plan by Planner.
For packing what consumer wants,
only use the function you have been provided with.
You have a pack function.
"""
Courier_system_message = """
Courier. You follow an approved plan by Planner.
For delivering what Packer has packed,
only use the function you have been provided with.
You have a deliver function.
"""

agents_config = {
    "User_proxy": {
        "name": "User_proxy",
        "agent_type": "UserProxyAgent"
    },
    "Planner": {
        "name": "Planner",
        "system_message": Planner_system_message,
        "agent_type": "AssistantAgent"
    },
    "Packer": {
        "name": "Packer",
        "system_message": Packer_system_message,
        "agent_type": "AssistantAgent",
        "func_configs": {
            "pack": {
                "description": "Pack what user wants",
                "func": pack,
            },
        },
    },
    "Courier": {
        "name": "Courier",
        "system_message": Courier_system_message,
        "agent_type": "AssistantAgent",
        "func_configs": {
            "deliver": {
                "description": "Deliver what has been packed",
                "func": deliver,
            },
        },
    },
}

multi_agent_config = {
    "version": "v001",
    "llm_config": llm_config,
    "agents_config": agents_config,
}