import pdfkit
from flask import Flask, render_template, request, redirect, url_for, Response, send_from_directory

import json
import requests
import time

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

@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory('static', filename)

def generar_imagen_descriptiva(texto_descriptivo):
    # Llama al API de Imagen de OpenAI para generar una imagen
    response = openai.Image.create(
        model="image-alpha-001",  # Utiliza el modelo adecuado
        prompt=texto_descriptivo,
        n=1,  # Puedes ajustar este valor según tus necesidades
        size="256x256",  # Tamaño de la imagen generada
    )

    # Guardar la imagen localmente
    imagen_url = response.data[0].url
    timestamp = int(time.time())
    imagen_nombre = f"imagen_descriptiva_{timestamp}.jpg"
    try:
        response = requests.get(imagen_url)
        response.raise_for_status()  # Lanzar una excepción si hay un error HTTP
        with open(f"static/{imagen_nombre}", 'wb') as imagen_file:
            imagen_file.write(response.content)
    except requests.exceptions.RequestException as e:
        # Manejar el error de descarga de la imagen (puedes registrar el error si es necesario)
        print(f"Error al descargar la imagen descriptiva: {e}")

    # Devolver la ruta relativa de la imagen
    return f"/static/{imagen_nombre}"

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

@app.route('/descargar_pdf')
def descargar_pdf():
    # Cargar noticias desde un archivo JSON (supongamos que se llama noticias.json)
    with open('noticias.json', 'r', encoding='utf-8') as json_file:
        noticias = json.load(json_file)

    contenido_html = '<html><head><meta charset="UTF-8"><title>Noticias</title></head><body>'
    
    for noticia in noticias:
        contenido_html += f"<h2>{noticia['titulo']}</h2>"

        # Utilizar la URL de la imagen proporcionada en la noticia
        imagen_url = noticia.get('imagen_url', '')  # Obtener la URL de la imagen de la noticia
        if imagen_url:
            contenido_html += f"<img src='{imagen_url}' alt='Imagen noticia'>"
        
        contenido_html += f"<p>Resumen: {noticia['resumen']}</p>"
        contenido_html += f"<p>Puntos Principales: {noticia['puntos_principales']}</p>"
        contenido_html += f"<p>{noticia['contenido']}</p>"
    
    contenido_html += '</body></html>'
    
    # Guardar el contenido HTML como noticias.html
    with open('noticias.html', 'w', encoding='utf-8') as html_file:
        html_file.write(contenido_html)
    
    # Crear el archivo PDF a partir del contenido HTML
    pdfkit.from_file('noticias.html', 'noticias.pdf')

    # Abrir el archivo PDF y devolverlo como respuesta para descargar
    with open('noticias.pdf', 'rb') as pdf_file:
        pdf_content = pdf_file.read()
    
    response = Response(pdf_content, content_type='application/pdf')
    response.headers['Content-Disposition'] = 'inline; filename=noticias.pdf'
    
    return response

if __name__ == '__main__':
    app.run(debug=True)