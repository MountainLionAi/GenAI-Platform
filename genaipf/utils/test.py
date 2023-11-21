from dotenv import load_dotenv
import speech_utils
from openai import OpenAI

load_dotenv(dotenv_path=".env")

client = OpenAI()
with open("speech.wav", "rb") as audio_file:
    text = speech_utils.transcribe(client=client, file=audio_file)
    print(text)
    speech_utils.textToSpeech(client=client, text=text)
