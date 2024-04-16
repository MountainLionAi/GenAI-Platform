from importlib import import_module
from genaipf.conf.server import PLUGIN_NAME
from genaipf.dispatcher.functions import need_tool_agent_l

async def fake_example_func(messages, newest_question, model, language, related_qa, source, owner, sources=[], is_need_search=False, sources_task=None, chain_id=''):
    ...

tool_agent_mapping = {
    "medical_____treatment": {
        "name": "medical_____treatment",
        "func": fake_example_func
    }
}


if PLUGIN_NAME:
    plugin_submodule_name = f'{PLUGIN_NAME}.dispatcher.tool_agent'
    plugin_submodule = import_module(plugin_submodule_name)
    tool_agent_mapping = getattr(plugin_submodule, "tool_agent_mapping", dict())
    assert set(need_tool_agent_l) == set(tool_agent_mapping.key())