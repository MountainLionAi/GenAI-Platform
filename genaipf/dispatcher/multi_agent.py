from importlib import import_module
from genaipf.conf.server import PLUGIN_NAME

from genaipf.dispatcher.multi_agent_templates.default import multi_agent_config

multi_agent_mapping = {
    "default": multi_agent_config
}

if PLUGIN_NAME:
    plugin_submodule_name = f'{PLUGIN_NAME}.dispatcher.multi_agent'
    try:
        plugin_submodule = import_module(plugin_submodule_name)
    except ModuleNotFoundError:
        plugin_submodule = None
    multi_agent_mapping = getattr(plugin_submodule, "multi_agent_mapping", dict())

