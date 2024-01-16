from genaipf.conf.server import os
import speech_utils
from openai import OpenAI


client = OpenAI()
with open("speech.wav", "rb") as audio_file:
    text = speech_utils.transcribe(client=client, file=audio_file)
    print(text)
    speech_utils.textToSpeech(client=client, text=text)
