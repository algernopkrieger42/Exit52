#!/bin/bash

# Start the Express server using pm2, ensuring it restarts if it crashes
npx pm2 start express.js --name my-express-server

# Function to start LocalTunnel and check connection
start_tunnel() {
    while true; do
        echo "Starting LocalTunnel..."
        npx localtunnel --port 3002 --subdomain 52crewdata > tunnel.log 2>&1 &
        TUNNEL_PID=$!
        
        # Sleep for 10 seconds to allow tunnel to initialize
        sleep 10
        
        # Check if LocalTunnel is running
        if grep -q "your url is" tunnel.log; then
            echo "LocalTunnel started successfully."
            break
        else
            echo "LocalTunnel failed to start. Retrying in 5 seconds..."
            kill $TUNNEL_PID
            sleep 5
        fi
    done
}

# Start LocalTunnel and monitor the connection
start_tunnel

# Monitor the LocalTunnel process and restart if it goes down
while true; do
    if ! pgrep -f "lt --port 3002" > /dev/null; then
        echo "LocalTunnel has stopped. Restarting..."
        start_tunnel
    fi
    sleep 60  # Check the status every minute
done


