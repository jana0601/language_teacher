@echo off
REM Language Teacher GUI Launcher - Simplified Version

echo Starting Language Teacher GUI...

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

REM Start the simplified GUI
python gui_simple.py

pause
