from genaipf.dispatcher.functions import gpt_functions
from genaipf.dispatcher.utils import openai, OPENAI_PLUS_MODEL, openai_chat_completion_acreate
from genaipf.utils.log_utils import logger
from datetime import datetime
from genaipf.dispatcher.prompts_v001 import LionPrompt
# from openai.error import InvalidRequestError
from openai import BadRequestError

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

async def afunc_gpt4_generator(messages, functions=gpt_functions, language=LionPrompt.default_lang, model='', picked_content="", related_qa=[]):
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
            system = {
                "role": "system",
                "content": LionPrompt.get_afunc_prompt(language, picked_content, related_qa, use_model)
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
            print('afunc_gpt4_generator called')
            return response
        except BadRequestError as e:
            print(e)
            logger.error(f'afunc_gpt4_generator BadRequestError {e}', e)
            messages = messages[mlength // 2:]
        except Exception as e:
            print(e)
            logger.error(f'afunc_gpt4_generator question_JSON call gpt4 error {e}', e)
            raise e


async def aref_answer_gpt_generator(messages, model='', language=LionPrompt.default_lang, preset_name=None, picked_content="", related_qa=[]):
    use_model = 'gpt-3.5-turbo-16k'
    if model == 'ml-plus':
        use_model = OPENAI_PLUS_MODEL
    for i in range(5):
        mlength = len(messages)
        try:
            system = {
                "role": "system",
                "content": LionPrompt.get_aref_answer_prompt(language, preset_name, picked_content, related_qa, use_model)
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
            print(f'aref_answer_gpt called')
            return response
        except BadRequestError as e:
            print(e)
            logger.error(f'aref_answer_gpt_generator BadRequestError {e}', e)
            messages = messages[mlength // 2:]
        except Exception as e:
            print(e)
            logger.error(f'aref_answer_gpt_generator question_JSON call gpt4 error {e}', e)


async def aref_oneshot_gpt_generator(messages, model='', language=LionPrompt.default_lang, preset_name=None, picked_content="", related_qa=[], data=None):
    front_messages = messages
    use_model = 'gpt-3.5-turbo-16k'
    if model == 'ml-plus':
        use_model = OPENAI_PLUS_MODEL
    try:
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
            temperature=temperature,  # 值在[0,1]之间，越大表示回复越具有不确定性
            max_tokens=max_tokens, # 输出的最大 token 数
            top_p=top_p, # 过滤掉低于阈值的 token 确保结果不散漫
            frequency_penalty=frequency_penalty,  # [-2,2]之间，该值越大则更倾向于产生不同的内容
            presence_penalty=presence_penalty,  # [-2,2]之间，该值越大则更倾向于产生不同的内容
            stream=False
        )
        print(f'aref_oneshot_gpt_generator called')
        return response
    except BadRequestError as e:
        print(e)
        logger.error(f'aref_answer_gpt_generator BadRequestError {e}', e)
        raise e
    except Exception as e:
        print(e)
        logger.error(f'aref_answer_gpt_generator question_JSON call gpt4 error {e}', e)
        raise e
