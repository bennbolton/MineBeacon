#!/bin/bash

# Activate the virtual environment
source ~/Minebeacon/.venv/bin/activate

# Start frontend
python ~/Minebeacon/src/app.py &
DASH_PID=$!

# Function to stop servers on CTRL+C
cleanup() {
    echo "Shutting down dashboard..."
    kill $DASH_PID
    wait $DASH_PID
    echo "Dashboard stopped."
    exit 0
}

# Trap CTRL+C
trap cleanup SIGINT

# Wait for both servers
wait $DASH_PID