#!/bin/bash
set -e

echo "Installing Python 3.10..."
apt-get update
apt-get install -y python3.10 python3.10-venv python3.10-dev

echo "Creating virtual environment with Python 3.10..."
python3.10 -m venv venv
source venv/bin/activate

echo "Upgrading pip..."
pip install --upgrade pip

echo "Installing dependencies..."
pip install -r requirements.txt

echo "Build complete!"
