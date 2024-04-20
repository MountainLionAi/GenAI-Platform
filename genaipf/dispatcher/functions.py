from genaipf.dispatcher.utils import get_vdb_topk, gpt_func_coll_name
from genaipf.dispatcher.vdb_pairs.gpt_func import vdb_map
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
    "medical_____treatment",
]

def gpt_function_filter(gpt_functions_mapping, messages, msg_k=5, v_n=5, per_n=2):
    try:
        user_messages = [msg['content'] for msg in messages if msg['role'] == 'user'][-msg_k:]
        used_names = set()
        for text in user_messages:
            tmp_names = []
            results = get_vdb_topk(text, gpt_func_coll_name, 0.1, v_n)
            for x in results:
                _name = vdb_map.get(x["payload"]["q"])
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