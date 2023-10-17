from dispatcher.functions import gpt_functions
from dispatcher.utils import openai
from utils.log_utils import logger
from datetime import datetime
from dispatcher.prompts_v001 import LionPrompt
from openai.error import InvalidRequestError


async def afunc_gpt4_generator(messages, functions=gpt_functions, language=LionPrompt.default_lang, model=''):
    '''
    "messages": [
        {"role": "user", "content": "Hello"},
        {"role": "assistant", "content": "Sure, how can I assist you?"},
        {"role": "user", "content": "Where is Tokyo?"},
    ]
    '''
    use_model = 'gpt-3.5-turbo-16k'
    if model == 'ml-plus':
        use_model = 'gpt-4'
    for i in range(5):
        mlength = len(messages)
        try:
            system = {
                "role": "system",
                "content": LionPrompt.get_afunc_prompt(language=language)
            }
            # messages.insert(0, system)
            _messages = [system] + messages
            # print(f'>>>>>test 004 : {_messages}')
            response = await openai.ChatCompletion.acreate(
                model=use_model,
                messages=_messages,
                functions=functions,
                temperature=2,  # 值在[0,1]之间，越大表示回复越具有不确定性
                max_tokens=2000, # 输出的最大 token 数
                top_p=0.9, # 过滤掉低于阈值的 token 确保结果不散漫
                frequency_penalty=0.1,  # [-2,2]之间，该值越大则更倾向于产生不同的内容
                presence_penalty=0.1,  # [-2,2]之间，该值越大则更倾向于产生不同的内容
                stream=True
            )
            print('afunc_gpt4_generator called')
            return response
        except InvalidRequestError as e:
            print(e)
            logger.error(f'afunc_gpt4_generator InvalidRequestError {e}', e)
            messages = messages[mlength // 2:]
        except Exception as e:
            print(e)
            logger.error(f'afunc_gpt4_generator question_JSON call gpt4 error {e}', e)
            raise e


async def aref_answer_gpt_generator(messages, model='', language=LionPrompt.default_lang, preset_name=None):
    use_model = 'gpt-3.5-turbo-16k'
    if model == 'ml-plus':
        use_model = 'gpt-4'
    for i in range(5):
        mlength = len(messages)
        try:
            system = {
                "role": "system",
                "content": LionPrompt.get_aref_answer_prompt(language=language, preset_name=preset_name)
            }
            # messages.insert(0, system)
            # print(f'>>>>>test 003 : {messages}')
            _messages = [system] + messages
            response = await openai.ChatCompletion.acreate(
                model=use_model,
                messages=_messages,
                temperature=2,  # 值在[0,1]之间，越大表示回复越具有不确定性
                max_tokens=2000, # 输出的最大 token 数
                top_p=0.9, # 过滤掉低于阈值的 token 确保结果不散漫
                frequency_penalty=0.1,  # [-2,2]之间，该值越大则更倾向于产生不同的内容
                presence_penalty=0.1,  # [-2,2]之间，该值越大则更倾向于产生不同的内容
                stream=True
            )
            print(f'aref_answer_gpt called')
            return response
        except InvalidRequestError as e:
            print(e)
            logger.error(f'aref_answer_gpt_generator InvalidRequestError {e}', e)
            messages = messages[mlength // 2:]
        except Exception as e:
            print(e)
            logger.error(f'aref_answer_gpt_generator question_JSON call gpt4 error {e}', e)
