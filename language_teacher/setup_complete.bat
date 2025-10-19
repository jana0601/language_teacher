@echo off
REM Language Teacher Complete Setup Script for Windows
REM This script handles everything once Ollama is installed

echo Language Teacher Complete Setup
echo ====================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python from: https://python.org
    pause
    exit /b 1
)

echo SUCCESS: Python is available

REM Check if Ollama is installed
ollama --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Ollama is not installed or not in PATH
    echo Please install Ollama from: https://ollama.ai
    echo Then run this script again.
    pause
    exit /b 1
)

echo SUCCESS: Ollama is installed

REM Run the Python setup script
echo.
echo Running complete setup...
echo This will:
echo - Start Ollama service
echo - Download llama3.2 model (may take several minutes)
echo - Install Python dependencies
echo - Test everything
echo - Create startup script
echo.

python setup_simple.py

echo.
echo Setup completed! Check the output above for results.
pause
