const express = require('express');
const multer = require('multer');
const AdmZip = require('adm-zip');
const fs = require('fs');
const pdf = require('pdf-parse');
const OpenAIApi = require('openai');

const app = express();
const port = 3000;

const storage = multer.diskStorage({
  destination: (req, file, cb) => {
    cb(null, 'uploads');
  },
  filename: (req, file, cb) => {
    cb(null, file.originalname);
  },
});

const upload = multer({ storage: storage });

// Configura tu clave de API de OpenAI
const apiKey = 'TU_API_KEY'; // Reemplaza con tu clave de API

app.post('/upload', upload.single('zipFile'), async (req, res) => {
  const zipFilePath = `uploads/${req.file.originalname}`;
  const unzipDir = `uploads/${req.file.originalname.split('.zip')[0]}`;

  // Descomprimir el archivo ZIP
  const zip = new AdmZip(zipFilePath);
  zip.extractAllTo(unzipDir, true);

  // Leer y procesar archivos PDF
  const pdfFiles = fs.readdirSync(unzipDir);

  const openai = new OpenAIApi({ apiKey });

  let allSummaries = ''; // Variable para almacenar todos los resúmenes

  for (const pdfFile of pdfFiles) {
    if (pdfFile.endsWith('.pdf')) {
      const pdfFilePath = `${unzipDir}/${pdfFile}`;

      // Extraer el texto del PDF con pdf-parse
      const dataBuffer = fs.readFileSync(pdfFilePath);
      const data = await pdf(dataBuffer);

      // Generar un resumen utilizando el API de Completación de Chat de OpenAI
      const prompt = `Traduce a español y resumen de \n${data.text}`;
      const completionResponse = await openai.chat.completions.create({
        messages: [
          { role: 'system', content: 'Eres un asistente que genera resúmenes' },
          { role: 'user', content: prompt },
        ],
        model: 'gpt-3.5-turbo-16k',
      });

      const summary = completionResponse.choices[0].message.content;

      // Guardar el resumen en un archivo .txt
      const summaryFilePath = `${unzipDir}/${pdfFile.replace('.pdf', '_summary.txt')}`;
      fs.writeFileSync(summaryFilePath, summary);

      // Agregar el resumen al texto acumulado
      allSummaries += summary + '\n';
    }
  }

  // Guardar el texto acumulado en un archivo
  const allSummariesFilePath = `${unzipDir}/all_summaries.txt`;
  fs.writeFileSync(allSummariesFilePath, allSummaries);

  // Eliminar el archivo ZIP cargado
  fs.unlinkSync(zipFilePath);

  // Analizar los resúmenes con OpenAI (aquí debes implementar tu análisis específico)
  // Por ejemplo, podrías enviar el texto a una función de análisis personalizada

  res.status(200).json({ message: 'Archivos ZIP descomprimidos, textos extraídos, resúmenes generados y analizados exitosamente.' });
});

// Ruta para servir el formulario HTML
app.get('/', (req, res) => {
    res.sendFile(__dirname + '/index.html');
 });

app.listen(port, () => {
  console.log(`Servidor escuchando en el puerto ${port}`);
});