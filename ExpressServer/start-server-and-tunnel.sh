#!/bin/bash
# Start the Express server using npx to ensure the correct path is used
npx pm2 start express.js --name my-express-server

# Start the localtunnel and capture the URL
TUNNEL_URL=$(npx localtunnel --port 3002 --subdomain 52crewdata)

# Echo the URL to the terminal
echo $TUNNEL_URL

