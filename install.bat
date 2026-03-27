@echo off
REM Installation script for Health Prediction System
REM This script will set up everything needed to run the application

echo.
echo ========================================================
echo     Health Prediction System - Installation
echo     ML Models + Dashboard + Internal Reports
echo ========================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python from: https://www.python.org/downloads/
    pause
    exit /b 1
)
echo [OK] Python is installed

REM Install requirements
echo.
echo Installing Python requirements...
pip install -r requirements.txt
if errorlevel 1 (
    echo WARNING: Some packages may not have installed correctly
    echo Try running: pip install -r requirements.txt manually
)

REM Run setup script
echo.
echo Running setup checks...
python setup.py

echo.
echo ========================================================
echo     Installation Complete!
echo ========================================================
echo.
echo Next Steps:
echo 1. Start the backend:  cd backend ^& python app.py
echo 2. Open dashboard:     Open frontend/index.html in browser
echo.
pause
