from genaipf.utils.log_utils import logger

from importlib import import_module
from genaipf.conf.server import PLUGIN_NAME


async def weather_generator(params):
    ...

stylized_process_mapping = {
    "weather": weather_generator
}

if PLUGIN_NAME:
    plugin_submodule_name = f'{PLUGIN_NAME}.dispatcher.stylized_process'
    plugin_submodule = import_module(plugin_submodule_name)
    stylized_process_mapping = getattr(plugin_submodule, "stylized_process_mapping", dict())