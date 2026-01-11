@echo off
echo [CoffeeBar] Installer
echo =====================
echo.

REM Check for Python
python --version >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo [Error] Python 3 is not installed or not in PATH.
    echo Please install Python 3 and try again.
    pause
    exit /b 1
)

echo [1/3] Installing dependencies...
pip install -r requirements.txt
if %ERRORLEVEL% neq 0 (
    echo [Error] Failed to install dependencies.
    pause
    exit /b 1
)

echo.
echo [2/3] Adding CoffeeBar to PATH...
python -m coffeebar.main add-to-path

echo.
echo =====================
echo [3/3] Installation Complete!
echo.
echo Please RESTART your terminal (close and open again).
echo.
echo You can now use the "coffeebar" command:
echo    coffeebar list
echo    coffeebar install 17
echo    coffeebar use 17
echo.
pause
