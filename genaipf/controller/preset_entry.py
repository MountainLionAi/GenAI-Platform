from genaipf.utils.log_utils import logger
from importlib import import_module
from genaipf.conf.server import PLUGIN_NAME


async def getAndPickSampleData(location, unit, language, subtype=None):
    presetContent = {}
    picked_content = ""
    return presetContent, picked_content

preset_entry_mapping = {
    "weather": {
        "type": "weather",
        "has_preset_content": True,
        "need_preset": True,
        "name": "weather",
        "sub_names": ["get_current_weather"],
        "param_names": ["location", "unit", "language", "subtype"],
        "get_and_pick": getAndPickSampleData,
    }
}

if PLUGIN_NAME:    
    plugin_name = PLUGIN_NAME
    math_module = import_module(module_name)