#!/bin/bash
# Render startup script

# Use PORT environment variable if provided (Render sets this)
PORT=${PORT:-8000}

echo "Starting Pickup Soccer API on port $PORT"

# Start uvicorn
python3.11 -m uvicorn api:app --host 0.0.0.0 --port $PORT
