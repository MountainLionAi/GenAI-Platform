

import subprocess
import base64
import hashlib
from genaipf.conf.server import os
import datetime
from dotenv import load_dotenv
from pathlib import Path
import genaipf
import google.generativeai as genai
from google.generativeai import caching
import datetime
import time
import httpx
from genaipf.utils.common_utils import sync_to_async, aget_multi_coro
_genaipf_dir = Path(genaipf.__path__[0]).parent
user_upload_files_cache_dir = Path(_genaipf_dir, ".cache/temp_user_upload_files")
user_pdf_files_cache_dir = Path(_genaipf_dir, ".cache/temp_user_pdf_files")

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")


file_redis_ttl_s = 45 * 60 * 60
cache_redis_ttl_s = 50 * 60
gemini_pdf_prefix = "gemini_pdf_____"
gemini_file_prefix = "gemini_file_____"
gemini_cache_prefix = "gemini_cache_____"

def simple_hash(base64_str: str):
    return hashlib.md5(base64_str.encode('utf-8')).hexdigest()

def upload_base64_mime_file(base64_str, filename):
    # Ensure cache directory exists
    cache_dir = user_upload_files_cache_dir
    os.makedirs(cache_dir, exist_ok=True)
    
    # Decode the base64 string
    mime_file_data = base64.b64decode(base64_str)
    
    # Generate a hash for the base64 string
    file_hash = simple_hash(base64_str)
    
    # Generate a unique filename
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    unique_filename = f"{timestamp}-{file_hash}-{filename}"
    file_path = os.path.join(cache_dir, unique_filename)
    
    # Write the decoded video data to the file
    with open(file_path, 'wb') as temp_file:
        temp_file.write(mime_file_data)
    
    # Upload the video file using the Files API
    mime_file = genai.upload_file(path=file_path)
    while mime_file.state.name == 'PROCESSING':
        mime_file = genai.get_file(mime_file.name)
        print(f'Waiting for mime_file {unique_filename} : {mime_file.name} to be processed.')
        time.sleep(2)

    # Optionally: clean up by deleting the temporary file if it's no longer needed
    # os.remove(file_path)
    
    return mime_file, unique_filename
async_upload_base64_mime_file = sync_to_async(upload_base64_mime_file)
async_genai_get_file = sync_to_async(genai.get_file)
async_caching_CachedContent_get = sync_to_async(caching.CachedContent.get)
async_caching_CachedContent_create = sync_to_async(caching.CachedContent.create)
async_genai_upload_file = sync_to_async(genai.upload_file)

# file ttl: 48hours https://ai.google.dev/gemini-api/docs/prompting_with_media?lang=python
# one file up to 2G, total files up to 20G
# cache ttl: 1hour https://ai.google.dev/gemini-api/docs/caching?lang=python

from genaipf.utils.redis_utils import x_get, x_set, x_is_key_in, x_delete
async def async_get_mime_file(f_hash, base64_str, filename):
    gfile_hash = f'{gemini_file_prefix}{f_hash}'
    is_in = await x_is_key_in(gfile_hash)
    if is_in:
        mime_file_name = await x_get(gfile_hash)
        mime_file = await async_genai_get_file(mime_file_name)
        print(f'async_get_mime_file hit: {filename} : {mime_file_name} in redis')
        return mime_file
    else:
        mime_file, unique_filename = await async_upload_base64_mime_file(base64_str, filename)
        mime_file_name = mime_file.name
        await x_set(gfile_hash, mime_file_name, ttl=file_redis_ttl_s)
        print(f'async_get_mime_file miss: {filename} not in redis, make {mime_file_name}')
        return mime_file

async def async_get_mime_files_cache(b64s_and_fname_l):
    '''
    b64s_and_fname_l = [
        {"base64": "AAA", "filename": "bitcoin.pdf"},
        {"base64": "BBB", "filename": "gold.pdf"},
    ]
    '''
    d_l = list()
    for d in b64s_and_fname_l:
        b64s = d["base64"]
        filename = d["filename"]
        f_h = simple_hash(b64s)
        mime_file = await async_get_mime_file(f_h, b64s, filename)
        d_l.append({"name": mime_file.name, "mime_file": mime_file, "filename": filename})
    d_l = sorted(d_l, key=lambda x: x["name"])
    filename_l = [x["filename"] for x in d_l]
    c_hash = "_".join([x["name"] for x in d_l])
    gcache_hash = f"{gemini_cache_prefix}{c_hash}"
    is_in = await x_is_key_in(gcache_hash)
    if is_in:
        cache_name = await x_get(gcache_hash)
        cache = await async_caching_CachedContent_get(cache_name)
        print(f'async_get_mime_files_cache hit: {filename_l} -> cache {cache_name} in redis')
        return cache
    else:
        mime_file_l = [x["mime_file"] for x in d_l]
        # Create a cache with a N minute TTL
        cache = await async_caching_CachedContent_create(
            model='models/gemini-2.5-flash-001',
            display_name=gcache_hash, # used to identify the cache
            system_instruction=(
                'You are an expert pdf analyzer, and your job is to answer '
                'the user\'s query based on the pdf file you have access to.'
            ),
            contents=[mime_file_l],
            ttl=datetime.timedelta(minutes=60), # default is also 1 hour
        )
        await x_set(gcache_hash, cache.name, ttl=cache_redis_ttl_s)
        print(f'async_get_mime_files_cache miss: {filename_l} not in redis -> make cache {cache_name}')
        return cache

# https://github.com/google-gemini/cookbook/blob/main/quickstarts/PDF_Files.ipynb
# mkdir output
# pdftoppm bitcoin.pdf -f 1 -l 9 output/images -jpeg
# pdftoppm bitcoin.pdf output/images -jpeg


def run_pdftoppm(file_path, out_dir, first, last):
    # Command to run `pdftoppm` as a single string
    # command = f"pdftoppm {file_path}  -f {first} -l {last}  output/images -jpeg"
    # -> output/images-1.jpg
    os.makedirs(out_dir, exist_ok=True)
    command = f"pdftoppm {file_path} -f {first} -l {last} {out_dir}/images -jpeg"
    
    try:
        # Run the command using shell=True
        result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Check if process returned zero exit status
        if result.returncode == 0:
            print("pdftoppm succeeded")
            return True
        else:
            print("pdftoppm failed with return code", result.returncode)
            return False
    except subprocess.CalledProcessError as e:
        # Catch any errors that occur during the execution of the command
        print(f"pdftoppm failed with error: {e}")
        print(f"pdftoppm Standard Error output: {e.stderr.decode()}")
        return False
async_run_pdftoppm = sync_to_async(run_pdftoppm)

def run_pdftotext(file_path, out_dir, page_number):
    # Command to run `pdftotext` as a single string
    # command = f"pdftotext {file_path} {out_dir}"
    # -> output/text-1.jpg
    os.makedirs(out_dir, exist_ok=True)
    command = f"pdftotext {file_path} -f {page_number} -l {page_number} {out_dir}/text-{page_number}.txt"
    
    try:
        # Run the command using shell=True
        result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Check if process returned zero exit status
        if result.returncode == 0:
            # print("pdftotext succeeded")
            return True
        else:
            print("pdftotext failed with return code", result.returncode)
            return False
    except subprocess.CalledProcessError as e:
        # Catch any errors that occur during the execution of the command
        print(f"pdftotext failed with error: {e}")
        print(f"pdftotext Standard Error output: {e.stderr.decode()}")
        return False
async_run_pdftotext = sync_to_async(run_pdftotext)


def get_pdf_page_count(file_path):
    # Command to run pdfinfo
    command = f"pdfinfo {file_path}"
    
    try:
        # Run the command using shell=True
        result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Standard output is captured
        output = result.stdout.decode()

        # Search for "Pages" in the output and parse the value
        for line in output.splitlines():
            if line.startswith("Pages:"):
                page_count = int(line.split(":")[1].strip())
                return page_count
        
        # If no "Pages" line is found
        print("Unable to find page count in pdfinfo output")
        return -1
        
    except subprocess.CalledProcessError as e:
        # Catch any errors that occur during the execution of the command
        print(f"pdfinfo failed with error: {e}")
        print(f"pdfinfo Standard Error output: {e.stderr.decode()}")
        return -1
async_get_pdf_page_count = sync_to_async(get_pdf_page_count)

# file_path = "/home/ubuntu/users/ray/GenAI-Platform/.cache/temp_user_upload_files/20240721082056-5105b68f8f7b8bc05969ec57ff55157c-bitcoin.pdf"

# n = await async_get_pdf_page_count(file_path)
# out_dir_images = "/home/ubuntu/users/ray/GenAI-Platform/.cache/temp_user_upload_files/20240721082056-5105b68f8f7b8bc05969ec57ff55157c-bitcoin-images"
# x = await async_run_pdftoppm(file_path, out_dir_images, 1, n)

# out_dir_text = "/home/ubuntu/users/ray/GenAI-Platform/.cache/temp_user_upload_files/20240721082056-5105b68f8f7b8bc05969ec57ff55157c-bitcoin-text"
# x = await async_run_pdftotext(file_path, out_dir, 9)


def sort_file_by_suffix(spliter, suffix):
    ...

async def async_process_pdf(file_path, out_dir_images, out_dir_text, first_page, last_page):
    print(f'async_process_pdf doing: async_run_pdftoppm {file_path}')
    await async_run_pdftoppm(file_path, out_dir_images, first_page, last_page)
    print(f'async_process_pdf doing: async_run_pdftotext {file_path}')
    for page in range(first_page, last_page+1):
        await async_run_pdftotext(file_path, out_dir_text, page)

    image_files = [str(x) for x in list(Path(out_dir_images).glob('images-*.jpg'))]
    
    img_d_l = []
    for i, s in enumerate(image_files):
        seq = int(s.split("-")[-1].strip(".jpg"))
        img_d_l.append({"seq": seq, "file": s})
    img_d_l = sorted(img_d_l, key=lambda x: x["seq"])
    image_files = [x["file"] for x in img_d_l]
    text_files = [str(Path(out_dir_text) / f"text-{page}.txt") for page in range(first_page, last_page+1)]
    txt_d_l = []
    for i, s in enumerate(text_files):
        seq = int(s.split("-")[-1].strip(".txt"))
        txt_d_l.append({"seq": seq, "file": s})
    txt_d_l = sorted(txt_d_l, key=lambda x: x["seq"])
    text_files = [x["file"] for x in txt_d_l]
    
    files = []
    # # image_files_ll = [[x] for x in image_files]
    # # args_l, i_m_files = await aget_multi_coro(async_genai_upload_file, image_files_ll, batch_size=2)
    # print(f'async_process_pdf doing: async_genai_upload_file {file_path}')
    # import tqdm
    # for img in tqdm(image_files):
    #     m_f = await async_genai_upload_file(img)
    #     files.append(m_f)
    img_mime_files = files
    return img_mime_files, image_files, text_files


async def async_process_pdf_b64s(pdf_hash, base64_str, filename):
    "pdf_hash = simple_hash(base64_str)"
    redis_hash = f"{gemini_pdf_prefix}{pdf_hash}"
    local_filename = f'{pdf_hash[-10:]}.pdf'
    is_in = await x_is_key_in(redis_hash)
    if is_in:
        pdf_mime_info = await x_get(redis_hash)
        pdf_mime_info["filename"] = filename
        pdf_mime_info["local_filename"] = local_filename
        pdf_mime_info["redis_hash"] = redis_hash
        print(f'async_process_pdf_b64s hit: {filename} : {redis_hash} in redis')
        return pdf_mime_info
    # await x_delete(redis_hash)
    cache_dir = user_pdf_files_cache_dir
    os.makedirs(cache_dir, exist_ok=True)
    mime_file_data = base64.b64decode(base64_str)
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    unique_filename = f"{timestamp}-{pdf_hash}-{local_filename}"
    file_path = os.path.join(cache_dir, unique_filename)
    with open(file_path, 'wb') as temp_file:
        temp_file.write(mime_file_data)
    out_dir_images = file_path + "-images"
    out_dir_text = file_path + "-text"
    N_pages = await async_get_pdf_page_count(file_path)
    first_page, last_page = 1, N_pages
    os.makedirs(out_dir_images, exist_ok=True)
    os.makedirs(out_dir_text, exist_ok=True)
    img_mime_files, image_files, text_files = await async_process_pdf(file_path, out_dir_images, out_dir_text, first_page, last_page)
    pdf_mime_info = {
        "pdf_hash": pdf_hash,
        "redis_hash": redis_hash,
        "filename": filename,
        "local_filename": local_filename,
        "out_dir_images": out_dir_images,
        "out_dir_text": out_dir_text,
        "unique_filename": unique_filename,
        "img_mime_files": img_mime_files,
        "image_files": image_files,
        "text_files": text_files,
    }
    await x_set(redis_hash, pdf_mime_info, ttl=file_redis_ttl_s)
    print(f'async_process_pdf_b64s miss: {filename} not in redis, make {redis_hash}, unique_filename {unique_filename}')
    return pdf_mime_info
    
def pdf_mime_info_to_parts_for_gemini(pdf_mime_info):
    texts = [Path(x).read_text() for x in pdf_mime_info["text_files"]]
    files = pdf_mime_info["image_files"]
    textbook = []
    first = 1 # from page 1 to end
    for page, (text, image) in enumerate(zip(texts, files)):
        textbook.append(genai.protos.Part(text=f'## Page {first+page} ##'))
        textbook.append(genai.protos.Part(text=text))
        textbook.append(genai.protos.Part(
            inline_data=genai.protos.Blob(
                mime_type='image/jpeg',
                data=Path(image).read_bytes()
            )
        ))
    return textbook


async def async_make_gemini_contents_from_ml_messages(messages):
    """_summary_

    Args:
        messages (list): _description_
            [
                {"role": "user", "content": "what is it", "base64content": "<base64>", "type": "image", "version": "v001"},
                {"role": "assistant", "content": "it is an apple"},
                {"role": "user", "content": "what color?", "type": "text", "version": "v001"},
                {"role": "assistant", "content": "red"},
                {"role": "user", "content": "summarize this file", "type": "pdf", "version": "v001", "extra_content": {"base64": "<base64 str>", "filename": "paper.pdf"}},
            ]
        use_model (str): _description_
            "gemini-2.5-flash"
    Outputs:
        [
            Content(role="user", parts=[Part.from_image?(img_mime_file), Part.from_text("it is an apple")]),
            Content(role="model", parts=[Part.from_text("it is an apple")]),
            Content(role="user", parts=[Part.from_text("Ned likes watching movies.")]),
            Content(role="model", parts=[Part.from_text("red")]),
            Content(role="user", parts=[textbook] + [Part.from_text("summarize this file")]),
        ]
    
    there is no system message which is made when genai.GenerativeModel
    """
    out_msgs = []
    for x in messages:
        if x["role"] == "assistant":
            role = "model"
        else:
            role = x["role"]
        if x.get("type") == "image":
            # b64s = x.get('base64content').split("base64,")[-1]
            # text = x.get("content", "")
            # out_msgs.append(
            #     genai.protos.Content(
            #         role=role,
            #         parts=[
            #             genai.protos.Part(
            #                 inline_data=genai.protos.Blob(
            #                     # mime_type='image/jpeg',
            #                     # data=pathlib.Path('image.jpg').read_bytes()
            #                     mime_type='image/png',
            #                     data=base64.b64decode(b64s)
            #                 )
            #             ), 
            #             genai.protos.Part(text=text)
            #         ]
            #     )
            # )
            parts = []
            for image_url in x.get('base64content'):
                image = httpx.get(image_url)
                part = genai.protos.Part(
                    inline_data=genai.protos.Blob(
                        mime_type='image/png',
                        data=base64.b64encode(image.content).decode('utf-8')
                    )
                )
                parts.append(part)
            parts.append(genai.protos.Part(text=text))
            out_msgs.append(
                genai.protos.Content(
                    role=role,
                    parts=parts
                )
            )
        elif x.get("type") == "pdf":
            b64s = x["extra_content"]["base64"]
            filename = x["extra_content"]["filename"]
            text = x.get("content", "")
            pdf_hash = simple_hash(b64s)
            pdf_mime_info = await async_process_pdf_b64s(pdf_hash, b64s, filename)
            textbook = pdf_mime_info_to_parts_for_gemini(pdf_mime_info)
            out_msgs.append(
                genai.protos.Content(
                    role=role,
                    parts=textbook + [genai.protos.Part(text=text)]
                )
            )
        else:
            text = x.get("content", "")
            out_msgs.append(
                genai.protos.Content(
                    role=role,
                    parts=[genai.protos.Part(text=text)]
                )
            )
    return out_msgs


async def async_get_gemini_chat_stream(gemini_contents, system_message):
    model = genai.GenerativeModel(model_name='gemini-2.5-flash', system_instruction=system_message)
    chat = model.start_chat(history=gemini_contents[:-1])
    response = await chat.send_message_async(gemini_contents[-1], stream=True)
    async for chunk in response:
        yield chunk.text

    
async def async_wrap_string_generator(str_generator, output_type=""):
    from genaipf.dispatcher.api import get_format_output, textToSpeech
    resp = str_generator
    yield get_format_output("step", "llm_yielding")
    _tmp_text = ""
    _tmp_voice_text = ""
    async for chunk in resp:
        _gpt_letter = chunk
        if _gpt_letter:
            _tmp_text += _gpt_letter
            _tmp_voice_text += _gpt_letter
            if output_type != 'voice':
                yield get_format_output("gpt", _gpt_letter)
        if output_type == 'voice': 
            if len(_tmp_voice_text) >= 200:
                base64_encoded_voice = textToSpeech(_tmp_voice_text)
                yield get_format_output("tts", base64_encoded_voice, "voice_mp3_v001")
                for c in _tmp_voice_text:
                    yield get_format_output("gpt", c)
                _tmp_voice_text = ""
    if output_type == 'voice': 
        base64_encoded_voice = textToSpeech(_tmp_voice_text)
        yield get_format_output("tts", base64_encoded_voice, "voice_mp3_v001")
        for c in _tmp_voice_text:
            yield get_format_output("gpt", c)
    yield get_format_output("inner_____gpt_whole_text", _tmp_text)






'''
b1 = "/home/ubuntu/users/ray/GenAI-Platform/.cache/bitcoin_base64.txt"
with open(b1, "r") as f:
    base64_str = f.read()
filename = "bitcoin.pdf"
m, u = await async_upload_base64_mime_file(base64_str, filename)
b64s_and_fname_l = [{"base64": base64_str, "filename": filename}]


b1 = "/home/ubuntu/users/ray/GenAI-Platform/.cache/bitcoin_base64.txt"
filename = "bitcoin.pdf"
# b1 = "/home/ubuntu/users/ray/GenAI-Platform/.cache/paper_base64.txt"
# filename = "paper.pdf"
with open(b1, "r") as f:
    base64_str = f.read()
pdf_hash = simple_hash(base64_str)
pdf_mime_info = await async_process_pdf_b64s(pdf_hash, base64_str, filename)


model = genai.GenerativeModel(model_name='gemini-2.5-flash', system_instruction=None)

textbook = make_content_for_gemini(pdf_mime_info)

response = model.generate_content(
    [f'# pdf: {pdf_mime_info["filename"]}']+
    textbook +
    ["[END]\n\n总结一下关键章节"]
)
x = response.parts[0]
x.text

pdf_mime_info["redis_hash"]


chat = model.start_chat(history=[])

















b1 = "/home/ubuntu/users/ray/GenAI-Platform/.cache/bitcoin_base64.txt"
filename = "bitcoin.pdf"
# b1 = "/home/ubuntu/users/ray/GenAI-Platform/.cache/paper_base64.txt"
# filename = "paper.pdf"
with open(b1, "r") as f:
    base64_str = f.read()
# pdf_hash = simple_hash(base64_str)
# pdf_mime_info = await async_process_pdf_b64s(pdf_hash, base64_str, filename)
# textbook = pdf_mime_info_to_parts_for_gemini(pdf_mime_info)


messages = [
    # {"role": "user", "content": "what is it", "base64content": "<base64>", "type": "image", "version": "v001"},
    # {"role": "assistant", "content": "it is an apple"},
    # {"role": "user", "content": "what color?", "type": "text", "version": "v001"},
    # {"role": "assistant", "content": "red"},
    {"role": "user", "content": "summarize this file", "type": "pdf", "version": "v001", "extra_content": {"base64": base64_str, "filename": filename}},
]



gemini_contents = await async_make_gemini_contents_from_ml_messages(messages)

model = genai.GenerativeModel(model_name='gemini-2.5-flash', system_instruction="you can say up to 10 words")

# chat = model.start_chat(history=gemini_contents)

chat = model.start_chat(history=[])
response = chat.send_message(gemini_contents[-1])

chat = model.start_chat(history=[])
response = chat.send_message(gemini_contents[-1])

chat = model.start_chat(history=gemini_contents)
response = await chat.send_message_async(gemini_contents[-1], stream=True)
async for chunk in response:
    # print(chunk.text)
    print(chunk)
    print("_"*80)

    
g1 = async_get_gemini_chat_stream(gemini_contents, "you can say up to 20 words")
g2 = async_wrap_string_generator(g1)
async for x in g2:
    print(x)
'''
