@echo off
title Social Media Script Generator

echo.
echo  ============================================================
echo   Social Media Script Generator
echo  ============================================================
echo.

:: Move to the folder where this bat file lives
cd /d "%~dp0"

:: ── Check Python is installed ──────────────────────────────────────────────
python --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo  Python is not installed on this computer.
    echo.
    echo  Here is what to do:
    echo  1. Open your browser and go to:  https://www.python.org/downloads/
    echo  2. Download the latest version and run the installer
    echo  3. IMPORTANT: tick "Add Python to PATH" before clicking Install
    echo  4. Once done, close this window and double-click START HERE.vbs again
    echo.
    pause
    exit /b 1
)

echo  Python found. Checking version...

:: ── Check Python version is 3.9 or newer (simple approach) ────────────────
python -c "import sys; exit(0 if sys.version_info >= (3,9) else 1)" >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo  Your Python version is too old.
    echo.
    echo  Please download Python 3.11 or newer from:
    echo  https://www.python.org/downloads/
    echo  Then close this window and double-click START HERE.vbs again.
    echo.
    pause
    exit /b 1
)

echo  Python version OK.
echo.

:: ── Install / update dependencies ─────────────────────────────────────────
echo  Installing required components...
echo  This takes about 1-2 minutes the first time. Please wait.
echo.

python -m pip install --upgrade pip --quiet --disable-pip-version-check 2>nul
python -m pip install -r requirements.txt --quiet --disable-pip-version-check 2>nul

echo  Components ready.
echo.

:: ── Launch the app ─────────────────────────────────────────────────────────
echo  Opening the app in your browser...
echo  If the browser does not open, go to:  http://localhost:8501
echo.
echo  To stop the app, close this window.
echo  ============================================================
echo.

python -m streamlit run streamlit_app.py --server.headless false --browser.gatherUsageStats false --server.port 8501

echo.
echo  The app stopped.
echo  Close this window or double-click START HERE.vbs to restart.
echo.
pause
