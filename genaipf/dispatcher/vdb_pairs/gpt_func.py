from importlib import import_module
from genaipf.conf.server import PLUGIN_NAME

vdb_map = {
    "Ask about the weather conditions of a certain city.": "weather_____get_current_weather",
}


if PLUGIN_NAME:
    plugin_submodule_name = f'{PLUGIN_NAME}.dispatcher.vdb_pairs.gpt_func'
    plugin_submodule = import_module(plugin_submodule_name)
    vdb_map = plugin_submodule.vdb_map
