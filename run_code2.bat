@echo off
title Student Academic Risk Detection System
echo ---------------------------------------------------
echo Student Academic Risk Detection System - Launcher
echo ---------------------------------------------------
echo.

:: Step 1: Check if Python is installed at all
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed on this system, or it is not
    echo         added to PATH.
    echo.
    echo         Please install Python from https://www.python.org/downloads/
    echo         During installation, make sure to check the box that says
    echo         "Add Python to PATH", then run this file again.
    echo.
    pause
    exit /b 1
)

echo [OK] Python found.
python --version
echo.

:: Step 2: Check if Streamlit is installed; install requirements if not
echo Checking for required packages...
python -m streamlit --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [INFO] Some required packages are missing.
    echo        Installing dependencies from requirements.txt ...
    echo.
    if exist requirements.txt (
        pip install -r requirements.txt
    ) else (
        echo [WARNING] requirements.txt not found in this folder.
        echo            Installing default packages instead...
        pip install streamlit pandas scikit-learn plotly
    )
    echo.
) else (
    echo [OK] Streamlit is already installed.
    echo.
)

:: Step 3: Check that required project files exist before launching
if not exist code.py (
    echo [ERROR] code.py not found in this folder.
    echo         Make sure all project files were extracted into the
    echo         SAME folder before running this launcher.
    echo.
    pause
    exit /b 1
)

if not exist Studentdata.csv (
    echo [ERROR] Studentdata.csv not found in this folder.
    echo         Make sure all project files were extracted into the
    echo         SAME folder before running this launcher.
    echo.
    pause
    exit /b 1
)

echo All checks passed. Launching dashboard...
echo ---------------------------------------------------
echo.

:: Step 4: Run the application
python -m streamlit run code.py

pause
