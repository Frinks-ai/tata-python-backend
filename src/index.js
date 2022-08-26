import fs from 'fs';
import path from 'path';
import express from 'express';
import { createServer } from 'http';
import { spawn } from 'child_process';

import middlewaresConfig from './config/middleware';
import constants from './config/constants';

const app = express();
const httpServer = createServer(app);

middlewaresConfig(app);

app.post('/image', (req, res) => {
  try {
    const { image } = req.body;
    fs.writeFile(`${constants.BASE_PATH}/images/upload.bmp`, image, 'base64', err => {
      if (err) {
        console.log(err);
      }
    });
    res.status(200).json({
      success: true,
      status: 'File uploaded successfully'
    });
  } catch (err) {
    console.log('image --- post --- error', err);
    res.status(500).json({
      success: false,
      status: 'File upload error please retry'
    });
  }
});

app.get('/analysis', (req, res) => {
  try {
    const pythonData = spawn('python3', [path.resolve(process.cwd(), 'scripts/main.py')]);
    pythonData.stdout.on('data', data => {
      res.status(200).json({
        success: true,
        status: 'Result Found',
        data: {
          analysis: JSON.parse(data),
          dividend: constants.DEVIATION
        }
      });
    });
  } catch (err) {
    console.log('analysis -------- error', err);
    res.send('Error occured');
  }
});

app.get('/images', (req, res) => {
  try {
    const filepath = `${constants.BASE_PATH}/images/${req.query.params}`;
    return res.sendFile(filepath);
  } catch (err) {
    console.log('images --- get --- error', err);
    return res.send('Error occured');
  }
});

if (!module.parent) {
  httpServer.listen(constants.PORT, err => {
    if (err) {
      console.log('Cannot run!');
    } else {
      console.log(`API server listening on port: ${constants.PORT}`);
    }
  });
}

app.post('/update-file', (req, res) => {
  try {
    const { file, filename } = req.body;
    fs.writeFile(`${constants.BASE_PATH}/scripts/${filename}`, file, 'base64', err => {
      if (err) {
        console.log(err);
      }
    });
    res.status(200).json({
      success: true,
      status: 'File uploaded successfully'
    });
  } catch (err) {
    console.log('update file --- post --- error', err);
    res.status(500).json({
      success: false,
      status: 'File upload error please retry'
    });
  }
});

export default app;
