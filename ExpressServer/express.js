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
    'https://algernopkrieger42.github.io',
];
app.use(cors({
    origin: (origin, callback) => {
        console.time('CORS Evaluation');
        if (allowedOrigins.includes(origin) || !origin) {
            console.timeEnd('CORS Evaluation');
            callback(null, true);
        } else {
            console.timeEnd('CORS Evaluation');
            callback(new Error('Not allowed by CORS'));
        }
    },
}));

// Set up a rate limiter to limit requests (100 requests per 15 minutes per IP)
/*const limiter = rateLimit({
    windowMs: 15 * 60 * 1000, // 15 minutes
    max: 100, // Limit each IP to 100 requests per `windowMs`
    message: 'Too many requests, please try again later.',
});
app.use(limiter);*/
app.use((req, res, next) => next());

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


/*import express from 'express';
import path from 'path';
import fs from 'fs';
import cors from 'cors';
import { fileURLToPath } from 'url';

const app = express();
const port = 3002;

// Get __filename and __dirname in ES modules
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

app.use(cors({
    origin: 'https://algernopkrieger42.github.io',
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
});*/



