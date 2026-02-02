@echo off
setlocal
title Visual Model Dashboard Launcher

echo ===========================================
echo Visual Model Dashboard Setup & Run
echo ===========================================

rem Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed or not in PATH.
    echo Please install Python 3.10+ from https://www.python.org/downloads/
    pause
    exit /b
)

rem Check if Ollama is installed
ollama --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [WARNING] Ollama is not detected in PATH.
    echo Please ensure Ollama is installed and running (https://ollama.com/).
    echo Continuing anyway, but model generation might fail...
) else (
    echo [INFO] Ollama detected. Ensuring model 'qwen3:0.6b' is available...
    ollama pull qwen3:0.6b
)

rem Create Virtual Environment if it doesn't exist
if not exist "venv" (
    echo [INFO] Creating virtual environment...
    python -m venv venv
)

rem Activate Virtual Environment
call venv\Scripts\activate

rem Install dependencies
echo [INFO] Installing/Updating dependencies...
pip install -r requirements.txt

echo ===========================================
echo Setup complete. Starting Dashboard...
echo Dashboard URL: http://127.0.0.1:8000
echo ===========================================

rem Run the application
python main.py

pause
