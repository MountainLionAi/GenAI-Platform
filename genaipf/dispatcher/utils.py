import os
import typing
import openai
import tqdm
import pandas as pd
from functools import cache
from qdrant_client import QdrantClient
from qdrant_client.http import models
from dotenv import load_dotenv
import tiktoken

load_dotenv(override=True)

openai.api_key = os.getenv("OPENAI_API_KEY")
MAX_CH_LENGTH_GPT3 = 8000
MAX_CH_LENGTH_GPT4 = 3000
MAX_CH_LENGTH_QA_GPT3 = 3000
MAX_CH_LENGTH_QA_GPT4 = 1500
qdrant_url = "http://localhost:6333"

from genaipf.conf.server import PLUGIN_NAME
vdb_prefix = PLUGIN_NAME

qa_coll_name = f"{vdb_prefix}_filtered_qa"
gpt_func_coll_name = f"{vdb_prefix}_gpt_func"

client = QdrantClient(qdrant_url)

@cache
def get_embedding(text, model = "text-embedding-ada-002"):
    result = openai.Embedding.create(
        model=model,
        input=text
    )
    embedding = result["data"][0]["embedding"]
    return embedding



def merge_ref_and_input_text(ref, input_text, language='en'):
    if language == 'cn':
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
    _vector = get_embedding(text)
    search_results = client.search(cname, _vector, limit=topk)
    wrapper_result = []
    for result in search_results:
        if result.score >= sim_th:
            wrapper_result.append({'payload': result.payload, 'similarity': result.score})
    return wrapper_result

def get_qa_vdb_topk(text: str, sim_th: float = 0.8, topk: int = 3) -> typing.List[typing.Mapping]:
    # results = get_vdb_topk(text, "qa", sim_th, topk)
    results = get_vdb_topk(text, qa_coll_name, sim_th, topk)
    out_l = []
    for x in results:
        v = f'{x["payload"].get("q")}: {x["payload"].get("a")}'
        out_l.append(v)
    return out_l

def merge_ref_and_qa(picked_content, related_qa, language="en", model=''):
    _ref_text = "\n\n".join(str(picked_content))
    _ref_text = _ref_text.replace("\n", "")
    length = MAX_CH_LENGTH_GPT3
    length_qa = MAX_CH_LENGTH_QA_GPT3
    if model == 'gpt-4':
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