# Clase 106 - SPEECH-TO-TEXT y TEXT-TO-SPEECH

> **Centro de Investigación en Computación**
>
> *Instituto Politécnico Nacional*
>
> Departamento de Diplomados y Extensión Profesional
>

![CIC-IPN](https://www.cic.ipn.mx/images/logos/logositiocicletras.png)

**Profesor**: [Alan Badillo Salas](alan@nomadacode.com)

---

## Contenido

    .1 Servidor de Noticias - Genera un servidor de noticias que tenga un formulario para subir la noticia. Recibir la noticia y genere un HTML con el título de la noticia, un resumen de la noticia, las palabras clave de la noticia, la noticia extendida. Generar 3 imágenes relacionadas a la noticia con DALL-E. Generar un PDF con los datos de la noticia para descargarse.

    .2 Servidor de Bibliografías - Genera un servidor de bibliografías que permita cargar un CSV con el nombre del personaje histórico y tres solicitudes para armar su bibliografía (por ejemplo, el año de nacimiento y muerte, la ciudad de origen y muerte y el resumen de su vida). Generar 3 imágenes distintas de cada persona con DALL-E. Generar un HTML con los datos de la bibliografía y un PDF con los datos de la bibliografía.

    .3 Servidor para la gestión de documentos oficiales - Genera un servidor de documentos que permita cargar un archivo ZIP con documentos similares (de formato similar). Descomprime el archivo comprimido y extrae los documentos. Extrae el contenido de cada documento texto/OCR y genera un archvio de texto/CSV con los datos extraídos de cada documento. Analiza el documento extraído y separa las diferentes piezas de información en otros archivos de texto/CSV. Genera un documento PDF con las diferentes piezas extraídas para formar reportes de compendio de todos los documentos y reportes individuales de cada documento.

    .4 Servidor de Traducción - Genera un servidor que permita grabar audio del usuario. Recupera el texto y traducelo a otro lenguaje. Genera el audio narrativo del segundo audio. Genera un HTML que devuelva el audio original, el texto extraído, el texto traducido y el audio transladado.

    .5 Servidor de Presentaciones en Video - Genera un servidor que tenga un formulario para describir una presentación en partes (en diapositivas). Para cada diapositiva genera el texto resumido de la diapositiva según la solicitud, genera imágenes asociadas con DALL-E y genera un audio para la locución de la diapositiva. Ensambla todas las diapositivas en un video que se pueda ver desde el servidor.

## .1 Servidor de Noticias

Genera un servidor de noticias que tenga un formulario para subir la noticia. Recibir la noticia y genere un HTML con el título de la noticia, un resumen de la noticia, las palabras clave de la noticia, la noticia extendida. Generar 3 imágenes relacionadas a la noticia con DALL-E. Generar un PDF con los datos de la noticia para descargarse.

![1.1](<./screenshots/p107/Captura de pantalla 2023-09-08 a la(s) 13.48.55.png>)

---

¡Claro! Para crear un servidor en Python que permita subir noticias mediante un formulario y guardarlas en un archivo JSON local, puedes seguir estos pasos:

Paso 1: Configurar el entorno
Asegúrate de tener Python instalado en tu sistema. También necesitarás instalar el framework web Flask para crear el servidor web. Puedes instalar Flask utilizando pip:

```bash
pip install Flask
```

Paso 2: Crear el proyecto
Crea un directorio para tu proyecto y crea un archivo Python llamado `app.py`.

Paso 3: Configurar la aplicación Flask
En `app.py`, importa Flask y crea una instancia de la aplicación:

```python
from flask import Flask, render_template, request, redirect, url_for
import json

app = Flask(__name__)
```

Paso 4: Definir rutas y formularios
Define una ruta para la página de inicio donde se mostrarán las noticias y otra ruta para el formulario de carga de noticias:

```python
@app.route('/')
def index():
    # Carga las noticias desde el archivo JSON
    noticias = cargar_noticias()
    return render_template('index.html', noticias=noticias)

@app.route('/subir_noticia', methods=['POST'])
def subir_noticia():
    # Obtiene los datos del formulario
    titulo = request.form['titulo']
    contenido = request.form['contenido']

    # Crea una nueva noticia
    noticia = {'titulo': titulo, 'contenido': contenido}

    # Agrega la noticia al archivo JSON
    agregar_noticia(noticia)

    return redirect(url_for('index'))
```

Paso 5: Crear funciones para cargar y agregar noticias
Crea funciones para cargar las noticias desde el archivo JSON y agregar una nueva noticia al archivo:

```python
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
```

Paso 6: Crear una plantilla HTML para el formulario y las noticias
Crea una plantilla HTML (por ejemplo, `templates/index.html`) para mostrar las noticias y el formulario:

```html
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Noticias</title>
</head>
<body>
    <h1>Noticias</h1>
    <ul>
        {% for noticia in noticias %}
            <li>
                <h2>{{ noticia['titulo'] }}</h2>
                <p>{{ noticia['contenido'] }}</p>
            </li>
        {% endfor %}
    </ul>
    
    <h2>Subir Noticia</h2>
    <form method="POST" action="/subir_noticia">
        <label for="titulo">Título:</label>
        <input type="text" name="titulo" required><br>
        <label for="contenido">Contenido:</label>
        <textarea name="contenido" required></textarea><br>
        <input type="submit" value="Subir Noticia">
    </form>
</body>
</html>
```

Paso 7: Ejecutar la aplicación
Finalmente, en el archivo `app.py`, agrega el siguiente código para ejecutar la aplicación:

```python
if __name__ == '__main__':
    app.run(debug=True)
```

Ahora, puedes ejecutar tu aplicación Flask con `python app.py` y acceder a ella en un navegador web en `http://localhost:5000/`. Puedes subir noticias utilizando el formulario y se guardarán en un archivo JSON local llamado `noticias.json`.

---

### El proyecto logra el objetivo

Se logra construir el proyecto asistido por CHATGPT.

Y los resultados son los siguientes:

![1.2](<./screenshots/p107/Captura de pantalla 2023-09-09 a la(s) 10.39.37.png>)

---

Por supuesto, aquí tienes un resumen de las modificaciones y mejoras realizadas en el proyecto:

1. **Generación de Resumen y Puntos Principales:** Se modificó la función `obtener_resumen_puntos_principales` para llamar al API de ChatGPT dos veces, una para obtener el resumen y otra para los puntos principales.

2. **Generación de Imagen Descriptiva:** Se agregó una función `generar_imagen_descriptiva` para generar imágenes descriptivas utilizando el API de Imagen de OpenAI. Además, se modificó la función `generar_imagen_descriptiva` para guardar las imágenes localmente con nombres únicos.

3. **Descarga de Noticias en PDF:** Se creó una función `descargar_pdf` para descargar las noticias en formato PDF. Las noticias ahora incluyen imágenes locales y se sirven públicamente.

4. **Plantilla Mejorada:** La plantilla HTML se mejoró para que tenga un estilo similar al de New York Times. Además, se agregó un formulario para subir noticias.

5. **Descarga de Noticias en HTML:** Se agregó una función `descargar_html` para descargar las noticias en formato HTML.

6. **Visualización de Noticias:** Se creó una página para mostrar las noticias con títulos, imágenes, resúmenes, puntos principales y contenido. Los resúmenes y puntos principales ahora se muestran como HTML sin etiquetas.

7. **Gestión de Errores en Descarga de Imágenes:** Se manejaron posibles errores al descargar imágenes, y se agregó una función para mostrar imágenes de manera pública.

8. **Nombre Único para Imágenes Descriptivas:** Se generan nombres únicos para las imágenes descriptivas basados en el sello de tiempo actual.

Estas modificaciones y mejoras permiten subir noticias mediante un formulario, generar resúmenes, puntos principales e imágenes descriptivas, y luego mostrar las noticias en formato PDF y HTML con un estilo similar al del New York Times. Además, se han manejado errores de descarga de imágenes y se han garantizado nombres de archivo únicos para las imágenes descriptivas.

---

![1.3](<./screenshots/p107/Captura de pantalla 2023-09-09 a la(s) 10.39.59.png>)

Aquí tienes los códigos importantes y las instalaciones realizadas en el proyecto:

### Instalaciones necesarias:

Puedes instalar las siguientes bibliotecas de Python utilizando `pip`:

```bash
pip install openai flask requests pdfkit
```

### Código principal de la aplicación Flask:

```python
from flask import Flask, request, redirect, url_for, render_template, Response, send_from_directory
import json
import openai
import requests
import pdfkit
import time

app = Flask(__name__)

# Configura tu clave de API de OpenAI
openai.api_key = 'TU_CLAVE_DE_API_DE_OPENAI'

@app.route('/')
def index():
    # Cargar noticias desde un archivo JSON (supongamos que se llama noticias.json)
    with open('noticias.json', 'r', encoding='utf-8') as json_file:
        noticias = json.load(json_file)
    return render_template('noticias.html', noticias=noticias)

@app.route('/subir_noticia', methods=['POST'])
def subir_noticia():
    # Obtiene los datos del formulario
    titulo = request.form['titulo']
    contenido = request.form['contenido']

    # Genera el resumen y los puntos principales
    resumen, puntos_principales = generar_resumen_puntos_principales(contenido)

    # Genera la imagen descriptiva
    imagen_url = generar_imagen_descriptiva(resumen)

    # Crea una nueva noticia
    noticia = {'titulo': titulo, 'contenido': contenido, 'resumen': resumen, 'puntos_principales': puntos_principales, 'imagen_url': imagen_url}

    # Agrega la noticia al archivo JSON
    agregar_noticia(noticia)

    return redirect(url_for('index'))

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

def generar_resumen_puntos_principales(contenido):
    # Llama al API de ChatGPT para obtener un resumen y puntos principales
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # Utiliza el modelo adecuado
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"Genera un resumen en HTML del siguiente contenido:\n{contenido}"}
        ],
        max_tokens=150,  # Ajusta este valor según tus necesidades
        temperature=0.7,
    )

    return response

def generar_imagen_descriptiva(texto_descriptivo):
    # Generar un nombre de archivo único utilizando el sello de tiempo actual
    timestamp = int(time.time())
    imagen_nombre = f"imagen_descriptiva_{timestamp}.jpg"

    # Llama al API de Imagen de OpenAI para generar una imagen
    response = openai.Image.create(
        model="image-alpha-001",  # Utiliza el modelo adecuado
        prompt=texto_descriptivo,
        n=1,  # Puedes ajustar este valor según tus necesidades
        size="256x256",  # Tamaño de la imagen generada
    )

    # Guardar la imagen localmente
    imagen_url = response.data[0].url
    try:
        response = requests.get(imagen_url)
        response.raise_for_status()  # Lanzar una excepción si hay un error HTTP
        with open(f"static/{imagen_nombre}", 'wb') as imagen_file:
            imagen_file.write(response.content)
    except requests.exceptions.RequestException as e:
        # Manejar el error de descarga de la imagen (puedes registrar el error si es necesario)
        print(f

"Error al descargar la imagen descriptiva: {e}")

    # Devolver la ruta relativa de la imagen
    return f"/static/{imagen_nombre}"

def agregar_noticia(noticia):
    # Cargar noticias existentes
    try:
        with open('noticias.json', 'r', encoding='utf-8') as json_file:
            noticias = json.load(json_file)
    except FileNotFoundError:
        noticias = []

    # Agregar la nueva noticia
    noticias.append(noticia)

    # Guardar las noticias actualizadas en el archivo JSON
    with open('noticias.json', 'w', encoding='utf-8') as json_file:
        json.dump(noticias, json_file, ensure_ascii=False, indent=4)

if __name__ == '__main__':
    app.run(debug=True)
```

### Plantilla HTML (`noticias.html`):

```html
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Noticias</title>
    <style>
        /* Estilos similares a New York Times */
        body {
            font-family: Arial, Helvetica, sans-serif;
            background-color: #f4f4f4;
            padding: 20px;
        }
        h1 {
            font-size: 36px;
            color: #333;
            margin-bottom: 20px;
        }
        h2 {
            font-size: 24px;
            color: #333;
            margin-top: 20px;
        }
        img {
            max-width: 100%;
            height: auto;
            margin-top: 10px;
        }
        p {
            font-size: 18px;
            color: #666;
        }
    </style>
</head>
<body>
    <h1>Noticias</h1>
    <ul>
        {% for noticia in noticias %}
            <li>
                <h2>{{ noticia['titulo'] }}</h2>
                <img src="{{ noticia['imagen_url'] }}" alt="{{ noticia['titulo'] }}" width="300">
                <p>Resumen: {{ noticia['resumen'] | safe }}</p>
                <p>Puntos Principales: {{ noticia['puntos_principales'] | safe }}</p>
                <p>{{ noticia['contenido'] | safe }}</p>
            </li>
        {% endfor %}
    </ul>
    
    <h2>Subir Noticia</h2>
    <form method="POST" action="/subir_noticia">
        <label for="titulo">Título:</label>
        <input type="text" name="titulo" required><br>
        <label for="contenido">Contenido:</label>
        <textarea name="contenido" required></textarea><br>
        <input type="submit" value="Subir Noticia">
    </form>

    <h2>Descargar Noticias</h2>
    <a href="/descargar_pdf" target="_blank">Descargar Noticias en PDF</a>
    <a href="/descargar_html" target="_blank">Descargar Noticias en HTML</a>
</body>
</html>
```

En este código, hemos incluido las partes clave de la aplicación Flask y la plantilla HTML. Asegúrate de configurar tu clave de API de OpenAI en la variable `openai.api_key` y de reemplazar `TU_CLAVE_DE_API_DE_OPENAI` con tu clave real. También, asegúrate de crear un directorio llamado `static` en la carpeta principal de tu proyecto para guardar las imágenes descriptivas.

### Comentarios del Proyecto 1

El proyecto pudo alcanzar el objetivo, sin embargo, la calidad del diseño es mejorable, así como otras partes.

La principal ventaja de utilizar CHATGPT como asistente es el ahorro en la generación de código, pero el costo asociado a las peticiones y resolver los problemas intermedios es muy alto.

> Tabla de Dificultad

* Enviar la noticia mediante un formulario
* Recibir la noticia mediante un formulario
* Mostrar las noticias y el formulario
 
No tuvo mayor dificultad en generar un servidor de FLASK que recibiera noticias desde un formulario y las guardara en un JSON. Genero un HTML y un archivo de Python con todo lo necesario y se pudo montar sin problemas.

* Generar el resumen y los puntos principales de la noticia con CHATGPT

Se le solicitó agregar el resumen y los puntos principales usando CHATGPT:

    - El código generado utilizaba una versión vieja para la generación (`davinci`) 
    - El código no hacia dos llamadas simultáneas, sino que nos pedia dividir manualmente las peticiones
    - Se tuvo que especificar cómo se tendría que incorporar dicho código (`EXPERTO`)

* Generar la imagen de la noticia con DALL-E

    - El código no utiliza el API de DALL-E y hay especificarlo (`NO FUNCIONAL`)

Mostrar las noticias utilizando la imagen generada y el resumen

    - El código HTML no se veía correctamente (`EXPERTO`)
    - Inclusión de diseño

Generar un PDF con las noticias

    - No funcionó hasta descargar WKHTMLTOPDF
    - La url no funcionaba y se tuvo que corregir desde la creación (`EXPERTO`)

## Proyecto .3



