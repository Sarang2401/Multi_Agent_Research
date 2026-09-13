@echo off
title Pistelle AI

echo.
echo  ============================================================
echo   Pistelle AI  ^|  Content Intelligence Suite
echo  ============================================================
echo.

:: Move to the folder where this bat file lives
cd /d "%~dp0"

:: ── Check Python is installed ─────────────────────────────────────────────────
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

python -c "import sys; exit(0 if sys.version_info >= (3,9) else 1)" >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo  Your Python version is too old. Please download Python 3.11 or newer from:
    echo  https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)

echo  Python found.  Checking dependencies...
echo.

:: ── Install / update Python dependencies ─────────────────────────────────────
python -m pip install --upgrade pip --quiet --disable-pip-version-check 2>nul
python -m pip install -r requirements.txt --quiet --disable-pip-version-check 2>nul

echo  Dependencies ready.
echo.

:: ── Open the browser after a short delay, then start the server ───────────────
echo  Opening Pistelle AI in your browser...
echo.
echo  App address:  http://localhost:8000
echo.
echo  ============================================================
echo  To stop the app, close this window.
echo  ============================================================
echo.

:: Open browser after 2 seconds (gives server time to start)
start "" /b cmd /c "timeout /t 2 /nobreak >nul && start http://localhost:8000"

:: Start the FastAPI server (this runs in the foreground, keeping the window alive)
python -m uvicorn api:app --host 127.0.0.1 --port 8000

echo.
echo  The app has stopped.
echo  Close this window or double-click START HERE.vbs to restart.
echo.
pause
