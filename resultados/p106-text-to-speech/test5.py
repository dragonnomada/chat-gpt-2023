# python3 -m pip install pytube
from pytube import YouTube

url = "https://www.youtube.com/watch?v=SqB4FSettTI"

yt = YouTube(url)

stream = yt.streams.filter(only_audio=True, file_extension="mp4").first()

output_audio = stream.download()

print(output_audio)

# python3 -m pip install openai
import openai

openai.api_key = 'TU_API_KEY'

transcript = openai.Audio.transcribe("whisper-1", open(output_audio, "rb"))

print(transcript.text)

response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "Eres un asistente que genera síntesis de textos"},
        {"role": "user", "content": f"Resume el siguiente texto:\n\n{transcript.text}"},
    ]
)

texto = response.choices[0].message['content']

print(texto)

# python3 -m pip install pyttsx3
import pyttsx3

engine = pyttsx3.init()

engine.say(texto)

engine.runAndWait()
