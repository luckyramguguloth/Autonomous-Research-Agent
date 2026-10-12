@echo off
setlocal enabledelayedexpansion
title Autonomous Research Agent

echo ======================================================================
echo                  AUTONOMOUS RESEARCH AGENT
echo       Deep Research with Multi-Step Reasoning ^& Knowledge Graphs
echo ======================================================================
echo.

:: Change directory to script location
cd /d "%~dp0"

:: Check virtual environment
if not exist "%~dp0venv\Scripts\activate.bat" (
    echo [ERROR] Virtual environment not found at:
    echo         "%~dp0venv\Scripts\activate.bat"
    echo.
    echo Please create the virtual environment before running:
    echo   python -m venv venv
    echo   venv\Scripts\activate
    echo   pip install -r requirements.txt
    echo.
    pause
    exit /b 1
)

:: Check for .env file
if not exist "%~dp0.env" (
    echo [WARNING] No .env file found in project root.
    echo Make sure GOOGLE_API_KEY is configured in your environment or create a .env file.
    echo Example:
    echo   GOOGLE_API_KEY=your_api_key_here
    echo.
)

:: Activate Virtual Environment
echo [INFO] Activating virtual environment...
call "%~dp0venv\Scripts\activate.bat"
if errorlevel 1 (
    echo [ERROR] Failed to activate virtual environment.
    pause
    exit /b 1
)

:: Verify Streamlit installation
where streamlit >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Streamlit is not installed in the virtual environment.
    echo Please install dependencies:
    echo   pip install -r requirements.txt
    echo.
    pause
    exit /b 1
)

echo [INFO] Virtual environment active.
echo [INFO] Starting Streamlit dashboard...
echo [INFO] Opening in browser (Default: http://localhost:8501)...
echo [INFO] Press Ctrl+C in this terminal to stop the application.
echo.

streamlit run app.py

if errorlevel 1 (
    echo.
    echo [ERROR] Application exited with an error code: %errorlevel%
    pause
    exit /b %errorlevel%
)

echo.
echo Application finished.
pause
