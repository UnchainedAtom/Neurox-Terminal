#!/bin/bash
# Neurox Terminal API startup script for Raspberry Pi

set -e

# Script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Virtual environment path
VENV_DIR="neuroxnodeTerminal-venv"
VENV_PYTHON="$VENV_DIR/bin/python"

# Check if virtual environment exists and is usable
if [ ! -x "$VENV_PYTHON" ]; then
    if [ -d "$VENV_DIR" ]; then
        echo "Existing virtual environment is not usable. Recreating..."
        rm -rf "$VENV_DIR"
    fi
    echo "Creating virtual environment..."
    python3 -m venv "$VENV_DIR"
fi

# Install/update dependencies
echo "Installing dependencies..."
"$VENV_PYTHON" -m pip install --upgrade pip
"$VENV_PYTHON" -m pip install -r requirements.txt

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
"$VENV_PYTHON" neuronodeTerminal_api.py
