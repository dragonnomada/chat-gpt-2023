# python3 -m pip install pyttsx3
import pyttsx3

#
# <PYTHON HOME>/3.11/lib/python3.11/site-packages/pyttsx3/drivers/nsss.py" 
#
# class NSSpeechDriver(NSObject):
#     @objc.python_method
#     def initWithProxy(self, proxy):
# <<<     self = super(NSSpeechDriver, self).init()
# >>>     self = objc.super(NSSpeechDriver, self).init()
#

# Crear un objeto de la clase TextToSpeech
engine = pyttsx3.init()

# Texto que quieres convertir a audio
texto = "Hola, esto es otro ejemplo de texto convertido a audio."

# Configurar propiedades (opcional)
engine.setProperty('rate', 150)  # Velocidad de habla en palabras por minuto

# Convertir y reproducir el texto
engine.say(texto)
engine.runAndWait()