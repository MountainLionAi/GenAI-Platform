from utils.log_utils import logger

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
