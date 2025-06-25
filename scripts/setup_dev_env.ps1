# DataFlow Toolkit Development Environment Setup Script for Windows

Write-Host "🚀 Setting up DataFlow Toolkit development environment..." -ForegroundColor Green

# Check Python version
try {
    $pythonVersion = python --version 2>&1 | Out-String
    if ($pythonVersion -match "Python (\d+\.\d+)") {
        $version = [version]$matches[1]
        if ($version -ge [version]"3.9") {
            Write-Host "✅ Python version check passed: $version" -ForegroundColor Green
        } else {
            Write-Host "❌ Error: Python 3.9 or higher is required (found $version)" -ForegroundColor Red
            exit 1
        }
    }
} catch {
    Write-Host "❌ Error: Python is not installed or not in PATH" -ForegroundColor Red
    exit 1
}

# Create virtual environment
if (!(Test-Path "venv")) {
    Write-Host "📦 Creating virtual environment..." -ForegroundColor Yellow
    python -m venv venv
} else {
    Write-Host "📦 Virtual environment already exists" -ForegroundColor Yellow
}

# Activate virtual environment
Write-Host "🔌 Activating virtual environment..." -ForegroundColor Yellow
& ".\venv\Scripts\Activate.ps1"

# Upgrade pip
Write-Host "⬆️  Upgrading pip..." -ForegroundColor Yellow
python -m pip install --upgrade pip setuptools wheel

# Install package in development mode
Write-Host "📥 Installing DataFlow Toolkit in development mode..." -ForegroundColor Yellow
pip install -e ".[dev,docs]"

# Install pre-commit hooks
Write-Host "🪝 Installing pre-commit hooks..." -ForegroundColor Yellow
pre-commit install

# Create necessary directories
Write-Host "📁 Creating project directories..." -ForegroundColor Yellow
New-Item -ItemType Directory -Force -Path logs, data, temp | Out-Null

Write-Host "✨ Development environment setup complete!" -ForegroundColor Green
Write-Host ""
Write-Host "To activate the environment, run:" -ForegroundColor Cyan
Write-Host "  .\venv\Scripts\Activate.ps1" -ForegroundColor White
Write-Host ""
Write-Host "Available make commands:" -ForegroundColor Cyan
Write-Host "  make test         - Run tests" -ForegroundColor White
Write-Host "  make lint         - Run linters" -ForegroundColor White
Write-Host "  make format       - Format code" -ForegroundColor White
Write-Host "  make build        - Build package" -ForegroundColor White
Write-Host "  make docs         - Build documentation" -ForegroundColor White
