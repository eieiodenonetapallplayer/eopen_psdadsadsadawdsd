const express = require('express');
const { spawn } = require('child_process');
const path = require('path');
const app = express();
const port = 3000;

app.use(express.static(path.join(__dirname, 'dist')));
app.use(express.json());

app.post('/run-python', (req, res) => {
  const pythonProcess = spawn('python', ['main.py']);
  let output = '';
  let errorOutput = '';

  pythonProcess.stdout.setEncoding('utf8');
  pythonProcess.stdout.on('data', (data) => {
    output += data.toString();
  });

  pythonProcess.stderr.setEncoding('utf8');
  pythonProcess.stderr.on('data', (data) => {
    errorOutput += data.toString();
  });

  pythonProcess.on('close', (code) => {
    if (code === 0) {
      res.setHeader('Content-Type', 'text/plain; charset=utf-8');
      res.send(output);
    } else {
      res.status(500).setHeader('Content-Type', 'text/plain; charset=utf-8');
      res.send(errorOutput || `Process exited with code ${code}`);
    }
  });
});

app.get('*', (req, res) => {
  res.sendFile(path.join(__dirname, 'dist', 'index.html'));
});

app.listen(port, () => {
  console.log(`Server running at http://localhost:${port}`);
});