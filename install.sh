#!/bin/bash

# Nomouse Installation Script
echo "Installing Nomouse - Transparent Grid Overlay"

# Check if Python 3 is installede
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed. Please install Python 3 first."
    exit 1
fi

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "Error: pip3 is not installed. Please install pip3 first."
    exit 1
fi

echo "Installing Python dependencies..."
pip3 install -r requirements.txt

if [ $? -eq 0 ]; then
    echo "Installation completed successfully!"
    echo ""
    echo "To run the application:"
    echo "  xhost +SI:localuser:root"
    echo "  sudo python3 nomouse.py"
    echo ""
    echo "Usage:"
    echo "  - Press Ctrl+; to show the overlay"
    echo "  - Type a two-letter code to move mouse to that cell"
    echo "  - Press Escape to close the overlay"
    echo "  - Press Ctrl+C to exit the application"
else
    echo "Error: Failed to install dependencies. Please check your Python/pip installation."
    exit 1
fi 