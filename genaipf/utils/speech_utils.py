from openai import OpenAI
from pathlib import Path
import tempfile
import os
import base64
from dotenv import load_dotenv

load_dotenv(dotenv_path=".env")

client = OpenAI()

def transcribe(base64_audio):
    # 解码 Base64 字符串以获取字节数据
    decoded_bytes = base64.b64decode(base64_audio)
    # 将解码后的字节数据保存为临时文件
    with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as tmp_file:
        tmp_file.write(decoded_bytes)
        tmp_file_path = tmp_file.name

    # 使用临时文件进行 API 调用
    with open(tmp_file_path, "rb") as audio_file:
        transcript = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file
        )

    # 删除临时文件
    os.remove(tmp_file_path)
    return transcript.text

def textToSpeech(text):

    # 调用 OpenAI 的语音合成 API
    response = client.audio.speech.create(
      model="tts-1",
      voice="nova",
      input=text
    )

    # 创建一个字节流对象来接收音频数据
    # 获取音频数据的二进制内容
    audio_data = response.content

    # 将二进制内容转换为 Base64 编码
    base64_encoded_audio = base64.b64encode(audio_data).decode('ASCII')

    return base64_encoded_audio
