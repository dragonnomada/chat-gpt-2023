const express = require('express');
const multer = require('multer');
const AdmZip = require('adm-zip');
const fs = require('fs');
const app = express();
const port = 3000;

// Configuración de multer para gestionar la carga de archivos ZIP
const storage = multer.diskStorage({
  destination: (req, file, cb) => {
    cb(null, 'uploads');
  },
  filename: (req, file, cb) => {
    cb(null, file.originalname);
  },
});

const upload = multer({ storage: storage });

// Ruta para cargar archivos ZIP
app.post('/upload', upload.single('zipFile'), (req, res) => {
  const zipFilePath = `uploads/${req.file.originalname}`;
  const unzipDir = `uploads/${req.file.originalname.split('.zip')[0]}`;

  // Descomprimir el archivo ZIP
  const zip = new AdmZip(zipFilePath);
  zip.extractAllTo(unzipDir, true);

  // Eliminar el archivo ZIP cargado
  fs.unlinkSync(zipFilePath);

  res.status(200).json({ message: 'Archivos ZIP descomprimidos exitosamente.' });
});

// Ruta para servir el formulario HTML
app.get('/', (req, res) => {
    res.sendFile(__dirname + '/index.html');
 });

app.listen(port, () => {
  console.log(`Servidor escuchando en el puerto ${port}`);
});
