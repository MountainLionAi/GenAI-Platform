from openai import OpenAI, AsyncOpenAI
import tempfile
import base64
from genaipf.conf.server import os

client = OpenAI()

# 可通过 env 升级同厂兼容版（对齐 ml_news TTS_OPENAI_MODEL）
ASR_OPENAI_MODEL = (os.getenv("ASR_OPENAI_MODEL") or "gpt-4o-mini-transcribe").strip()
TTS_OPENAI_MODEL = (os.getenv("TTS_OPENAI_MODEL") or "gpt-4o-mini-tts").strip()


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
            model=ASR_OPENAI_MODEL,
            file=audio_file
        )

    # 删除临时文件
    os.remove(tmp_file_path)
    return transcript.text

def textToSpeech(text):

    # 调用 OpenAI 的语音合成 API
    response = client.audio.speech.create(
      model=TTS_OPENAI_MODEL,
      voice="nova",
      input=text
    )

    # 创建一个字节流对象来接收音频数据
    # 获取音频数据的二进制内容
    audio_data = response.content

    # 将二进制内容转换为 Base64 编码
    base64_encoded_audio = base64.b64encode(audio_data).decode('ASCII')

    return base64_encoded_audio


async def transcribe_v2(base64_audio):
    """
    异步方法，使用 OpenAI 最新的模型将 base64 编码的音频转换为文本
    """
    async_client = AsyncOpenAI()

    # 解码 Base64 字符串以获取字节数据
    decoded_bytes = base64.b64decode(base64_audio)

    # 将解码后的字节数据保存为临时文件
    with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as tmp_file:
        tmp_file.write(decoded_bytes)
        tmp_file_path = tmp_file.name

    try:
        # 使用临时文件进行 API 调用
        with open(tmp_file_path, "rb") as audio_file:
            transcript = await async_client.audio.transcriptions.create(
                model=ASR_OPENAI_MODEL,
                file=audio_file
            )

        return transcript.text
    finally:
        # 确保临时文件被删除
        if os.path.exists(tmp_file_path):
            os.remove(tmp_file_path)
