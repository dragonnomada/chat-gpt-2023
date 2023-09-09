const express = require('express');
const multer = require('multer');
const AdmZip = require('adm-zip');
const fs = require('fs');
const pdf = require('pdf-parse'); // Importa la biblioteca pdf-parse
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

app.post('/upload', upload.single('zipFile'), async (req, res) => {
  const zipFilePath = `uploads/${req.file.originalname}`;
  const unzipDir = `uploads/${req.file.originalname.split('.zip')[0]}`;

  // Descomprimir el archivo ZIP
  const zip = new AdmZip(zipFilePath);
  zip.extractAllTo(unzipDir, true);

  // Leer y procesar archivos PDF
  const pdfFiles = fs.readdirSync(unzipDir);

  for (const pdfFile of pdfFiles) {
    if (pdfFile.endsWith('.pdf')) {
      const pdfFilePath = `${unzipDir}/${pdfFile}`;

      // Extraer el texto del PDF con pdf-parse
      const dataBuffer = fs.readFileSync(pdfFilePath);
      const data = await pdf(dataBuffer);

      // Guardar el texto en un archivo .txt
      const textFilePath = `${unzipDir}/${pdfFile.replace('.pdf', '.txt')}`;
      fs.writeFileSync(textFilePath, data.text);
    }
  }

  // Eliminar el archivo ZIP cargado
  fs.unlinkSync(zipFilePath);

  res.status(200).json({ message: 'Archivos ZIP descomprimidos y textos extraídos exitosamente.' });
});

// Ruta para servir el formulario HTML
app.get('/', (req, res) => {
    res.sendFile(__dirname + '/index.html');
 });

app.listen(port, () => {
  console.log(`Servidor escuchando en el puerto ${port}`);
});
