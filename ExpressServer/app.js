import express from 'express';
import path from 'path';
import fs from 'fs';
import cors from 'cors';
import ngrok from 'ngrok'
import { fileURLToPath } from 'url';

const app = express();
//const port = 3000;

// Get __filename and __dirname in ES modules
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

app.use(cors({
    origin: 'https//algernopkrieger42.github.io',
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

const PORT = process.env.PORT || 3000

// Start the server
//app.listen(port, async () => {
//    console.log(`Server is running on port ${port}`);
//});
app.listen(PORT, async () => {
    console.log(`Server is running on port ${PORT}`);

    try {
        const url = await ngrok.connect(PORT); // Connect ngrok to your server
        console.log(`ngrok tunnel opened at: ${url}`);
    } catch (err) {
        console.error('Error connecting to ngrok:', err);
    }
});

