from importlib import import_module
from genaipf.conf.server import PLUGIN_NAME




if PLUGIN_NAME:
    plugin_submodule_name = f'{PLUGIN_NAME}.conf.model_selection_conf'
    plugin_submodule = import_module(plugin_submodule_name)
    MODEL_MAPPING = plugin_submodule.MODEL_MAPPING