
from importlib import import_module
from genaipf.conf.server import PLUGIN_NAME


source_mapping = {
    "TEST_SOURCE_001": { # source 名
        "qa_vdb": "TEST001PLUGIN_NAME__filtered_qa", # TEST_SOURCE_001 这个 source 名对应的 qa_vdb 名是 TEST001PLUGIN_NAME__filtered_qa
        "qa_map": "TEST001", # TEST_SOURCE_001 这个 source 名对应的 qa_map 名是 TEST001
        "gpt_func_vdb": "TEST001PLUGIN_NAME__gpt_func", # TEST_SOURCE_001 这个 source 名对应的 gpt_func_vdb 名是 TEST001PLUGIN_NAME__gpt_func
        "gpt_func_map": "TEST001", # TEST_SOURCE_001 这个 source 名对应的 gpt_func_map 名是 TEST001
    }
}

if PLUGIN_NAME:
    plugin_submodule_name = f'{PLUGIN_NAME}.dispatcher.source_mapping'
    plugin_submodule = import_module(plugin_submodule_name)
    source_mapping = getattr(plugin_submodule, "source_mapping", dict())
