import express from 'express';
import path from 'path';
import fs from 'fs';
import cors from 'cors';
import { fileURLToPath } from 'url';

const app = express();
const port = 3001;

// Get __filename and __dirname in ES modules
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

app.use(cors({
    origin: 'https//algernopkrieger42.github.io/Exit52/',
}));

// Serve the latest predictions.json file
app.get('/predictions.json', (req, res) => {
    const filePath = path.join(__dirname, 'predictions.json');
    
    // Check if file exists and is updated
    if (fs.existsSync(filePath)) {
        res.sendFile(filePath);
    } else {
        res.status(404).send('File not found');
    }
});


// Default route to handle other requests
app.get('/', (req, res) => {
    res.send('Welcome to the Express server!');
});

// Start the server
app.listen(port, () => {
    console.log(`Server is running on port ${port}`);
});



