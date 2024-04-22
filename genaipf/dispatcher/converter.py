import json
from genaipf.utils.log_utils import logger
from genaipf.controller.preset_entry import preset_entry_mapping, preset_entry_top_mapping
from genaipf.dispatcher.utils import get_qa_vdb_topk, merge_ref_and_input_text
from genaipf.dispatcher.api import generate_unique_id, get_format_output, gpt_functions, afunc_gpt_generator, aref_answer_gpt_generator
from genaipf.dispatcher.postprocess import posttext_mapping, PostTextParam
from genaipf.tools.search.utils.search_agent_utils import not_need_search, not_need_sources
from genaipf.services.cmc_token import get_token_cmc_url

async def convert_func_out_to_stream(chunk, messages, newest_question, model, language, related_qa, source, owner, sources=[], is_need_search=False, sources_task=None, chain_id=''):
    """
    chunk: afunc_gpt_generator return
    """
    # chunk = await resp1.__anext__()
    assert chunk["role"] == "inner_____func_param"
    _param = chunk["content"]
    _param["language"] = language
    _param["chain_id"] = chain_id
    func_name = _param["func_name"]
    sub_func_name = _param["subtype"]
    logger.info(f'>>>>> func_name: {func_name}, sub_func_name: {sub_func_name}, _param: {_param}')
    already_sources = False
    if sources:
        already_sources = True
    if is_need_search and (func_name not in not_need_sources):
        sources, related_qa = await sources_task
    else:
        if func_name == 'coin_price':
            sources = [
                {
                    'title': 'coin_price',
                    'url': get_token_cmc_url(_param['symbol'])
                }
            ]
    if func_name not in not_need_search and not already_sources:
        yield {
            "role": "sources", 
            "content": sources
        }
        yield get_format_output("chatSerpResults", sources)
    elif func_name in not_need_search and already_sources:
        yield get_format_output("chatSerpResultsHide", 1)
    content = ""
    _type = ""
    presetContent = {}
    picked_content=""
    _data = {}
    if func_name in preset_entry_mapping:
        preset_conf = preset_entry_mapping[func_name]
        _type = preset_conf["type"]
        _args = [_param.get(x) for x in preset_conf["param_names"]]
        if func_name == 'richer_prompt':
            reslt = await preset_conf["get_and_pick"](messages, *_args)
        else:
            reslt = await preset_conf["get_and_pick"](*_args)
        if len(reslt) == 2:
            presetContent, picked_content = reslt
            if func_name == 'coin_swap' and presetContent.get('preset_type') == 'coin_swap1':
                sub_func_name = 'coin_swap1'
            if func_name == 'url_search':
                related_qa.append(f'相关问题: {picked_content}')
        elif len(reslt) == 3:
            presetContent, picked_content, _type = reslt
        if preset_conf.get("has_preset_content") and (_param.get("need_chart") or preset_conf.get("need_preset")) and presetContent != {}:
            _data.update({
                'type' : _type,
                'subtype': sub_func_name,
                'content' : content,
                'presetContent' : presetContent
            })
            if func_name in preset_entry_top_mapping:
                if func_name == 'generate_report':
                    _data.update({
                        'coin': _param.get('coin')
                    })
                yield {
                    "role": "inner_____preset_top", 
                    "type": "inner_____preset_top", 
                    "format": "inner_____preset_top", 
                    "version": "v001", 
                    "content": _data
                }
                _data = {}
    if func_name in ['buy_but_not_receive', 'why_can_not_transfer_out', 'transfer_only']:
        if _data:
            yield {
                "role": "inner_____preset", 
                "type": "inner_____preset", 
                "format": "inner_____preset", 
                "version": "v001", 
                "content": _data
            }
            if func_name == 'transfer_only':
                transfer_only_content = """
                好的，为了确保您的资金安全，我们需要对您提供的转账地址进行合规性检测。请您提供您想要检查的转账地址。
            一旦您提供了地址，我们将尽快回复您检测结果。如果任何问题或需要进一步的协助，请随时联系我们。我们在这里为您提供支持！
                """
                yield get_format_output("gpt", transfer_only_content)
    if (func_name not in not_need_search and sub_func_name != 'coin_swap1') or (func_name == 'generate_report' and presetContent == {}):
        _messages = [x for x in messages if x["role"] != "system"]
        msgs = _messages[::]
        resp2 = await aref_answer_gpt_generator(msgs, model, language, _type, str(picked_content), related_qa, source, owner)
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
    if func_name not in ['buy_but_not_receive', 'why_can_not_transfer_out', 'transfer_only']:
        if _data:
            yield {
                "role": "inner_____preset", 
                "type": "inner_____preset", 
                "format": "inner_____preset", 
                "version": "v001", 
                "content": _data
            }
        
        
        
async def run_tool_agent(chunk, messages, newest_question, model, language, related_qa, source, owner, sources=[], is_need_search=False, sources_task=None, chain_id=''):
    _param = chunk["content"]
    func_name = _param["func_name"]
    from genaipf.dispatcher.tool_agent import tool_agent_mapping
    tool_agent_func = tool_agent_mapping[func_name]["func"]
    resp = await tool_agent_func(messages, newest_question, model, language, related_qa, source, owner, sources=[], is_need_search=False, sources_task=None, chain_id='')
    async for item in resp:
        yield item
    