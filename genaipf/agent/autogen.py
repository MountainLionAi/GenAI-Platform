import os
import asyncio
import autogen
from typing_extensions import Annotated
from typing import Mapping, Any, Callable, Awaitable
import inspect
from functools import partial, update_wrapper

AsyncCallable = Callable[..., Awaitable[Any]]

def _wrap(self, fn: AsyncCallable) -> AsyncCallable:
    sig = inspect.signature(fn)
    parameters = [p for name, p in sig.parameters.items() if name != 'self']
    new_sig = sig.replace(parameters=parameters)
    async def _wrapped_fn(*args: Any, **kwargs: Any) -> Any:
        res = await fn(self, *args, **kwargs)
        return res
    update_wrapper(_wrapped_fn, fn, assigned=('__module__', '__name__', '__qualname__', '__annotations__', '__doc__'))
    _wrapped_fn.__signature__ = new_sig
    return _wrapped_fn

class AutoGenMultiAgent:
    def __init__(
        self,
        llm_config: Mapping[str, Any],
        agents_config: Mapping[str, Any],
        context_obj: Any
    ):
        self.llm_config: Mapping[str, Any] = llm_config
        self.agents_config: Mapping[str, Any] = agents_config
        self.context_obj = context_obj
        if hasattr(self.context_obj, "update_llm_config"):
            self.llm_config = self.context_obj.update_llm_config(self.llm_config)
        self.assistant_agents = dict()
        self.setup_agents()
        self.setup_groupchat()
        
    def setup_agents(self):
        for _, config in self.agents_config.items():
            if config["agent_type"] == "UserProxyAgent":
                self.setup_UserProxyAgent(config)
            elif config["agent_type"] == "AssistantAgent":
                self.setup_AssistantAgent(config)
    
    def setup_groupchat(self):
        _agents = [self.user_proxy] + list(self.assistant_agents.values())
        self.groupchat = autogen.GroupChat(
            agents=_agents, messages=[], max_round=50
        )
        self.manager = autogen.GroupChatManager(
            groupchat=self.groupchat,
            llm_config=self.llm_config.copy()
        )

    async def a_initiate_chat(self, message: str):
        return await self.user_proxy.a_initiate_chat(
            self.manager,
            message=message,
        )
    
    def setup_UserProxyAgent(self, config):
        name = config["name"]
        self.user_proxy = autogen.UserProxyAgent(
            name=name,
            is_termination_msg=lambda x: True if "TERMINATE" in x.get("content") else False,
            code_execution_config=False,
            human_input_mode="NEVER",
            default_auto_reply="TERMINATE",
            max_consecutive_auto_reply=3,
        )
    
    def setup_AssistantAgent(self, config):
        name = config["name"]
        system_message = config["system_message"]
        func_configs = config.get("func_configs", dict())
        self.assistant_agents[name] = autogen.AssistantAgent(
            name=name,
            system_message=system_message,
            llm_config=self.llm_config.copy()
        )
        for _, func_conf in func_configs.items():
            desc = func_conf["description"]
            fn = func_conf["func"]
            wrapped_fn = _wrap(self, fn)
            _agent = self.assistant_agents[name]
            _agent.register_for_execution()(
                _agent.register_for_llm(description=desc)(wrapped_fn)
            )
