@echo off
REM Language Teacher GUI Launcher for Windows

echo 🌍 Language Teacher GUI Launcher
echo ========================================

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python is not installed or not in PATH
    echo Please install Python from: https://python.org
    pause
    exit /b 1
)

echo ✅ Python is installed

REM Check if Ollama is running
curl -s http://localhost:11434/api/tags >nul 2>&1
if %errorlevel% neq 0 (
    echo ⚠️  Ollama is not running!
    echo Please make sure Ollama is installed and running:
    echo 1. Install from: https://ollama.ai
    echo 2. Run: ollama pull llama3.2
    echo 3. Run: ollama serve
    echo.
    echo Continuing anyway...
) else (
    echo ✅ Ollama is running
)

echo 🚀 Launching Language Teacher GUI...
python run_gui.py

pause
