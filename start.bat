@echo off
REM ResQPaws - Quick Start Setup Script (Windows CMD version)
REM Run this script to set up and start the application

setlocal enabledelayedexpansion

echo.
echo ================================
echo   ResQPaws - Quick Start Setup
echo ================================
echo.

REM Check if venv exists
if not exist "venv\Scripts\activate.bat" (
    echo [ERROR] Virtual environment not found!
    echo Run: python -m venv venv
    pause
    exit /b 1
)

REM Step 1: Activate virtual environment
echo [1/3] Activating virtual environment...
call venv\Scripts\activate.bat
echo      ✓ Virtual environment activated
echo.

REM Step 2: Install requirements
echo [2/3] Installing packages...
pip install --upgrade -r requirements.txt
echo      ✓ Packages installed
echo.

REM Step 3: Start the application
echo [3/3] Starting ResQPaws application...
echo.
echo ==========================================
echo   Application is running!
echo   Open: http://localhost:5000
echo   Press Ctrl+C to stop
echo ==========================================
echo.

python app.py

if errorlevel 1 (
    echo.
    echo ERROR: Application failed to start
    echo Check the error messages above
    pause
)
