from importlib import import_module
from genaipf.conf.server import PLUGIN_NAME


ASSISTANT_ID_MAPPING = {
    "biz_id_____source": "123",
    "default": "012"
}

if PLUGIN_NAME:
    plugin_submodule_name = f'{PLUGIN_NAME}.conf.assistant_conf'
    plugin_submodule = import_module(plugin_submodule_name)
    ASSISTANT_ID_MAPPING = plugin_submodule.ASSISTANT_ID_MAPPING