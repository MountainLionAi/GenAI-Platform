from genaipf.dispatcher.utils import get_vdb_topk, gpt_func_coll_name
from genaipf.dispatcher.vdb_pairs.gpt_func import vdb_map, gpt_func_maps, gpt_funcs
from genaipf.utils.log_utils import logger

from importlib import import_module
from genaipf.conf.server import PLUGIN_NAME

gpt_functions_mapping = {
    "weather_____get_current_weather": {
        "name": "weather_____get_current_weather",
        "description": "Get the current weather in a given location",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "The city and state, e.g. San Francisco, CA"
                },
                "unit": {
                    "type": "string",
                    "enum": ["celsius", "fahrenheit"]
                }
            },
            "required": ["location"]
        }
    },
    "medical_____treatment": {
        "name": "medical_____treatment",
        "description": "if user want surgery or medicine, call this",
        "parameters": {
            "type": "object",
            "properties": {
                "treatment": {
                    "type": "string",
                    "description": "surgery or medicine"
                }
            },
            "required": ["treatment"]
        }
    }
}


gpt_functions = list(gpt_functions_mapping.values())
need_tool_agent_l = [
    "medical",
    "medical_____treatment",
]

def gpt_function_filter(gpt_functions_mapping, messages, msg_k=5, v_n=5, per_n=2, source=None):
    from genaipf.dispatcher.source_mapping import source_mapping
    if source in source_mapping:
        vdb_name = source_mapping[source]["gpt_func_vdb"]
        _gpt_func_map_name = source_mapping[source]["gpt_func_map"]
        _gpt_func_map = gpt_func_maps[_gpt_func_map_name]
    else:
        vdb_name = gpt_func_coll_name
        _gpt_func_map = vdb_map
    try:
        if source == 'v008':
            used_names = gpt_funcs['SOURCE008']
        elif source == 'v009':
            used_names = gpt_funcs['SOURCE009']
        else:
            user_messages = [msg['content'] for msg in messages if msg['role'] == 'user'][-msg_k:]
            used_names = set()
            for text in user_messages:
                tmp_names = []
                results = get_vdb_topk(text, vdb_name, 0.1, v_n)
                for x in results:
                    _name = _gpt_func_map.get(x["payload"]["q"])
                    if _name and _name not in tmp_names:
                        tmp_names.append(_name)
                used_names = used_names.union(set(tmp_names[:per_n]))
        return [gpt_functions_mapping[k] for k in used_names]
    except Exception as e:
        logger.error(f'>>>>>>gpt_function_filter {e}')
        return gpt_functions
    

if PLUGIN_NAME:
    plugin_submodule_name = f'{PLUGIN_NAME}.dispatcher.functions'
    plugin_submodule = import_module(plugin_submodule_name)
    gpt_functions_mapping = plugin_submodule.gpt_functions_mapping
    gpt_functions = list(gpt_functions_mapping.values())
    need_tool_agent_l = getattr(plugin_submodule, "need_tool_agent_l", list())