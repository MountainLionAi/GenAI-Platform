import os
import asyncio
import typing
import openai
import tqdm
import pandas as pd
from functools import cache
from qdrant_client import QdrantClient
from qdrant_client.http import models
import tiktoken
from openai import OpenAI, AsyncOpenAI
from openai._types import NOT_GIVEN
from genaipf.conf.server import os
from anthropic import AsyncAnthropic

from genaipf.utils.log_utils import logger
import json
from genaipf.utils.common_utils import check_is_json
from genaipf.utils.interface_error_notice_tg_bot_util import send_notice_message
import traceback

PERPLEXITY_API_KEY=os.getenv("PERPLEXITY_API_KEY")
PERPLEXITY_URL=os.getenv("PERPLEXITY_URL", "https://api.perplexity.ai")
DEEPSEEK_API_KEY=os.getenv("DEEPSEEK_API_KEY")
DEEPSEEK_URL=os.getenv("DEEPSEEK_URL", "https://api.deepseek.com")
openai.api_key = os.getenv("OPENAI_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
OPENAI_API_KEY_FOR_PREDICT = os.getenv("OPENAI_API_KEY_FOR_PREDICT")
SIMPLE_CHAT_MODEL = os.getenv("SIMPLE_CHAT_MODEL")
MAX_CH_LENGTH_GPT3 = 8000
MAX_CH_LENGTH_GPT4 = 3000
MAX_CH_LENGTH_QA_GPT3 = 3000
MAX_CH_LENGTH_QA_GPT4 = 1500
OPENAI_PLUS_MODEL = "gpt-4.1-2025-04-14"
CLAUDE_MODEL = "claude-sonnet-4-20250514"
PERPLEXITY_MODEL = "sonar-pro"  # "sonar-small-online"
MISTRAL_MODEL = "open-mixtral-8x22b"
DEEPSEEK_V3_MODEL = os.getenv("DEEPSEEK_V3_MODEL")
DEEPSEEK_R1_MODEL = os.getenv("DEEPSEEK_R1_MODEL")
MOUNTAINLION_C1_MODEL = os.getenv("MOUNTAINLION_C1_MODEL")
MOUNTAINLION_C1_D_MODEL = os.getenv("MOUNTAINLION_C1_D_MODEL")
QWEN_MODEL = os.getenv("DS_OPENROUTER_MODEL_QWEN")
qdrant_url = "http://localhost:6333"

openai_client = OpenAI(
    # defaults to os.environ.get("OPENAI_API_KEY")
    api_key=openai.api_key,
)
# async_openai_client = AsyncOpenAI(
#     # defaults to os.environ.get("OPENAI_API_KEY")
#     api_key=openai.api_key,
# )

from genaipf.conf.server import PLUGIN_NAME
from genaipf.conf.server import SUB_VDB_QA_PREFIX, SUB_VDB_GPT_FUNC_PREFIX
vdb_prefix = PLUGIN_NAME

qa_coll_name = f"{SUB_VDB_QA_PREFIX}{vdb_prefix}_filtered_qa"
gpt_func_coll_name = f"{SUB_VDB_GPT_FUNC_PREFIX}{vdb_prefix}_gpt_func"

client = QdrantClient(qdrant_url)

@cache
def get_embedding(text, model = "text-embedding-ada-002"):
    # result = openai.Embedding.create(
    text = limit_tokens_from_string(text, model, 8192)
    result = openai_client.embeddings.create(
        input=text,
        model=model,
    )
    # embedding = result["data"][0]["embedding"]
    embedding = result.data[0].embedding
    return embedding

@cache
def get_local_embedding(text, model="llama3"):
    #from langchain_ollama import OllamaEmbeddings
    # embeddings_model = OllamaEmbeddings(model)
    # text = embeddings_model.embed_documents(text, model)
    # embedding = text[0]
    # return embedding
    from ollama import embed
    print("into local embeddings")
    response = embed(model=model, input=text)
    return response['embeddings'][0]

async def openai_chat_completion_acreate(
    model, messages, functions,
    temperature, max_tokens, top_p, frequency_penalty, presence_penalty, stream
):
    try:
        if model == PERPLEXITY_MODEL:
            logger.info(f"调用perplexity模型传入的消息列表:{messages}")
            async_openai_client = AsyncOpenAI(api_key=PERPLEXITY_API_KEY, base_url=PERPLEXITY_URL)
            try:
                if functions:
                    response = await asyncio.wait_for(
                        async_openai_client.chat.completions.create(
                            model=model,
                            messages=messages,
                            functions=functions if functions else NOT_GIVEN,
                            temperature=temperature,  # 值在[0,1]之间，越大表示回复越具有不确定性
                            max_tokens=max_tokens, # 输出的最大 token 数
                            top_p=top_p, # 过滤掉低于阈值的 token 确保结果不散漫
                            presence_penalty=presence_penalty,  # [-2,2]之间，该值越大则更倾向于产生不同的内容
                            stream=stream
                        ),
                        timeout=60.0  # 设置超时时间为180秒
                    )
                else:
                    logger.info(f"调用perplexity模型传入的消息列表:{messages}")
                    response = await asyncio.wait_for(
                        async_openai_client.chat.completions.create(
                            model=model,
                            messages=messages,
                            temperature=temperature,  # 值在[0,1]之间，越大表示回复越具有不确定性
                            max_tokens=max_tokens, # 输出的最大 token 数
                            top_p=top_p, # 过滤掉低于阈值的 token 确保结果不散漫
                            presence_penalty=presence_penalty,  # [-2,2]之间，该值越大则更倾向于产生不同的内容
                            stream=stream
                        ),
                        timeout=60.0  # 设置超时时间为180秒
                    )
            except Exception as e:
                err_message = f"调用perplexity模型出现异常：{e}"
                logger.error(err_message)
                logger.error(traceback.format_exc())
                await send_notice_message('genai_utils', 'openai_chat_completion_acreate', 0, err_message, 3)
                raise e
        elif model == DEEPSEEK_V3_MODEL:
            logger.info(f"调用deepseek模型传入的消息列表:{messages}")
            async_openai_client = AsyncOpenAI(
                api_key=DEEPSEEK_API_KEY, base_url=DEEPSEEK_URL
            )
            try:
                if functions:
                    response = await asyncio.wait_for(
                        async_openai_client.chat.completions.create(
                            model=model,
                            messages=messages,
                            functions=functions if functions else NOT_GIVEN,
                            temperature=temperature,  # 值在[0,1]之间，越大表示回复越具有不确定性
                            max_tokens=max_tokens, # 输出的最大 token 数
                            top_p=top_p, # 过滤掉低于阈值的 token 确保结果不散漫
                            presence_penalty=presence_penalty,  # [-2,2]之间，该值越大则更倾向于产生不同的内容
                            stream=stream
                        ),
                        timeout=60.0  # 设置超时时间为180秒
                    )
                else:
                    logger.info(f"调用deepseek模型传入的消息列表:{messages}")
                    response = await asyncio.wait_for(
                        async_openai_client.chat.completions.create(
                            model=model,
                            messages=messages,
                            temperature=temperature,  # 值在[0,1]之间，越大表示回复越具有不确定性
                            max_tokens=max_tokens, # 输出的最大 token 数
                            top_p=top_p, # 过滤掉低于阈值的 token 确保结果不散漫
                            presence_penalty=presence_penalty,  # [-2,2]之间，该值越大则更倾向于产生不同的内容
                            stream=stream
                        ),
                        timeout=60.0  # 设置超时时间为180秒
                    )
            except Exception as e:
                err_message = f"调用deepseek模型出现异常：{e}"
                logger.error(err_message)
                logger.error(traceback.format_exc())
                await send_notice_message('genai_utils', 'openai_chat_completion_acreate', 0, err_message, 3)
                raise e
        elif model == DEEPSEEK_R1_MODEL:
            logger.info(f"调用deepseek模型传入的消息列表:{messages}")
            async_openai_client = AsyncOpenAI(
                api_key=DEEPSEEK_API_KEY, base_url=DEEPSEEK_URL
            )
            try:
                if functions:
                    response = await asyncio.wait_for(
                        async_openai_client.chat.completions.create(
                            model=model,
                            messages=messages,
                            functions=functions if functions else NOT_GIVEN,
                            temperature=temperature,  # 值在[0,1]之间，越大表示回复越具有不确定性
                            max_tokens=max_tokens, # 输出的最大 token 数
                            top_p=top_p, # 过滤掉低于阈值的 token 确保结果不散漫
                            presence_penalty=presence_penalty,  # [-2,2]之间，该值越大则更倾向于产生不同的内容
                            stream=stream
                        ),
                        timeout=60.0  # 设置超时时间为180秒
                    )
                else:
                    logger.info(f"调用deepseek模型传入的消息列表:{messages}")
                    response = await asyncio.wait_for(
                        async_openai_client.chat.completions.create(
                            model=model,
                            messages=messages,
                            temperature=temperature,  # 值在[0,1]之间，越大表示回复越具有不确定性
                            max_tokens=max_tokens, # 输出的最大 token 数
                            top_p=top_p, # 过滤掉低于阈值的 token 确保结果不散漫
                            presence_penalty=presence_penalty,  # [-2,2]之间，该值越大则更倾向于产生不同的内容
                            stream=stream
                        ),
                        timeout=60.0  # 设置超时时间为180秒
                    )
            except Exception as e:
                err_message = f"调用deepseek模型出现异常：{e}"
                logger.error(err_message)
                logger.error(traceback.format_exc())
                await send_notice_message('genai_utils', 'openai_chat_completion_acreate', 0, err_message, 3)
                raise e
        else:
            async_openai_client = AsyncOpenAI(
                # defaults to os.environ.get("OPENAI_API_KEY")
                api_key=openai.api_key,
            )
            # print(f'>>>>>>>>>test001.1 async_openai_client.chat.completions.create')
            if functions:
                # try:
                #     _base_urls = os.getenv("COMPATABLE_OPENAI_BASE_URLS", [])
                #     _base_urls = json.loads(_base_urls)
                #     _api_keys = os.getenv("COMPATABLE_OPENAI_API_KEYS", [])
                #     _api_keys = json.loads(_api_keys)
                #     if len(_base_urls) == 0:
                #         raise
                #     import random
                #     i = random.randint(0, len(_base_urls) - 1)
                #     _base_url = _base_urls[i]
                #     _api_key = _api_keys[i]
                #     _client = AsyncOpenAI(api_key=_api_key, base_url=_base_url)
                #     tools = []
                #     tool_choice = 'auto'
                #     for function in functions:
                #         tools.append(
                #             {
                #                 "type": "function",
                #                 "function": function
                #             }
                #         )
                #     response = await asyncio.wait_for(
                #         _client.chat.completions.create(
                #             model=model,
                #             messages=messages,
                #             tools=tools,
                #             tool_choice=tool_choice,
                #             temperature=temperature,  # 值在[0,1]之间，越大表示回复越具有不确定性
                #             max_tokens=max_tokens, # 输出的最大 token 数
                #             top_p=top_p, # 过滤掉低于阈值的 token 确保结果不散漫
                #             frequency_penalty=frequency_penalty,  # [-2,2]之间，该值越大则更倾向于产生不同的内容
                #             presence_penalty=presence_penalty,  # [-2,2]之间，该值越大则更倾向于产生不同的内容
                #             stream=stream
                #         ),
                #         timeout=60.0  # 设置超时时间为180秒
                #     )
                #     logger.info(f'>>>>>>>>>other openai use {_base_url}')
                #     return response
                # except Exception as e:
                #     logger.error(f'>>>>>>>>>other openai error: {e}')
                #     pass
                response = await asyncio.wait_for(
                    async_openai_client.chat.completions.create(
                        model=model,
                        messages=messages,
                        functions=functions if functions else NOT_GIVEN,
                        temperature=temperature,  # 值在[0,1]之间，越大表示回复越具有不确定性
                        max_tokens=max_tokens, # 输出的最大 token 数
                        top_p=top_p, # 过滤掉低于阈值的 token 确保结果不散漫
                        frequency_penalty=frequency_penalty,  # [-2,2]之间，该值越大则更倾向于产生不同的内容
                        presence_penalty=presence_penalty,  # [-2,2]之间，该值越大则更倾向于产生不同的内容
                        stream=stream
                    ),
                    timeout=60.0  # 设置超时时间为180秒
                )
            else:
                # try:
                #     _base_urls = os.getenv("COMPATABLE_OPENAI_BASE_URLS", [])
                #     _base_urls = json.loads(_base_urls)
                #     _api_keys = os.getenv("COMPATABLE_OPENAI_API_KEYS", [])
                #     _api_keys = json.loads(_api_keys)
                #     if len(_base_urls) == 0:
                #         raise
                #     import random
                #     i = random.randint(0, len(_base_urls) - 1)
                #     _base_url = _base_urls[i]
                #     _api_key = _api_keys[i]
                #     _client = AsyncOpenAI(api_key=_api_key, base_url=_base_url)
                #     response = await asyncio.wait_for(
                #         _client.chat.completions.create(
                #             model=model,
                #             messages=messages,
                #             temperature=temperature,  # 值在[0,1]之间，越大表示回复越具有不确定性
                #             max_tokens=max_tokens, # 输出的最大 token 数
                #             top_p=top_p, # 过滤掉低于阈值的 token 确保结果不散漫
                #             frequency_penalty=frequency_penalty,  # [-2,2]之间，该值越大则更倾向于产生不同的内容
                #             presence_penalty=presence_penalty,  # [-2,2]之间，该值越大则更倾向于产生不同的内容
                #             stream=stream
                #         ),
                #         timeout=60.0  # 设置超时时间为180秒
                #     )
                #     logger.info(f'>>>>>>>>>other openai use {_base_url}')
                #     return response
                # except Exception as e:
                #     logger.error(f'>>>>>>>>>other openai error: {e}')
                #     err_message = f"调用other openai模型出现异常：{e}"
                #     logger.error(err_message)
                #     logger.error(traceback.format_exc())
                #     await send_notice_message('genai_utils', 'openai_chat_completion_acreate', 0, err_message, 3)
                #     raise e
                response = await asyncio.wait_for(
                    async_openai_client.chat.completions.create(
                        model=model,
                        messages=messages,
                        temperature=temperature,  # 值在[0,1]之间，越大表示回复越具有不确定性
                        max_tokens=max_tokens, # 输出的最大 token 数
                        top_p=top_p, # 过滤掉低于阈值的 token 确保结果不散漫
                        frequency_penalty=frequency_penalty,  # [-2,2]之间，该值越大则更倾向于产生不同的内容
                        presence_penalty=presence_penalty,  # [-2,2]之间，该值越大则更倾向于产生不同的内容
                        stream=stream
                    ),
                    timeout=60.0  # 设置超时时间为180秒
                )
            # print(f'>>>>>>>>>test001 async_openai_client.chat.completions.create, response: {response}')
    except asyncio.TimeoutError as e:
        logger.error(f'>>>>>>>>>test002 async_openai_client.chat.completions.create, e: {e}')
        raise Exception("The request to OpenAI timed out after 3 minutes.")
    except Exception as e:
        logger.error(f'>>>>>>>>>test003 async_openai_client.chat.completions.create, e: {e}')
        # openai失败用deepbricks
        if model == OPENAI_PLUS_MODEL:
            model = 'gpt-4o-2024-08-06'
        if functions:
            try:
                _base_urls = os.getenv("COMPATABLE_OPENAI_BASE_URLS", [])
                _base_urls = json.loads(_base_urls)
                _api_keys = os.getenv("COMPATABLE_OPENAI_API_KEYS", [])
                _api_keys = json.loads(_api_keys)
                if len(_base_urls) == 0:
                    raise
                import random
                i = random.randint(0, len(_base_urls) - 1)
                _base_url = _base_urls[i]
                _api_key = _api_keys[i]
                _client = AsyncOpenAI(api_key=_api_key, base_url=_base_url)
                tools = []
                tool_choice = 'auto'
                for function in functions:
                    tools.append(
                        {
                            "type": "function",
                            "function": function
                        }
                    )
                response = await asyncio.wait_for(
                    _client.chat.completions.create(
                        model=model,
                        messages=messages,
                        tools=tools,
                        tool_choice=tool_choice,
                        temperature=temperature,  # 值在[0,1]之间，越大表示回复越具有不确定性
                        max_tokens=max_tokens, # 输出的最大 token 数
                        top_p=top_p, # 过滤掉低于阈值的 token 确保结果不散漫
                        frequency_penalty=frequency_penalty,  # [-2,2]之间，该值越大则更倾向于产生不同的内容
                        presence_penalty=presence_penalty,  # [-2,2]之间，该值越大则更倾向于产生不同的内容
                        stream=stream
                    ),
                    timeout=60.0  # 设置超时时间为180秒
                )
                logger.info(f'>>>>>>>>>other openai use {_base_url}')
                return response
            except Exception as e:
                logger.error(f'>>>>>>>>>other openai error: {e}')
                err_message = f"调用other openai functions模型出现异常：{e}"
                logger.error(err_message)
                logger.error(traceback.format_exc())
                await send_notice_message('genai_utils', 'openai_chat_completion_acreate', 0, err_message, 4)
                raise e
        else:
            try:
                _base_urls = os.getenv("COMPATABLE_OPENAI_BASE_URLS", [])
                _base_urls = json.loads(_base_urls)
                _api_keys = os.getenv("COMPATABLE_OPENAI_API_KEYS", [])
                _api_keys = json.loads(_api_keys)
                if len(_base_urls) == 0:
                    raise
                import random
                i = random.randint(0, len(_base_urls) - 1)
                _base_url = _base_urls[i]
                _api_key = _api_keys[i]
                _client = AsyncOpenAI(api_key=_api_key, base_url=_base_url)
                response = await asyncio.wait_for(
                    _client.chat.completions.create(
                        model=model,
                        messages=messages,
                        temperature=temperature,  # 值在[0,1]之间，越大表示回复越具有不确定性
                        max_tokens=max_tokens, # 输出的最大 token 数
                        top_p=top_p, # 过滤掉低于阈值的 token 确保结果不散漫
                        frequency_penalty=frequency_penalty,  # [-2,2]之间，该值越大则更倾向于产生不同的内容
                        presence_penalty=presence_penalty,  # [-2,2]之间，该值越大则更倾向于产生不同的内容
                        stream=stream
                    ),
                    timeout=60.0  # 设置超时时间为180秒
                )
                logger.info(f'>>>>>>>>>other openai use {_base_url}')
                return response
            except Exception as e:
                logger.error(f'>>>>>>>>>other openai error: {e}')
                err_message = f"调用other openai模型出现异常：{e}"
                logger.error(err_message)
                logger.error(traceback.format_exc())
                await send_notice_message('genai_utils', 'openai_chat_completion_acreate', 0, err_message, 4)
                raise e
        raise e
    return response

async def simple_achat(messages: typing.List[typing.Mapping[str, str]], model: str = 'gpt-4o-mini'):
    from llama_index.llms import ChatMessage, OpenAI as OpenAI2
    OPENAI_API_KEY = openai.api_key
    _msgs = []
    for m in messages:
        if m["role"] in ["system", "user", "assistant"]:
            _msgs.append(ChatMessage(
                role=m["role"],
                content=m["content"]
            ))
    resp = await OpenAI2(model=model, api_key=OPENAI_API_KEY).achat(_msgs)
    return resp.message.content

async def async_simple_chat(messages: typing.List[typing.Mapping[str, str]], stream: bool = False, model: str = 'gpt-4o-mini', key_type: str = 'normal'):
    try:
        if SIMPLE_CHAT_MODEL == 'openai':
            expired_time = 30.0
            api_key = OPENAI_API_KEY
            if key_type != 'normal':
                expired_time = 60.0
                api_key = OPENAI_API_KEY_FOR_PREDICT
            async_openai_client = AsyncOpenAI(
                api_key=api_key,
            )
            response = await asyncio.wait_for(
                async_openai_client.chat.completions.create(
                    model=model,
                    messages=messages,
                    stream=stream
                ),
                timeout=expired_time  # 设置超时时间为180秒
            )
            if stream:
                return response
            else:
                return response.choices[0].message.content
        elif SIMPLE_CHAT_MODEL == 'claude':
            model = CLAUDE_MODEL
            expired_time = 60.0
            claude_client = AsyncAnthropic(api_key=ANTHROPIC_API_KEY)
            response = await asyncio.wait_for(
                claude_client.messages.create(
                    model=model,
                    max_tokens=2048,
                    temperature=0,
                    messages=messages,
                    stream=stream
                ),
                timeout=expired_time  # 设置超时时间为180秒
            )
            if stream:
                return response
            else:
                return response.content[0].text

    except asyncio.TimeoutError as e:
        err_message = f'>>>>>>>>>async_simple_chat:test002 创建对话失败,出现超时异常，当前使用模型{SIMPLE_CHAT_MODEL}，模型版本: {model}, e: {e}'
        logger.error(err_message)
        await send_notice_message('genai_utils', 'async_simple_chat', 0, err_message, 3)
        raise Exception("async_simple_chat:The request to OpenAI timed out after 3 minutes.")
    except Exception as e:
        logger.error(f'>>>>>>>>>async_simple_chat:test003 async_openai_client.chat.completions.create, e: {e}')
        if SIMPLE_CHAT_MODEL == 'openai':
            if model == OPENAI_PLUS_MODEL:
                model = 'gpt-4o-2024-08-06'
        else:
            model = 'gpt-4o-2024-08-06'
        try:
            _base_urls = os.getenv("COMPATABLE_OPENAI_BASE_URLS", [])
            _base_urls = json.loads(_base_urls)
            _api_keys = os.getenv("COMPATABLE_OPENAI_API_KEYS", [])
            _api_keys = json.loads(_api_keys)
            if len(_base_urls) == 0:
                raise
            import random
            i = random.randint(0, len(_base_urls) - 1)
            _base_url = _base_urls[i]
            _api_key = _api_keys[i]
            _client = AsyncOpenAI(api_key=_api_key, base_url=_base_url)
            response = await asyncio.wait_for(
                _client.chat.completions.create(
                    model=model,
                    messages=messages,
                    stream=stream
                ),
                timeout=60.0  # 设置超时时间为180秒
            )
            logger.info(f'>>>>>>>>>async_simple_chat openai use {_base_url}')
            if stream:
                return response
            else:
                return response.choices[0].message.content
        except Exception as e:
            logger.error(f'>>>>>>>>>async_simple_chat openai error: {e}')
            err_message = f"调用async_simple_chat出现异常：使用的模型={model}"
            err_message = traceback.format_exc()
            logger.error(err_message)
            await send_notice_message('genai_utils', 'async_simple_chat', 0, err_message, 3)
            raise e


async def async_simple_chat_with_model(messages: typing.List[typing.Mapping[str, str]], stream: bool = False, model: str = 'gpt-4o-mini', base_model:str = 'openai', key_type: str = 'normal', system_msg=''):
    try:
        simple_achat_model = base_model
        if simple_achat_model == 'openai':
            expired_time = 30.0
            api_key = OPENAI_API_KEY
            if key_type != 'normal':
                expired_time = 60.0
                api_key = OPENAI_API_KEY_FOR_PREDICT
            async_openai_client = AsyncOpenAI(
                api_key=api_key,
            )
            response = await asyncio.wait_for(
                async_openai_client.chat.completions.create(
                    model=model,
                    messages=messages,
                    stream=stream
                ),
                timeout=expired_time  # 设置超时时间为180秒
            )
            if stream:
                return response
            else:
                return response.choices[0].message.content
        elif simple_achat_model == 'claude':
            model = CLAUDE_MODEL
            expired_time = 60.0
            claude_client = AsyncAnthropic(api_key=ANTHROPIC_API_KEY)
            if system_msg:
                response = await asyncio.wait_for(
                    claude_client.messages.create(
                        model=model,
                        max_tokens=2048,
                        temperature=0,
                        messages=messages,
                        stream=stream,
                        system=system_msg
                    ),
                    timeout=expired_time  # 设置超时时间为180秒
                )
            else:
                response = await asyncio.wait_for(
                    claude_client.messages.create(
                        model=model,
                        max_tokens=2048,
                        temperature=0,
                        messages=messages,
                        stream=stream
                    ),
                    timeout=expired_time  # 设置超时时间为180秒
                )
            if stream:
                return response
            else:
                return response.content[0].text

    except asyncio.TimeoutError as e:
        err_message = f'>>>>>>>>>async_simple_chat:test002 创建对话失败,出现超时异常，当前使用模型{SIMPLE_CHAT_MODEL}，模型版本: {model}, e: {e}'
        logger.error(err_message)
        await send_notice_message('genai_utils', 'async_simple_chat', 0, err_message, 3)
        raise Exception("async_simple_chat:The request to OpenAI timed out after 3 minutes.")
    except Exception as e:
        logger.error(f'>>>>>>>>>async_simple_chat:test003 async_openai_client.chat.completions.create, e: {e}')
        if simple_achat_model == 'openai':
            if model == OPENAI_PLUS_MODEL:
                model = 'gpt-4o-2024-08-06'
        else:
            model = 'gpt-4o-2024-08-06'
        try:
            _base_urls = os.getenv("COMPATABLE_OPENAI_BASE_URLS", [])
            _base_urls = json.loads(_base_urls)
            _api_keys = os.getenv("COMPATABLE_OPENAI_API_KEYS", [])
            _api_keys = json.loads(_api_keys)
            if len(_base_urls) == 0:
                raise
            import random
            i = random.randint(0, len(_base_urls) - 1)
            _base_url = _base_urls[i]
            _api_key = _api_keys[i]
            _client = AsyncOpenAI(api_key=_api_key, base_url=_base_url)
            response = await asyncio.wait_for(
                _client.chat.completions.create(
                    model=model,
                    messages=messages,
                    stream=stream
                ),
                timeout=60.0  # 设置超时时间为180秒
            )
            logger.info(f'>>>>>>>>>async_simple_chat openai use {_base_url}')
            if stream:
                return response
            else:
                return response.choices[0].message.content
        except Exception as e:
            logger.error(f'>>>>>>>>>async_simple_chat openai error: {e}')
            err_message = f"调用async_simple_chat出现异常：{e}"
            logger.error(err_message)
            err_message = traceback.format_exc()
            logger.error(err_message)
            await send_notice_message('genai_utils', 'async_simple_chat', 0, err_message, 3)
            raise e

async def async_simple_chat_stream(messages: typing.List[typing.Mapping[str, str]], model: str='gpt-4o-mini'):
    from genaipf.dispatcher.api import awrap_gpt_generator
    resp = await async_simple_chat(messages, True, model)
    return awrap_gpt_generator(resp, "text")

def merge_ref_and_input_text(ref, input_text, language='en'):
    if language == 'zh' or language == 'cn':
        return f"""可能相关的资料：
```
{ref}
```

Human:
{input_text}？

AI:
"""
    else:
        return f"""Possible related materials:
```
{ref}
```

Human:
{input_text}？

AI:
"""


def get_vdb_topk(text: str, cname: str, sim_th: float = 0.8, topk: int = 3) -> typing.List[typing.Mapping]:
    try:
        _vector = get_embedding(text)
        search_results = client.search(cname, _vector, limit=topk)
        wrapper_result = []
        for result in search_results:
            if result.score >= sim_th:
                wrapper_result.append({'payload': result.payload, 'similarity': result.score})
        return wrapper_result
    except Exception as e:
        logger.error(f"Open AI text embedding error {e}, use llama3 as backup")
        _vector = get_local_embedding(text)
        if cname.startswith('SOURCE'):
            cname_backup = cname[:9] + "_backup" + cname[9:]
        else:
            cname_backup = "_backup" + cname 
        search_results = client.search(cname_backup, _vector, limit=topk)
        wrapper_result = []
        if not cname.endswith('func'):
            sim_th = 0.25
        for result in search_results:
            if result.score >= sim_th:
                wrapper_result.append({'payload': result.payload, 'similarity': result.score})
        return wrapper_result

def get_qa_vdb_topk(text: str, sim_th: float = 0.85, topk: int = 3, source=None) -> typing.List[typing.Mapping]:
    from genaipf.dispatcher.source_mapping import source_mapping
    # # results = get_vdb_topk(text, "qa", sim_th, topk)
    from genaipf.dispatcher.vdb_pairs.qa import vdb_map, qa_maps
    if source in source_mapping:
        vdb_name = source_mapping[source]["qa_vdb"]
        _qa_map_name = source_mapping[source]["qa_map"]
        _qa_map = qa_maps[_qa_map_name]
    else:
        vdb_name = qa_coll_name
        _qa_map = vdb_map
    results = get_vdb_topk(text, vdb_name, sim_th, topk)
    out_l = []
    for x in results:
        _a = _qa_map.get(x["payload"]["q"])
        ans = _a if _a else x["payload"].get("a")
        # if not check_is_json(ans):
        #     data = {
        #         'template': 0,
        #         'ans': ans
        #     }
        #     ans = json.dumps(data)
        v = f'{x["payload"].get("q")}: {ans}'
        out_l.append(v)
    return out_l

def merge_ref_and_qa(picked_content, related_qa, language="en", model=''):
    _ref_text = "\n\n".join(str(picked_content))
    _ref_text = _ref_text.replace("\n", "")
    length = MAX_CH_LENGTH_GPT3
    length_qa = MAX_CH_LENGTH_QA_GPT3
    if model == OPENAI_PLUS_MODEL:
        length = MAX_CH_LENGTH_GPT4
        length_qa = MAX_CH_LENGTH_QA_GPT4
    ref_text = limit_tokens_from_string(_ref_text, model, length)
    # related_qa = get_qa_vdb_topk(newest_question)
    if language == "cn":
        ref_text += "\n\n可能相关的历史问答:\n" + "\n\n".join(related_qa)
    else:
        ref_text += "\n\nPossible related historical questions and answers:\n" + "\n\n".join(related_qa)
    # ref_text = limit_tokens_from_string(_ref_text, model, length + length_qa)
    ref_text = limit_tokens_from_string(ref_text, model, length + length_qa)
    return ref_text

def limit_tokens_from_string(string: str, model: str, limit: int) -> str:
    """Limits the string to a number of tokens (estimated)."""

    try:
        encoding = tiktoken.encoding_for_model(model)
    except:
        encoding = tiktoken.encoding_for_model('gpt2')  # Fallback for others.

    encoded = encoding.encode(string)

    return encoding.decode(encoded[:limit])