@echo off
setlocal enabledelayedexpansion

:: ------------------------------------------------------------
:: Supply Chain Analytics Platform - Single Run Setup Script
:: ------------------------------------------------------------

echo ============================================================
echo   Setting up Supply Chain Analytics Development Environment
echo ============================================================
echo.

rem Ensure we are running from the repository root
pushd "%~dp0"

:: ------------------------------------------------------------
:: 1. Backend Setup: Virtual Environment & Python Dependencies
:: ------------------------------------------------------------
echo --- 1/3 Backend Setup: Python Virtual Environment ---

rem Check if uv is installed
where uv >nul 2>&1
if %errorlevel% equ 0 (
    echo [INFO] 'uv' package manager detected. Using 'uv' for ultra-fast setup.
    
    if not exist ".venv" (
        echo Creating virtual environment with 'uv venv'...
        uv venv
        if !errorlevel! neq 0 (
            echo [ERROR] Failed to create virtual environment with 'uv'.
            popd
            exit /b 1
        )
    ) else (
        echo Virtual environment '.venv' already exists.
    )
    
    echo Activating virtual environment...
    call .venv\Scripts\activate.bat
    
    echo Installing backend dependencies with 'uv pip'...
    uv pip install -r requirements.txt
    if !errorlevel! neq 0 (
        echo [ERROR] Failed to install Python dependencies.
        popd
        exit /b 1
    )
) else (
    echo [INFO] 'uv' not detected. Falling back to standard Python.
    
    rem Check if python is installed
    where python >nul 2>&1
    if %errorlevel% neq 0 (
        echo [ERROR] Python is not installed or not in PATH.
        echo Please install Python 3.10+ and try again.
        popd
        exit /b 1
    )
    
    if not exist ".venv" (
        echo Creating virtual environment with 'python -m venv'...
        python -m venv .venv
        if !errorlevel! neq 0 (
            echo [ERROR] Failed to create virtual environment.
            popd
            exit /b 1
        )
    ) else (
        echo Virtual environment '.venv' already exists.
    )
    
    echo Activating virtual environment...
    call .venv\Scripts\activate.bat
    
    echo Upgrading pip...
    python -m pip install --upgrade pip
    
    echo Installing backend dependencies with pip...
    pip install -r requirements.txt
    if !errorlevel! neq 0 (
        echo [ERROR] Failed to install Python dependencies.
        popd
        exit /b 1
    )
)

echo [SUCCESS] Backend dependencies installed successfully.
echo.

:: ------------------------------------------------------------
:: 2. Frontend Setup: Node/npm Dependencies
:: ------------------------------------------------------------
echo --- 2/3 Frontend Setup: Node Packages ---

if exist "frontend\package.json" (
    where npm >nul 2>&1
    if %errorlevel% equ 0 (
        echo Node.js/npm detected. Installing frontend packages...
        pushd frontend
        call npm install
        if !errorlevel! neq 0 (
            echo [WARNING] Frontend dependency installation failed.
            echo You may need to run 'npm install' inside the frontend directory manually.
        ) else (
            echo [SUCCESS] Frontend dependencies installed successfully.
        )
        popd
    ) else (
        echo [WARNING] npm/Node.js not detected. Skipping frontend dependencies installation.
        echo Please install Node.js (which includes npm) to run the frontend app.
    )
) else (
    echo [INFO] No frontend/package.json found. Skipping frontend setup.
)
echo.

:: ------------------------------------------------------------
:: 3. Git Hooks Setup
:: ------------------------------------------------------------
echo --- 3/3 Git Hooks Setup ---

if exist "setup-hooks.cmd" (
    echo Running setup-hooks.cmd to configure Git hooks...
    call setup-hooks.cmd
    if !errorlevel! neq 0 (
        echo [WARNING] Git hooks setup returned a non-zero exit code.
    )
) else (
    echo [ERROR] setup-hooks.cmd not found in the root directory.
)
echo.

echo ============================================================
echo   Setup Complete!
echo   To start coding:
echo   1. Activate the environment: call .venv\Scripts\activate
echo   2. Run backend/tests or frontend server as needed.
echo ============================================================

popd
exit /b 0
