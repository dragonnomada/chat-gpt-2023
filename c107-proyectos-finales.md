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

![1.1](<Captura de pantalla 2023-09-08 a la(s) 13.48.55.png>)

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