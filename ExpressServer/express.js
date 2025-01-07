import express from 'express';
import path from 'path';
import fs from 'fs';
import cors from 'cors';
import { fileURLToPath } from 'url';
import helmet from 'helmet';  // Add Helmet for basic security
import rateLimit from 'express-rate-limit';  // Add rate-limiting

const app = express();
const port = 3000;

// Get __filename and __dirname in ES modules
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

app.set('trust proxy', 1);

// Apply Helmet for basic security (sets security-related headers)
app.use(helmet());

// Enable CORS (allow all origins)
const allowedOrigins = [
    'https://enabled-needed-kitten.ngrok-free.app', // Your static Ngrok domain
    'https://algernopkrieger42.github.io', // GitHub Pages
];

// Update the CORS middleware
app.use(cors({
    origin: (origin, callback) => {
        console.log(`Incoming Origin: ${origin}`); // Log the origin
        console.time('CORS Evaluation');
        if (allowedOrigins.includes(origin) || !origin) {
            console.timeEnd('CORS Evaluation');
            callback(null, true);
        } else {
            console.timeEnd('CORS Evaluation');
            console.error(`Origin ${origin} is not allowed by CORS`);
            callback(new Error('Not allowed by CORS'));
        }
    },
}));

app.use((req, res, next) => {
    res.setHeader('ngrok-skip-browser-warning', 'true');
    console.log(`Added ngrok-skip-browser-warning header for ${req.method} ${req.url}`);
    next();
});

app.use((err, req, res, next) => {
    res.setHeader('ngrok-skip-browser-warning', 'true');
    console.error('Error middleware triggered:', err.message);
    res.status(500).send('Internal Server Error');
});


// Handle OPTIONS preflight requests for all routes
app.options('*', (req, res) => {
    res.setHeader('ngrok-skip-browser-warning', 'true');
    res.setHeader('Access-Control-Allow-Origin', 'https://algernopkrieger42.github.io');
    res.setHeader('Access-Control-Allow-Methods', 'GET, OPTIONS');
    res.setHeader('Access-Control-Allow-Headers', 'Content-Type, bypass-tunnel-reminder');
    res.status(204).send();
});

app.options('/predictions.json', cors({
    origin: allowedOrigins,
    methods: ['GET', 'OPTIONS'],
    allowedHeaders: ['ngrok-skip-browser-warning', 'Content-Type', 'Authorization', 'bypass-tunnel-reminder'],
    optionsSuccessStatus: 204, // Respond quickly for preflight
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


