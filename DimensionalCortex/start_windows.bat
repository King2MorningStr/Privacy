@echo off
echo ================================================
echo   DIMENSIONAL CORTEX - SETUP
echo   Universal AI Continuity Engine
echo ================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ from python.org
    pause
    exit /b 1
)

echo [1/4] Installing Python dependencies...
pip install flask flask-cors numpy --quiet

if %errorlevel% neq 0 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)

echo [2/4] Creating project directories...
if not exist "data" mkdir data

echo [3/4] Starting Dimensional Cortex server...
echo.
echo ================================================
echo   SERVER STARTING
echo ================================================
echo.
echo Dashboard: http://localhost:5000/dashboard
echo Upgrade:   http://localhost:5000/upgrade
echo API:       http://localhost:5000/stats
echo.
echo Press Ctrl+C to stop the server
echo.

REM Start server
python cortex_server.py

pause
