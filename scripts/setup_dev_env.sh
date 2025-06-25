#!/bin/bash

# DataFlow Toolkit Development Environment Setup Script

set -e  # Exit on error

echo "🚀 Setting up DataFlow Toolkit development environment..."

# Check Python version
PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
REQUIRED_VERSION="3.9"

if [ "$(printf '%s\n' "$REQUIRED_VERSION" "$PYTHON_VERSION" | sort -V | head -n1)" != "$REQUIRED_VERSION" ]; then
    echo "❌ Error: Python $REQUIRED_VERSION or higher is required (found $PYTHON_VERSION)"
    exit 1
fi

echo "✅ Python version check passed: $PYTHON_VERSION"

# Create virtual environment
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
else
    echo "📦 Virtual environment already exists"
fi

# Activate virtual environment
echo "🔌 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip setuptools wheel

# Install package in development mode
echo "📥 Installing DataFlow Toolkit in development mode..."
pip install -e ".[dev,docs]"

# Install pre-commit hooks
echo "🪝 Installing pre-commit hooks..."
pre-commit install

# Create necessary directories
echo "📁 Creating project directories..."
mkdir -p logs data temp

# Run initial tests
echo "🧪 Running initial tests..."
pytest tests/unit -v

# Check code quality
echo "🔍 Checking code quality..."
make lint || true

echo "✨ Development environment setup complete!"
echo ""
echo "To activate the environment, run:"
echo "  source venv/bin/activate"
echo ""
echo "Available make commands:"
echo "  make test         - Run tests"
echo "  make lint         - Run linters"
echo "  make format       - Format code"
echo "  make build        - Build package"
echo "  make docs         - Build documentation"
