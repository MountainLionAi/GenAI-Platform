from sanic.request import Request
from concurrent.futures import ThreadPoolExecutor
from sanic.response import json
from genaipf.interfaces.common_response import success,fail
from genaipf.services import assistant_service
from genaipf.utils.time_utils import get_format_time
import time
from datetime import datetime
import os
import asyncio
import openai
from dotenv import load_dotenv
from genaipf.conf.assistant_conf import ASSISTANT_ID_MAPPING
from openai import BadRequestError

load_dotenv(override=True)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ASSISTANT_ACCESSTOKEN_TOTAL_STRING = os.getenv("ASSISTANT_ACCESSTOKEN_TOTAL_STRING")
client = openai.AsyncOpenAI(api_key=OPENAI_API_KEY)

async def submit_message(assistant_id, thread, user_message):
    await client.beta.threads.messages.create(
        thread_id=thread.id, role="user", content=user_message
    )
    return await client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant_id,
    )

async def get_response(thread):
    return await client.beta.threads.messages.list(thread_id=thread.id)

async def retrieve_thread_and_run(assistant_id, thread_id, user_input):
    # thread = client.beta.threads.create()
    thread = await client.beta.threads.retrieve(thread_id)
    run = await submit_message(assistant_id, thread, user_input)
    return thread, run

async def wait_on_run(run, thread):
    cnt = 0
    while run.status == "queued" or run.status == "in_progress":
        run = await client.beta.threads.runs.retrieve(
            thread_id=thread.id,
            run_id=run.id,
        )
        await asyncio.sleep(1)
        cnt += 1
        if cnt % 10 == 0:
            print(f">>>>>[{datetime.now()}] thread.id: {thread.id}, run.status: {run.status}")
    return run

async def get_assistant_response(assistant_id, thread_id, content_l):
    content = content_l[-1]
    user_input = content["content"]
    thread1, run1 = await retrieve_thread_and_run(
        assistant_id, thread_id, user_input
    )
    run1 = await wait_on_run(run1, thread1)
    msgs = await get_response(thread1)
    res = "nothing"
    for m in msgs.data:
        if m.role == "assistant":
            res = m.content[0].text.value
            break
    return res
            

async def assistant_chat(request: Request):
    '''
    INPUT:
    outer_user_id, biz_id, source
    content: [
        {"role": "", "type": "", "format": "", "version": "", "content": ""},
        {"role": "", "type": "", "format": "", "version": "", "content": ""}
    ]
    # 参考格式 https://platform.openai.com/docs/guides/vision/quick-start
    
    MID:
    thread_id
    
    OUTPUT:
    {"type": "", "format": "", "version": "", "content": ""}
    '''
    # 解析请求体中的JSON数据
    print(f">>>>> assistant api request in")
    try:
        request_params = request.json
        outer_user_id = request_params.get("outer_user_id", "")
        biz_id = request_params.get("biz_id", "")
        source = request_params.get("source", "")
        content_l = request_params.get("content", [])
        access_token = request_params.get("access_token", "")
        if len(access_token) < 20 or access_token not in ASSISTANT_ACCESSTOKEN_TOTAL_STRING:
            return fail(code=5001)

        assistant_name = f'{biz_id}_____{source}'
        if assistant_name in ASSISTANT_ID_MAPPING:
            assistant_id = ASSISTANT_ID_MAPPING[assistant_name]
        else:
            assistant_id = ASSISTANT_ID_MAPPING["default"]

        # 业务逻辑code
        user_l = await assistant_service.get_assistant_user_info_from_db(outer_user_id, biz_id, source)
        if len(user_l) == 0:
            thread = await client.beta.threads.create()
            thread_id = thread.id
            user_info = (
                outer_user_id,
                biz_id,
                source,
                thread_id,
                get_format_time()
            )
            await assistant_service.add_assistant_user(user_info)
        else:
            user = user_l[0]
            thread_id = user["thread_id"]
        res = await get_assistant_response(assistant_id, thread_id, content_l)
        print(f">>>>> request_params: {request_params}\n>>>>> res: {res}")
        # 构造输出JSON响应
        response_data = [{
            "role": "assistant",
            "type": "text",
            "format": "text",
            "version": "v001",
            "content": res
        }]
    except BadRequestError as e:
        print(type(e), e)
        if "while a run" in e.message:
            return fail(code=1001, message=f"{outer_user_id} of {source} Cant add message while a run is active")
        else:
            return fail(code=1001, message=f"{outer_user_id} of {source} openai BadRequestError")
    except Exception as e:
        print(type(e), e)
        return fail(code=1001)

    return success(response_data)

async def get_user_history(request: Request):
    # 解析请求体中的JSON数据
    request_params = request.json
    outer_user_id = request_params.get("outer_user_id", "")
    biz_id = request_params.get("biz_id", "")
    source = request_params.get("source", "")
    num_limit = request_params.get("num_limit", 10)
    access_token = request_params.get("access_token", "")
    if len(access_token) < 20 or access_token not in ASSISTANT_ACCESSTOKEN_TOTAL_STRING:
        return fail(code=5001)

    # 业务逻辑code
    user_l = await assistant_service.get_assistant_user_info_from_db(outer_user_id, biz_id, source)
    
    if len(user_l) == 0:
        return success([])

    thread_id = user_l[0]["thread_id"]
    history = await client.beta.threads.messages.list(thread_id=thread_id)

    message_values = [{
        "role": msg.role,
        "content": msg.content[0].text.value
    } for msg in history.data if msg.content]
    message_values = message_values[:num_limit][::-1]
    for i in range(len(message_values)):
        message_values[i].update({
            "type": "text",
            "format": "text",
            "version": "v001",
        })
    # 构造输出JSON响应
    response_data = message_values
    to_show_m = "\n".join([m['role'] + ': ' + m["content"][:20] + "..." for m in message_values])
    print(f">>>>> history: {to_show_m}")
    return success(response_data)