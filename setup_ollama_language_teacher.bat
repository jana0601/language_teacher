@echo off
REM Setup script for Language Teacher with Ollama (Windows)

echo 🌍 Language Teacher Setup Script
echo ================================

REM Check if Ollama is installed
ollama --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Ollama is not installed!
    echo Please install Ollama from: https://ollama.ai
    echo Then run this script again.
    pause
    exit /b 1
)

echo ✅ Ollama is installed

REM Check if llama3.2 model is available
ollama list | findstr "llama3.2" >nul
if %errorlevel% neq 0 (
    echo 📥 Downloading llama3.2 model (this may take a few minutes)...
    ollama pull llama3.2
    if %errorlevel% neq 0 (
        echo ❌ Failed to download llama3.2 model
        pause
        exit /b 1
    )
    echo ✅ llama3.2 model downloaded successfully
) else (
    echo ✅ llama3.2 model is already available
)

REM Start Ollama server
echo 🚀 Starting Ollama server...
start /b ollama serve

REM Wait a moment for server to start
timeout /t 3 /nobreak >nul

REM Check if server is running
curl -s http://localhost:11434/api/tags >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Failed to start Ollama server
    pause
    exit /b 1
)

echo ✅ Ollama server is running on localhost:11434

echo.
echo 🎉 Setup complete!
echo.
echo Next steps:
echo 1. Install Python dependencies: pip install -r backend\requirements.txt
echo 2. Start the backend: cd backend ^&^& python main.py
echo 3. Open frontend\index.html in your browser
echo.
echo Ollama server is running in the background
echo To stop Ollama: taskkill /f /im ollama.exe
pause
