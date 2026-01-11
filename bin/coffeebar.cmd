@echo off
REM CoffeeBar Wrapper for CMD
REM Enables environment refresh via Chocolatey's RefreshEnv if available

setlocal
REM Get the project root directory (one level up from bin)
set "PROJECT_ROOT=%~dp0.."
pushd "%PROJECT_ROOT%"

REM Run the Python application
python -m src.main %*
set PYTHON_EXIT_CODE=%ERRORLEVEL%

popd

REM Check if the command was "use" and Python succeeded
if "%1"=="use" (
    if %PYTHON_EXIT_CODE% equ 0 (
        REM Check for Chocolatey's RefreshEnv
        where refreshenv >nul 2>nul
        if %ERRORLEVEL% equ 0 (
            echo.
            echo [CoffeeBar] Chocolatey detected. Refreshing environment...
            call refreshenv
        ) else (
            echo.
            echo [CoffeeBar] Note: 'refreshenv' not found. Please restart your terminal to apply changes.
        )
    )
)

exit /b %PYTHON_EXIT_CODE%
