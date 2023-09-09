from flask import Flask, render_template, request, redirect, url_for
import json

app = Flask(__name__)

@app.route('/')
def index():
    # Carga las noticias desde el archivo JSON
    noticias = cargar_noticias()
    return render_template('index.html', noticias=noticias)

import openai

# Define tu clave de API de OpenAI
openai.api_key = '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'

def obtener_resumen_puntos_principales(contenido):
    # Llama al API de ChatGPT para obtener el resumen
    respuesta_resumen = generar_resumen(contenido)

    # Llama al API de ChatGPT para obtener los puntos principales
    respuesta_puntos_principales = generar_puntos_principales(contenido)

    # Obtén los textos de resumen y puntos principales
    resumen = respuesta_resumen['choices'][0]['message']['content'].strip()
    puntos_principales = respuesta_puntos_principales['choices'][0]['message']['content'].strip()

    return resumen, puntos_principales

def generar_resumen(contenido):
    # Llama al API de ChatGPT para que el redactor de noticias genere el resumen en HTML
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # Utiliza el modelo adecuado
        messages=[
            {"role": "system", "content": "You are a news writer."},
            {"role": "user", "content": f"Redacta un resumen en formato HTML del siguiente contenido:\n{contenido}"}
        ],
        max_tokens=150,  # Ajusta este valor según tus necesidades
        temperature=0.7,
    )

    return response

def generar_puntos_principales(contenido):
    # Llama al API de ChatGPT para que el redactor de noticias genere los puntos principales en HTML
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # Utiliza el modelo adecuado
        messages=[
            {"role": "system", "content": "You are a news writer."},
            {"role": "user", "content": f"Redacta los puntos principales en formato HTML del siguiente contenido:\n{contenido}"}
        ],
        max_tokens=150,  # Ajusta este valor según tus necesidades
        temperature=0.7,
    )

    return response

def generar_imagen_descriptiva(texto_descriptivo):
    # Llama al API de Imagen de OpenAI para generar una imagen
    response = openai.Image.create(
        model="image-alpha-001",  # Utiliza el modelo adecuado
        prompt=texto_descriptivo,
        n=1,  # Puedes ajustar este valor según tus necesidades
        size="256x256",  # Tamaño de la imagen generada
    )

    # Obtiene la URL de la imagen generada
    imagen_url = response.data[0].url

    return imagen_url


@app.route('/subir_noticia', methods=['POST'])
def subir_noticia():
    # Obtiene los datos del formulario
    titulo = request.form['titulo']
    contenido = request.form['contenido']

    # Obtiene el resumen y los puntos principales del contenido
    resumen, puntos_principales = obtener_resumen_puntos_principales(contenido)

    # Genera una imagen descriptiva utilizando DALL-E
    imagen_url = generar_imagen_descriptiva(titulo)  # Puedes usar el título como texto descriptivo

    # Crea una nueva noticia con resumen, puntos principales y la imagen
    noticia = {'titulo': titulo, 'contenido': contenido, 'resumen': resumen, 'puntos_principales': puntos_principales, 'imagen_url': imagen_url}

    # Agrega la noticia al archivo JSON
    agregar_noticia(noticia)

    return redirect(url_for('index'))

def cargar_noticias():
    try:
        with open('noticias.json', 'r') as archivo:
            noticias = json.load(archivo)
    except FileNotFoundError:
        noticias = []
    return noticias

def agregar_noticia(noticia):
    noticias = cargar_noticias()
    noticias.append(noticia)
    with open('noticias.json', 'w') as archivo:
        json.dump(noticias, archivo, indent=4)

if __name__ == '__main__':
    app.run(debug=True)