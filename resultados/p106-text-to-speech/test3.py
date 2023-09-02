import openai

openai.api_key = 'TU_API_KEY'

print("Generando un cuento corto")

response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "Eres un asistente que genera texto"},
        {"role": "user", "content": "Crea un cuento corto"},
    ]
)

texto = response.choices[0].message['content']

print(texto)

import pyttsx3

engine = pyttsx3.init()

print("Narrando al texto...")

engine.say(texto)

engine.runAndWait()