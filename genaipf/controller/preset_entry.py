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
    '''
    from importlib import import_module

    # the full path to the submodule 
    module_name = "m1.s1"
    submodule = import_module(module_name)

    # name of the item you want to import
    item_name = "x1"
    item = getattr(submodule, item_name)

    # now item is equivalent to x1 and you can use it as such
    '''
    # plugin_controller_name = f'{PLUGIN_NAME}.controller'
    # plugin_controller = import_module(plugin_controller_name)
    # preset_entry_mapping = plugin_controller.preset_entry.preset_entry_mapping
    plugin_submodule_name = f'{PLUGIN_NAME}.controller.preset_entry'
    plugin_submodule = import_module(plugin_submodule_name)
    preset_entry_mapping = plugin_submodule.preset_entry_mapping
    preset_entry_top_mapping = plugin_submodule.preset_entry_top_mapping
    get_swap_preset_info = plugin_submodule.get_swap_preset_info
    intent_recog_mapping = getattr(plugin_submodule, "intent_recog_mapping", dict())
