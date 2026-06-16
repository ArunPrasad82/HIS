#!/bin/bash
# Installation script for Hospital Information System

set -e

echo ""
echo "========================================="
echo "Hospital Information System Setup"
echo "========================================="
echo ""

# Check Python version
echo "Checking Python version..."
python3 --version
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed"
    exit 1
fi

# Create virtual environment
echo ""
echo "Creating virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "✓ Virtual environment created"
else
    echo "✓ Virtual environment already exists"
fi

# Activate virtual environment
echo ""
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo ""
echo "Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo ""
echo "Installing dependencies..."
pip install -r requirements.txt
echo "✓ Dependencies installed"

# Create necessary directories
echo ""
echo "Creating necessary directories..."
mkdir -p logs
mkdir -p uploads
mkdir -p reports
mkdir -p backups
echo "✓ Directories created"

# Run migrations
echo ""
echo "Running database migrations..."
echo ""
python3 migrations/001_init_schema.py

# Run seeding
echo ""
echo "Seeding initial data..."
echo ""
python3 migrations/002_seed_data.py

# Configuration file creation
echo ""
echo "Creating configuration files..."
if [ ! -f ".env" ]; then
    cp .env.example .env
    echo "✓ .env file created (please update with your settings)"
else
    echo "✓ .env file already exists"
fi

echo ""
echo "========================================="
echo "✓ Installation Complete!"
echo "========================================="
echo ""
echo "To start the application, run:"
echo "  source venv/bin/activate"
echo "  streamlit run app.py"
echo ""
echo "Default Login Credentials:"
echo "  Username: admin"
echo "  Password: admin@123"
echo ""
echo "Note: Change the default password after first login!"
echo ""
