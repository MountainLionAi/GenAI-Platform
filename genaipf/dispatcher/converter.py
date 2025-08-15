import json
from genaipf.utils.log_utils import logger
from genaipf.controller.preset_entry import preset_entry_mapping, preset_entry_top_mapping
from genaipf.dispatcher.utils import get_qa_vdb_topk, merge_ref_and_input_text
from genaipf.dispatcher.api import generate_unique_id, get_format_output, gpt_functions, afunc_gpt_generator, aref_answer_gpt_generator
from genaipf.dispatcher.postprocess import posttext_mapping, PostTextParam
from genaipf.tools.search.utils.search_agent_utils import not_need_search, not_need_sources, need_gpt
from genaipf.services.cmc_token import get_token_cmc_url
import time

async def convert_func_out_to_stream(chunk, messages, newest_question, model, language, related_qa, source, owner, sources=[], is_need_search=False, sources_task=None, chain_id='', output_type="", llm_model="", user_id="", wallet_type="", visitor_id=''):
    """
    chunk: afunc_gpt_generator return
    """
    # chunk = await resp1.__anext__()
    assert chunk["role"] == "inner_____func_param"
    _param = chunk["content"]
    _param["language"] = language
    _param["chain_id"] = chain_id
    _param["wallet_type"] = wallet_type
    _param["user_id"] = user_id
    _param["visitor_id"] = visitor_id
    func_name = _param["func_name"]
    sub_func_name = _param["subtype"]
    logger.info(f'>>>>> func_name: {func_name}, sub_func_name: {sub_func_name}, _param: {_param}')
    from genaipf.controller.preset_entry import intent_recog_mapping
    if source not in ['v005', 'v006', 'v008', 'v009', 'v010'] and func_name in intent_recog_mapping:
        func = intent_recog_mapping[func_name]["func"]
        need_spec_gen_l = intent_recog_mapping[func_name]["need_spec_gen_l"]
        _messages = [x for x in messages if x["role"] != "system"]
        need_spec, intent = await func(_messages, _param)
        if need_spec:
            _spec_gen = intent_recog_mapping[func_name][intent]
            _g = _spec_gen(_param)
            async for _x in _g:
                yield _x
            return
        else:
            pass
    already_sources = False
    if sources:
        already_sources = True
    if is_need_search and (func_name not in not_need_sources):
        convert_task_start_time = time.perf_counter()
        sources, related_qa, _ = await sources_task
        convert_task_emd_time = time.perf_counter()
        elapsed_related_questions_task_time = (convert_task_start_time - convert_task_emd_time) * 1000
        logger.info(f'=====================>convert_task_questions_task耗时：{elapsed_related_questions_task_time:.3f}毫秒')
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
        # yield get_format_output("chatSerpResults", [])  #  TODO 暂时屏蔽RAG来源
        # yield get_format_output("chatSerpResults", sources)
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
            if _type == 'tx_hash_analysis':
                func_name = _type
                sub_func_name = _type
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
    if (func_name not in not_need_search and sub_func_name not in ['coin_swap1','transfer_only', 'why_can_not_transfer_out', 'buy_but_not_receive']) or (func_name == 'generate_report' and presetContent == {}) or source in ['v201', 'v202', 'v203', 'v204', 'v210'] or func_name in need_gpt or owner == 'Trust Wallet':
        _messages = [x for x in messages if x["role"] != "system"]
        msgs = _messages[::]
        resp2 = await aref_answer_gpt_generator(msgs, model, language, _type, str(picked_content), related_qa, source, owner, output_type=output_type, llm_model=llm_model)
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



async def run_tool_agent(chunk, messages, newest_question, model, language, related_qa, source, owner, sources=[], is_need_search=False, sources_task=None, chain_id=''):
    _param = chunk["content"]
    func_name = _param["func_name"]
    sub_func_name = _param["sub_func_name"]
    whole_func_name = f"{func_name}_____{sub_func_name}"
    from genaipf.dispatcher.tool_agent import tool_agent_mapping, tool_agent_sub_mapping
    if whole_func_name in tool_agent_sub_mapping:
        tool_agent_func = tool_agent_sub_mapping[whole_func_name]["func"]
    else:
        tool_agent_func = tool_agent_mapping[func_name]["func"]
    resp = tool_agent_func(messages, newest_question, model, language, related_qa, source, owner, sources=[], is_need_search=False, sources_task=None, chain_id='')
    async for item in resp:
        yield item
