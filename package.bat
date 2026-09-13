@echo off
title Pistelle AI - Package Builder
cd /d "%~dp0"

echo.
echo  ============================================================
echo   Pistelle AI  ^|  Package Builder
echo   This creates a clean zip ready to upload to Super Profile
echo  ============================================================
echo.

:: Check Node/npm is available
where npm >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo  ERROR: npm not found. Please install Node.js from nodejs.org
    pause
    exit /b 1
)

:: Build the React frontend
echo  Step 1/2: Building the React frontend...
cd frontend
call npm run build
if %ERRORLEVEL% NEQ 0 (
    echo  ERROR: Frontend build failed. See error above.
    pause
    exit /b 1
)
cd ..
echo  Frontend built successfully.
echo.

:: Create the zip (excluding dev files)
echo  Step 2/2: Creating distribution zip...

:: Check PowerShell compress is available
powershell -Command "$src = Get-Location; $dest = Join-Path $src 'Pistelle_AI.zip'; if (Test-Path $dest) { Remove-Item $dest }; $exclude = @('.git', 'node_modules', '.env', 'venv', '__pycache__', '.python-version', 'package.bat'); $items = Get-ChildItem -Path $src | Where-Object { $exclude -notcontains $_.Name }; Compress-Archive -Path $items.FullName -DestinationPath $dest -Force; Write-Host 'Zip created: ' + $dest"

echo.
echo  ============================================================
echo   Done! Pistelle_AI.zip is ready in this folder.
echo   Upload it to your Super Profile product listing.
echo  ============================================================
echo.
pause
