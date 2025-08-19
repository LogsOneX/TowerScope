#!/bin/bash
# TowerScope Environment Setup Script

echo "Setting up TowerScope environment..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Python 3 is not installed. Please install it first."
    exit 1
fi

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv towerScope-env

# Activate virtual environment
echo "Activating virtual environment..."
source towerScope-env/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

echo "Setup complete! Activate the environment with: source towerScope-env/bin/activate"
