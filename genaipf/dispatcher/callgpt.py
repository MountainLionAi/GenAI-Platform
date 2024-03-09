from typing import Mapping, Any
from genaipf.utils.log_utils import logger
from importlib import import_module
from genaipf.conf.server import PLUGIN_NAME

need_call_gpt_subtype_list = []

class DispatcherCallGpt:
    @classmethod
    async def get_subtype_task_result(cls, subtype: str, language: str, data: Mapping[str, Any]):
        ...
    
    @classmethod
    async def get_specific_gpt_result(cls, name: str, language: str, data: Mapping[str, Any]):
        ...
        
    @classmethod
    def need_call_gpt(cls, data: Mapping[str, Any]):
        ...

    @classmethod
    def gen_preset_content(cls, subtype: str, subtype_task_result: Mapping[str, Any], data: Mapping[str, Any]):
        ...

if PLUGIN_NAME:
    plugin_submodule_name = f'{PLUGIN_NAME}.dispatcher.callgpt'
    plugin_submodule = import_module(plugin_submodule_name)
    DispatcherCallGpt = plugin_submodule.DispatcherCallGpt
    need_call_gpt_subtype_list = plugin_submodule.need_call_gpt_subtype_list