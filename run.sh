#!/bin/bash

echo "---- APP START SCRIPT ----"

# Always run from project root
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR" || exit 1

echo "Pulling latest code (if git repo)..."
if [ -d ".git" ]; then
    git pull --rebase || true
fi

echo "Activating virtual environment (if exists)..."
if [ -d "venv" ]; then
    source venv/bin/activate
fi

echo "Installing dependencies..."
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
fi

echo "Stopping existing app..."
pkill -f "python app.py" || true

sleep 1

echo "Starting app..."
nohup python3 app.py > logs.txt 2>&1 &

echo "App running in background."
echo "Logs: tail -f logs.txt"
echo "---- DONE ----"