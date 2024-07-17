
from importlib import import_module
from genaipf.conf.server import PLUGIN_NAME


template_qa = {
    "q": { # vdb_qa对应问题
        "ans_cn": "a", # 中文答案
        "ans_en": "a" # 英文答案
    }
}

if PLUGIN_NAME:
    plugin_submodule_name = f'{PLUGIN_NAME}.dispatcher.template_qa'
    plugin_submodule = import_module(plugin_submodule_name)
    template_qa = getattr(plugin_submodule, "template_qa", dict())
