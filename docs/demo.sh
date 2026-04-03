#!/bin/bash
# Demo Script - AgriScan AI
# ========================
# Run this script to demonstrate the AI Crop Disease Detection system

echo "=========================================="
echo "   AgriScan AI - Demo Launcher"
echo "=========================================="
echo ""

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is required but not installed."
    exit 1
fi

# Function to start backend
start_backend() {
    echo "Starting Flask backend..."
    cd "$(dirname "$0")/backend"
    source ../../.venv/bin/activate 2>/dev/null || true
    python3 app.py
}

# Function to start frontend
start_frontend() {
    echo "Starting React frontend..."
    cd "$(dirname "$0")/frontend"
    npm start
}

# Main menu
echo "Select demo option:"
echo "1. Start Backend Only (API on port 5000)"
echo "2. Start Frontend Only (Web UI on port 3000)"
echo "3. Start Both (Full Stack)"
echo "4. Run Quick Test (Mock Prediction)"
echo "5. Exit"
echo ""

read -p "Enter your choice (1-5): " choice

case $choice in
    1)
        start_backend
        ;;
    2)
        start_frontend
        ;;
    3)
        echo "Starting backend in background..."
        start_backend &
        sleep 3
        echo "Starting frontend..."
        start_frontend
        ;;
    4)
        cd "$(dirname "$0")"
        python3 -c "
import sys
sys.path.append('model')
from inference import predict_disease
result = predict_disease('sample_images/sample_leaf.jpg')
print('Mock Prediction Result:')
print(f\"Disease: {result['disease']}\")
print(f\"Confidence: {result['confidence']}%\")
print(f\"Treatment: {result['treatment']}\")
"
        ;;
    5)
        echo "Exiting..."
        exit 0
        ;;
    *)
        echo "Invalid choice. Exiting."
        exit 1
        ;;
esac