import json
import asyncio
from genaipf.dispatcher.functions import gpt_functions
from genaipf.dispatcher.utils import openai, OPENAI_PLUS_MODEL, openai_chat_completion_acreate
from genaipf.utils.log_utils import logger
from datetime import datetime
from genaipf.dispatcher.prompts_v001 import LionPrompt
import genaipf.dispatcher.prompts_v002 as prompts_v002
import genaipf.dispatcher.prompts_v003 as prompts_v003
import genaipf.dispatcher.prompts_v004 as prompts_v004
# from openai.error import InvalidRequestError
from openai import BadRequestError
from genaipf.utils.redis_utils import RedisConnectionPool

# temperature=2 # 值在[0,1]之间，越大表示回复越具有不确定性
# max_tokens=2000 # 输出的最大 token 数
# top_p=0.9 # 过滤掉低于阈值的 token 确保结果不散漫
# frequency_penalty=0.1 # [-2,2]之间，该值越大则更倾向于产生不同的内容
# presence_penalty=0.1 # [-2,2]之间，该值越大则更倾向于产生不同的内容
temperature=0.8 # 值在[0,1]之间，越大表示回复越具有不确定性
max_tokens=2000 # 输出的最大 token 数
top_p=0.85 # 过滤掉低于阈值的 token 确保结果不散漫
frequency_penalty=0.3 # [-2,2]之间，该值越大则更倾向于产生不同的内容
presence_penalty=0.2 # [-2,2]之间，该值越大则更倾向于产生不同的内容


def generate_unique_id():
    redis_client = RedisConnectionPool().get_connection()
    return redis_client.incr('unique_id')

def get_format_output(role, content, mode=None):
    if mode == "voice_mp3_v001":
        return {
            "role": role, 
            "type": "voice", 
            "format": "mp3", 
            "version": "v001", 
            "content": content
        }
    else:
        return {"role": role, "type": "text", "format": "text", "version": "v001", "content": content}

async def aget_error_generator(msg="ERROR"):
    for c in msg:
        await asyncio.sleep(0.02)
        yield get_format_output("error", c)

async def awrap_gpt_generator(gpt_response):
    resp = gpt_response
    chunk = await resp.__anext__()
    _func_or_text = chunk.choices[0].delta.function_call
    if _func_or_text:
        mode1 = "func"
    else:
        mode1 = "text"
    if mode1 == "text":
        yield get_format_output("step", "llm_yielding")
        c0 = chunk.choices[0].delta.content
        _tmp_text = ""
        _tmp_text += c0
        yield get_format_output("gpt", c0)
        async for chunk in resp:
            _gpt_letter = chunk.choices[0].delta.content
            if _gpt_letter:
                _tmp_text += _gpt_letter
                yield get_format_output("gpt", _gpt_letter)
        yield get_format_output("inner_____gpt_whole_text", _tmp_text)
    elif mode1 == "func":
        yield get_format_output("step", "agent_routing")
        big_func_name = _func_or_text.name
        func_name, sub_func_name = big_func_name.split("_____")
        _arguments = _func_or_text.arguments
        async for chunk in resp:
            _func_json = chunk.choices[0].delta.function_call
            if _func_json:
                _arguments += _func_json.arguments
        _param = json.loads(_arguments)
        _param["func_name"] = func_name
        _param["sub_func_name"] = sub_func_name
        _param["subtype"] = sub_func_name
        yield get_format_output("inner_____func_param", _param)
        

async def afunc_gpt_generator(messages, functions=gpt_functions, language=LionPrompt.default_lang, model='', picked_content="", related_qa=[], source='v001', owner=''):
    '''
    "messages": [
        {"role": "user", "content": "Hello"},
        {"role": "assistant", "content": "Sure, how can I assist you?"},
        {"role": "user", "content": "Where is Tokyo?"},
    ]
    '''
    use_model = 'gpt-3.5-turbo-16k'
    if model == 'ml-plus':
        use_model = OPENAI_PLUS_MODEL
    for i in range(5):
        mlength = len(messages)
        try:
            if source == 'v002':
                content = prompts_v002.LionPrompt.get_afunc_prompt(language, picked_content, related_qa, use_model)
            elif source == 'v003':
                data = {
                    'format' : owner
                }
                content = prompts_v003.LionPrompt.get_afunc_prompt(language, picked_content, related_qa, use_model, data)
            elif source == 'v004':
                content = prompts_v004.LionPrompt.get_afunc_prompt(language, picked_content, related_qa, use_model)
            else:
                content = LionPrompt.get_afunc_prompt(language, picked_content, related_qa, use_model, '', owner)
            system = {
                "role": "system",
                "content": content
            }
            # messages.insert(0, system)
            _messages = [system] + messages
            # print(f'>>>>>test 004 : {_messages}')
            response = await openai_chat_completion_acreate(
                model=use_model,
                messages=_messages,
                functions=functions,
                temperature=temperature,  # 值在[0,1]之间，越大表示回复越具有不确定性
                max_tokens=max_tokens, # 输出的最大 token 数
                top_p=top_p, # 过滤掉低于阈值的 token 确保结果不散漫
                frequency_penalty=frequency_penalty,  # [-2,2]之间，该值越大则更倾向于产生不同的内容
                presence_penalty=presence_penalty,  # [-2,2]之间，该值越大则更倾向于产生不同的内容
                stream=True
            )
            logger.info('afunc_gpt_generator called')
            return awrap_gpt_generator(response)
        except BadRequestError as e:
            print(e)
            logger.error(f'afunc_gpt_generator BadRequestError {e}', e)
            messages = messages[mlength // 2:]
        except Exception as e:
            print(e)
            logger.error(f'afunc_gpt_generator question_JSON call gpt4 error {e}', e)
            return aget_error_generator(str(e))
    return aget_error_generator("error after retry many times")


async def aref_answer_gpt_generator(messages, model='', language=LionPrompt.default_lang, preset_name=None, picked_content="", related_qa=[], source='v001', owner=''):
    use_model = 'gpt-3.5-turbo-16k'
    if model == 'ml-plus':
        use_model = OPENAI_PLUS_MODEL
    for i in range(5):
        mlength = len(messages)
        try:
            if source == 'v002':
                content = prompts_v002.LionPrompt.get_aref_answer_prompt(language, preset_name, picked_content, related_qa, use_model)
            elif source == 'v003':
                data = {
                    'format' : owner
                }
                content = prompts_v003.LionPrompt.get_aref_answer_prompt(language, preset_name, picked_content, related_qa, use_model, data)
            elif source == 'v004':
                content = prompts_v004.LionPrompt.get_aref_answer_prompt(language, preset_name, picked_content, related_qa, use_model)
            else:
                content = LionPrompt.get_aref_answer_prompt(language, preset_name, picked_content, related_qa, use_model, '', owner)
            system = {
                "role": "system",
                "content": content
            }
            # messages.insert(0, system)
            # print(f'>>>>>test 003 : {messages}')
            _messages = [system] + messages
            response = await openai_chat_completion_acreate(
                model=use_model,
                messages=_messages,
                functions=None,
                temperature=temperature,  # 值在[0,1]之间，越大表示回复越具有不确定性
                max_tokens=max_tokens, # 输出的最大 token 数
                top_p=top_p, # 过滤掉低于阈值的 token 确保结果不散漫
                frequency_penalty=frequency_penalty,  # [-2,2]之间，该值越大则更倾向于产生不同的内容
                presence_penalty=presence_penalty,  # [-2,2]之间，该值越大则更倾向于产生不同的内容
                stream=True
            )
            logger.info(f'aref_answer_gpt called')
            return awrap_gpt_generator(response)
        except BadRequestError as e:
            print(e)
            logger.error(f'aref_answer_gpt_generator BadRequestError {e}', e)
            messages = messages[mlength // 2:]
        except Exception as e:
            print(e)
            logger.error(f'aref_answer_gpt_generator question_JSON call gpt4 error {e}', e)
            return aget_error_generator(str(e))
    return aget_error_generator("error after retry many times")

async def aref_oneshot_gpt_generator(messages, model='', language=LionPrompt.default_lang, preset_name=None, picked_content="", related_qa=[], data=None, stream=False, mode=None):
    front_messages = messages
    gpt_prams = data.get("gpt_prams", {})
    use_model = 'gpt-3.5-turbo-16k'
    if model == 'ml-plus':
        use_model = OPENAI_PLUS_MODEL
    try:
        if mode == "raw":
            _messages = [{"role": x["role"], "content": x["content"]} for x in front_messages]
            _check_something = LionPrompt.get_merge_ref_and_input_prompt(str(picked_content), related_qa, "question", language, preset_name, data)
        else:
            system = {
                "role": "system",
                "content": LionPrompt.get_aref_answer_prompt(language, preset_name, picked_content, related_qa, use_model, data)
            }
            newest_question = front_messages[-1]["content"]
            merged_ref_text = LionPrompt.get_merge_ref_and_input_prompt(str(picked_content), related_qa, newest_question, language, preset_name, data)
            _messages = [system] + [{"role": "user", "content": merged_ref_text}]
            
        response = await openai_chat_completion_acreate(
            model=use_model,
            messages=_messages,
            functions=None,
            temperature=gpt_prams.get("temperature", temperature),  # 值在[0,1]之间，越大表示回复越具有不确定性
            max_tokens=gpt_prams.get("max_tokens", max_tokens), # 输出的最大 token 数
            top_p=gpt_prams.get("top_p", top_p), # 过滤掉低于阈值的 token 确保结果不散漫
            frequency_penalty=gpt_prams.get("frequency_penalty", frequency_penalty),  # [-2,2]之间，该值越大则更倾向于产生不同的内容
            presence_penalty=gpt_prams.get("presence_penalty", presence_penalty),  # [-2,2]之间，该值越大则更倾向于产生不同的内容
            stream=stream
        )
        logger.info(f'aref_oneshot_gpt_generator called')
        return response
    except BadRequestError as e:
        print(e)
        logger.error(f'aref_answer_gpt_generator BadRequestError {e}', e)
        raise e
    except Exception as e:
        print(e)
        logger.error(f'aref_answer_gpt_generator question_JSON call gpt4 error {e}', e)
        raise e
