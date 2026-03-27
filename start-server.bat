@echo off
setlocal enabledelayedexpansion

REM Startup script for Health Prediction System
REM This script starts the backend API server

cls
echo.
echo ========================================================
echo     Health Prediction System - Starting API
echo ========================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in your PATH.
    echo Please install Python from https://www.python.org/
    pause
    exit /b 1
)

echo Starting Flask backend API server...
echo.
echo The server will be available at: http://127.0.0.1:5000
echo.
echo Dashboard: Open frontend/index.html in your browser
echo.
echo Press Ctrl+C to stop the server
echo.
echo ========================================================
echo.

REM Get the directory of the batch file
set "PROJECT_ROOT=%~dp0"
cd /d "%PROJECT_ROOT%backend"

REM Run the app
python app.py

if errorlevel 1 (
    echo.
    echo [ERROR] The backend server failed to start or crashed.
    echo Please check the error messages above.
    echo.
)

pause
