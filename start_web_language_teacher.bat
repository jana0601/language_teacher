@echo off
REM Language Teacher Web Application Launcher

echo Starting Language Teacher Web Application...
echo.

REM Check if Ollama is running
curl -s http://localhost:11434/api/tags >nul 2>&1
if %errorlevel% neq 0 (
    echo WARNING: Ollama is not running!
    echo Please start Ollama first:
    echo   ollama serve
    echo.
    echo Continuing anyway...
) else (
    echo SUCCESS: Ollama is running
)

echo.
echo Starting web application...
echo The application will open in your browser automatically
echo.

python web_server.py

pause
