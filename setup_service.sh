#!/bin/bash

# Setup script for Nomouse systemd service
echo "Setting up Nomouse as a system service..."

# Check if running as root
if [ "$EUID" -ne 0 ]; then
    echo "This script must be run as root (use sudo)"
    exit 1
fi

# Install Python dependencies for root
echo "Installing Python dependencies for root user..."
pip3 install -r requirements.txt

# Copy service file to systemd directory
echo "Installing systemd service..."
cp nomouse.service /etc/systemd/system/

# Reload systemd to recognize the new service
systemctl daemon-reload

# Enable the service to start on boot
systemctl enable nomouse.service

# Start the service
systemctl start nomouse.service

echo ""
echo "Nomouse service has been installed and started!"
echo ""
echo "Service status:"
systemctl status nomouse.service --no-pager -l
echo ""
echo "To manage the service:"
echo "  Start:   sudo systemctl start nomouse"
echo "  Stop:    sudo systemctl stop nomouse"
echo "  Restart: sudo systemctl restart nomouse"
echo "  Status:  sudo systemctl status nomouse"
echo "  Logs:    sudo journalctl -u nomouse -f"
echo ""
echo "The app will now start automatically on boot!"
echo "Press Ctrl+; to show the overlay." 