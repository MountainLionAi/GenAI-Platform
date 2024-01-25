import json
from genaipf.utils.log_utils import logger
from genaipf.controller.preset_entry import preset_entry_mapping, preset_entry_top_mapping
from genaipf.dispatcher.utils import get_qa_vdb_topk, merge_ref_and_input_text
from genaipf.dispatcher.api import generate_unique_id, get_format_output, gpt_functions, afunc_gpt_generator, aref_answer_gpt_generator
from genaipf.dispatcher.postprocess import posttext_mapping, PostTextParam

async def convert_func_out_to_stream(chunk, messages, newest_question, model, language):
    """
    chunk: afunc_gpt_generator return
    """
    # chunk = await resp1.__anext__()
    assert chunk["role"] == "inner_____func_param"
    _param = chunk["content"]
    _param["language"] = language
    func_name = _param["func_name"]
    sub_func_name = _param["subtype"]
    logger.info(f'>>>>> func_name: {func_name}, sub_func_name: {sub_func_name}, _param: {_param}')
    content = ""
    _type = ""
    presetContent = {}
    picked_content=""
    _data = {}
    if func_name in preset_entry_mapping:
        preset_conf = preset_entry_mapping[func_name]
        _type = preset_conf["type"]
        _args = [_param.get(x) for x in preset_conf["param_names"]]
        reslt = await preset_conf["get_and_pick"](*_args)
        if len(reslt) == 2:
            presetContent, picked_content = reslt
        elif len(reslt) == 3:
            presetContent, picked_content, _type = reslt
        if preset_conf.get("has_preset_content") and (_param.get("need_chart") or preset_conf.get("need_preset")):
            _data.update({
                'type' : _type,
                'subtype': sub_func_name,
                'content' : content,
                'presetContent' : presetContent
            })
            if func_name in preset_entry_top_mapping:
                yield {
                    "role": "inner_____preset", 
                    "type": "inner_____preset", 
                    "format": "inner_____preset", 
                    "version": "v001", 
                    "content": _data
                }
                _data = {}
    related_qa = get_qa_vdb_topk(newest_question)
    _messages = [x for x in messages if x["role"] != "system"]
    msgs = _messages[::]
    resp2 = await aref_answer_gpt_generator(msgs, model, language, _type, str(picked_content), related_qa)
    logger.info(f'>>>>> start->data done.')
    async for item in resp2:
        if item["role"] == "inner_____gpt_whole_text":
            # _tmp_text = item["content"]
            yield item
        else:
            yield item
    posttexter = posttext_mapping.get(func_name)
    if posttexter is not None:
        async for _gpt_letter in posttexter.get_text_agenerator(PostTextParam(language, sub_func_name)):
            _tmp_text += _gpt_letter
            yield get_format_output("gpt", _gpt_letter)
    if _data:
        yield {
            "role": "inner_____preset", 
            "type": "inner_____preset", 
            "format": "inner_____preset", 
            "version": "v001", 
            "content": _data
        }