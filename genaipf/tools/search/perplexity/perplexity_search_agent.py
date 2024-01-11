import json

import requests
from genaipf.conf.server import PER_PLE_URL,PER_PLE_API_KEY



async def perplexity_search(question: str):
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": "Bearer " + PER_PLE_API_KEY
    }
    # pplx-7b-chat, pplx-70b-chat, pplx-7b-online, pplx-70b-online, llama-2-70b-chat, codellama-34b-instruct, mistral-7b-instruct, and mixtral-8x7b-instruct
    model_version = "mistral-7b-instruct"
    payload = {
        "model": model_version,
        "messages": [{"role": "user", "content": question}]
    }
    response = requests.post(PER_PLE_URL, json=payload, headers=headers)
    return json.loads(response.text)['choices'][0]['message']['content']