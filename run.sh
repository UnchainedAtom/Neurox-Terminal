#!/bin/bash
# Neurox Terminal API startup script for Raspberry Pi

set -e

# Script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Virtual environment path
VENV_DIR="neuroxnodeTerminal-venv"

# Check if virtual environment exists
if [ ! -d "$VENV_DIR" ]; then
    echo "Creating virtual environment..."
    python3 -m venv "$VENV_DIR"
fi

# Activate virtual environment
echo "Activating virtual environment..."
source "$VENV_DIR/bin/activate"

# Install/update dependencies
echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Check for .env file
if [ ! -f ".env" ]; then
    echo "Warning: .env file not found. Creating from .env.example..."
    if [ -f ".env.example" ]; then
        cp .env.example .env
        echo "Created .env file. Please edit it with your Home Assistant configuration."
    else
        echo "Error: .env.example not found"
        exit 1
    fi
fi

# Start the application
echo "Starting Neurox Terminal API..."
python neuronodeTerminal_api.py