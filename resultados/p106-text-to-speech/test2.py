import pyttsx3

#
#
#
# 62.       return Voice(attr['VoiceIdentifier'], attr['VoiceName'],
# 63.                    [lang], attr['VoiceGender'],
# 64. <<<                attr['VoiceAge'])
# 64. >>>                None)
#

# Crear un objeto de la clase TextToSpeech
engine = pyttsx3.init()

# Mostrar todas las voces disponibles
voices = engine.getProperty('voices')

for voice in voices:
    print("Voz:", voice.id)
    print(" - Nombre:", voice.name)
    print(" - Idioma:", voice.languages)
    print(" - Género:", voice.gender)
    print("")

print("=" * 80)

es_voices = []

for voice in voices:
    lang, country = tuple(voice.languages[0].split("_"))

    if not lang == "es":
        continue

    es_voices.append((voice.id, voice.name, voice.gender))

    print("Voz:", voice.id)
    print(" - Nombre:", voice.name)
    print(" - Idioma:", voice.languages)
    print(" - Género:", voice.gender)
    print("")

texto = "Hola, esta es una prueba de audio narrada por {} del género {}. Espero que te agrade mi voz"

engine = pyttsx3.Engine()

for id, name, gender in es_voices:
    print("NARRANDO:", id)
    print(texto.format(name, gender))
    engine.setProperty('voice', id)
    engine.setProperty('rate', 150)
    engine.say(texto.format(name, gender))

engine.runAndWait()