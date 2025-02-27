import httpx
import json
from enum import Enum
from typing import List, Dict, Optional
from openai import OpenAI, AsyncOpenAI
from genaipf.utils.log_utils import logger
from genaipf.dispatcher.api import temperature, max_tokens, top_p, presence_penalty
from genaipf.utils.interface_error_notice_tg_bot_util import send_notice_message
import asyncio
import traceback
import os

DS_DMX_API_KEY = os.getenv("DS_DMX_API_KEY")
DS_DMX_API_URL = os.getenv("DS_DMX_API_URL")
DS_DMX_MODEL_V3 = os.getenv("DS_DMX_MODEL_V3")
DS_DMX_MODEL_R1 = os.getenv("DS_DMX_MODEL_R1")

DS_OPENROUTER_API_KEY = os.getenv("DS_OPENROUTER_API_KEY")
DS_OPENROUTER_API_URL = os.getenv("DS_OPENROUTER_API_URL")
DS_OPENROUTER_MODEL_V3 = os.getenv("DS_OPENROUTER_MODEL_V3")
DS_OPENROUTER_MODEL_R1 = os.getenv("DS_OPENROUTER_MODEL_R1")

DS_OFFICIAL_API_KEY = os.getenv("DS_OFFICIAL_API_KEY")
DS_OFFICIAL_API_URL = os.getenv("DS_OFFICIAL_API_URL")
DS_OFFICIAL_MODEL_V3 = os.getenv("DS_OFFICIAL_MODEL_V3")
DS_OFFICIAL_MODEL_R1 = os.getenv("DS_OFFICIAL_MODEL_R1")

class ProviderPriority(Enum):
    DMXAPI = 1
    OPENROUTER = 2
    DEEPSEEK_OFFICIAL = 3

API_INFOs = {
    ProviderPriority.DMXAPI: {
        'API_KEY': DS_DMX_API_KEY,
        'API_URL': DS_DMX_API_URL,
        'MODEL': {
            'V3': DS_DMX_MODEL_V3,
            'R1': DS_DMX_MODEL_R1,
        }
    },
    ProviderPriority.OPENROUTER: {
        'API_KEY': DS_OPENROUTER_API_KEY,
        'API_URL': DS_OPENROUTER_API_URL,
        'MODEL': {
            'V3': DS_OPENROUTER_MODEL_V3,
            'R1': DS_OPENROUTER_MODEL_R1,
        }
    },
    ProviderPriority.DEEPSEEK_OFFICIAL: {
        'API_KEY': DS_OFFICIAL_API_KEY,
        'API_URL': DS_OFFICIAL_API_URL,
        'MODEL': {
            'V3': DS_OFFICIAL_MODEL_V3,
            'R1': DS_OFFICIAL_MODEL_R1,
        }
    }
}

CLIENT_TYPE_OPENAI = 0
CLIENT_TYPE_HTTPX = 1

proxy_client = httpx.AsyncClient(
    proxies="http://127.0.0.1:8022",  # 替换为你的代理地址
    timeout=60  # 设置超时时间
)


class AsyncDeepSeekClient:
    def __init__(self,
                 api_infos: Dict = API_INFOs,
                 timeout: int = 60,
                 max_retries: int = 1,
                 client_type: int = CLIENT_TYPE_OPENAI):
        """
        初始化异步DeepSeek客户端
        :param api_infos: 包含不同供应商API密钥和URL的字典
        :param timeout: 请求超时时间（秒）
        :param max_retries: 最大重试次数
        :param client_type: 客户端类型0--AsyncOpenAI 1--http请求类型
        """
        self.api_infos = api_infos
        self.timeout = timeout
        self.max_retries = max_retries
        self.provider_order = sorted(ProviderPriority, key=lambda x: x.value, reverse=False)

        self.client_type = client_type
        if client_type == CLIENT_TYPE_OPENAI:
            self.client = AsyncOpenAI(timeout=timeout)
        else:
            self.client = httpx.AsyncClient(timeout=timeout)

    async def chat_completion(self,
                              messages: List[Dict[str, str]],
                              model: str = "V3",
                              stream: bool = False,
                              temperature: float = temperature,
                              max_tokens: int = max_tokens,
                              top_p: float = top_p,
                              presence_penalty: float = presence_penalty) -> Dict:
        """
        异步统一聊天补全接口
        :param messages: 消息历史列表
        :param model: 使用的模型名称
        :param stream: 是否使用流式输出
        :param temperature: 温度参数
        :param max_tokens: 最大生成token数
        :param top_p: 过滤掉低于阈值的 token 确保结果不散漫
        :param presence_penalty: [-2,2]之间，该值越大则更倾向于产生不同的内容
        :return: 标准化响应格式
        """
        logger.info(f"调用deepseek模型传入的消息列表:{messages}")
        for provider in self.provider_order:
            if provider not in self.api_infos:
                continue

            for attempt in range(self.max_retries):
                try:
                    if provider == ProviderPriority.DMXAPI:
                        response = await self._dmxapi_request(
                            messages, model, stream, temperature, max_tokens, top_p, presence_penalty)
                    elif provider == ProviderPriority.OPENROUTER:
                        response = await self._openrouter_request(
                            messages, model, stream, temperature, max_tokens, top_p, presence_penalty)
                    elif provider == ProviderPriority.DEEPSEEK_OFFICIAL:
                        response = await self._deepseek_official_request(
                            messages, model, stream, temperature, max_tokens, top_p, presence_penalty)

                    return self._format_text_response(response)

                except Exception as e:
                    err_message = f"调用{provider.name}出现异常，当前第 {attempt}次尝试：{str(e)}"
                    if attempt == self.max_retries - 1:
                        logger.error(f"All retries exhausted for {provider.name}")
                        continue
        err_message = f"调用deepseek_utils出现异常，所有尝试失败"
        logger.error(err_message)
        logger.error(traceback.format_exc())
        await send_notice_message('deepseek_util.py', 'chat_completion', 0, err_message, 3)
        raise Exception(err_message)

    async def _dmxapi_request(self, messages, model, stream, temperature, max_tokens, top_p, presence_penalty):
        """DMXAPI异步请求实现"""
        logger.info(f'正在使用{ProviderPriority.DMXAPI.name}')
        final_model = self.api_infos[ProviderPriority.DMXAPI]['MODEL'][model]
        if self.client_type == CLIENT_TYPE_OPENAI:
            self.client.base_url = self.api_infos[ProviderPriority.DMXAPI]['API_URL']
            self.client.api_key = self.api_infos[ProviderPriority.DMXAPI]['API_KEY']
            response = await asyncio.wait_for(
                self.client.chat.completions.create(
                    model=final_model,
                    messages=messages,
                    temperature=temperature,  # 值在[0,1]之间，越大表示回复越具有不确定性
                    max_tokens=max_tokens,  # 输出的最大 token 数
                    top_p=top_p,  # 过滤掉低于阈值的 token 确保结果不散漫
                    presence_penalty=presence_penalty,  # [-2,2]之间，该值越大则更倾向于产生不同的内容
                    stream=stream
                ),
                timeout=self.client.timeout
            )
            return response
        else:
            url = f"{self.api_infos[ProviderPriority.DMXAPI]['API_URL']}/chat/completions"
            headers = {
                'Accept': 'application/json',
                'Authorization': self.api_infos[ProviderPriority.DMXAPI]['API_KEY'],  # 这里放你的 DMXapi key
                'User-Agent': 'DMXAPI/1.0.0 (https://www.dmxapi.com)',
                'Content-Type': 'application/json'
            }
            payload = {
                "model": final_model,
                "messages": messages,
                "temperature": temperature,
                "max_tokens": max_tokens,
                "top_p": top_p,
                "presence_penalty": presence_penalty,
                "stream": stream
            }
            response = await self.client.post(url, headers=headers, json=payload)
            response = response.json()
            return response

    async def _openrouter_request(self, messages, model, stream, temperature, max_tokens, top_p, presence_penalty):
        """OpenRouter异步请求实现"""
        logger.info(f'正在使用{ProviderPriority.OPENROUTER.name}')
        final_model = self.api_infos[ProviderPriority.OPENROUTER]['MODEL'][model]
        if self.client_type == CLIENT_TYPE_OPENAI:
            self.client.base_url = self.api_infos[ProviderPriority.OPENROUTER]['API_URL']
            self.client.api_key = self.api_infos[ProviderPriority.OPENROUTER]['API_KEY']
            response = await asyncio.wait_for(
                self.client.chat.completions.create(
                    model=final_model,
                    messages=messages,
                    temperature=temperature,  # 值在[0,1]之间，越大表示回复越具有不确定性
                    max_tokens=max_tokens,  # 输出的最大 token 数
                    top_p=top_p,  # 过滤掉低于阈值的 token 确保结果不散漫
                    presence_penalty=presence_penalty,  # [-2,2]之间，该值越大则更倾向于产生不同的内容
                    stream=stream
                ),
                timeout=self.client.timeout
            )
            return response
        else:
            url = f"{self.api_infos[ProviderPriority.OPENROUTER]['API_URL']}/chat/completions"
            headers = {
                "Authorization": f"Bearer {self.api_infos[ProviderPriority.OPENROUTER]['API_KEY']}",
                "Content-Type": "application/json"
            }
            payload = {
                "model": final_model,
                "messages": messages,
                "temperature": temperature,
                "max_tokens": max_tokens,
                "top_p": top_p,
                "presence_penalty": presence_penalty,
                "stream": stream
            }
            response = await self.client.post(url, headers=headers, json=payload)
            return response.json()

    async def _deepseek_official_request(self, messages, model, stream, temperature, max_tokens, top_p, presence_penalty):
        """DeepSeek官方API异步请求实现"""
        logger.info(f'正在使用{ProviderPriority.DEEPSEEK_OFFICIAL.name}')
        final_model = self.api_infos[ProviderPriority.DEEPSEEK_OFFICIAL]['MODEL'][model]
        if self.client_type == CLIENT_TYPE_OPENAI:
            self.client.base_url = self.api_infos[ProviderPriority.DEEPSEEK_OFFICIAL]['API_URL']
            self.client.api_key = self.api_infos[ProviderPriority.DEEPSEEK_OFFICIAL]['API_KEY']
            response = await asyncio.wait_for(
                self.client.chat.completions.create(
                    model=final_model,
                    messages=messages,
                    temperature=temperature,  # 值在[0,1]之间，越大表示回复越具有不确定性
                    max_tokens=max_tokens,  # 输出的最大 token 数
                    top_p=top_p,  # 过滤掉低于阈值的 token 确保结果不散漫
                    presence_penalty=presence_penalty,  # [-2,2]之间，该值越大则更倾向于产生不同的内容
                    stream=stream
                ),
                timeout=self.client.timeout
            )
            return response
        else:
            url = f"{self.api_infos[ProviderPriority.DEEPSEEK_OFFICIAL]['API_URL']}/v1/chat/completions"
            headers = {
                "Authorization": f"Bearer {self.api_infos[ProviderPriority.DEEPSEEK_OFFICIAL]['API_KEY']}",
                "Content-Type": "application/json"
            }
            payload = {
                "model": final_model,
                "messages": messages,
                "temperature": temperature,
                "max_tokens": max_tokens,
                "top_p": top_p,
                "presence_penalty": presence_penalty,
                "stream": stream
            }
            response = await self.client.post(url, headers=headers, json=payload)
            return response.json()

    def _format_text_response(self, raw_response) -> str:
        """标准化响应格式（异步版本）"""
        if isinstance(raw_response, dict):
            return raw_response['choices'][0]['message']['content']
        else:
            return raw_response.choices[0].message.content

    async def close(self):
        """关闭客户端连接"""
        if self.client_type == CLIENT_TYPE_OPENAI:
            await self.client.close()
        else:
            await self.client.aclose()