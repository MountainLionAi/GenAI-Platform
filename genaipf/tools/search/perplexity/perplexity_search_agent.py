import json
from genaipf.conf.server import PER_PLE_URL,PER_PLE_API_KEY
from genaipf.utils import http_utils


async def perplexity_search(question: str, language=None):
    client = http_utils.AsyncHttpClient()
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": "Bearer " + PER_PLE_API_KEY
    }
    # pplx-7b-chat, pplx-70b-chat, pplx-7b-online, pplx-70b-online, llama-2-70b-chat, codellama-34b-instruct, mistral-7b-instruct, and mixtral-8x7b-instruct
    model_version = "mixtral-8x7b-instruct"
    payload = {
        "model": model_version,
        "messages": [{"role": "system", "content": "Answer my questions in Chinese"}, {"role": "user", "content": question}]
    }
    if language == 'en':
        payload["messages"] = [{"role": "system", "content": "Answer my questions in English"}, {"role": "user", "content": question}]
    try:
        print('PER_PLE_URL: ', PER_PLE_URL)
        print('headers: ', headers)
        print('payload: ', payload)
        result = await client.post(PER_PLE_URL, json=payload, headers=headers)
        return json.loads(result)['choices'][0]['message']['content']
    finally:
        await client.close()