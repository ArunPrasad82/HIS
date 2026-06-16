@echo off
REM Installation script for Hospital Information System (Windows)

echo.
echo =========================================
echo Hospital Information System Setup
echo =========================================
echo.

REM Check Python version
echo Checking Python version...
python --version
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    exit /b 1
)

REM Create virtual environment
echo.
echo Creating virtual environment...
if not exist "venv" (
    python -m venv venv
    echo ^✓ Virtual environment created
) else (
    echo ^✓ Virtual environment already exists
)

REM Activate virtual environment
echo.
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Upgrade pip
echo.
echo Upgrading pip...
python -m pip install --upgrade pip

REM Install dependencies
echo.
echo Installing dependencies...
pip install -r requirements.txt
echo ^✓ Dependencies installed

REM Create necessary directories
echo.
echo Creating necessary directories...
if not exist "logs" mkdir logs
if not exist "uploads" mkdir uploads
if not exist "reports" mkdir reports
if not exist "backups" mkdir backups
echo ^✓ Directories created

REM Run migrations
echo.
echo Running database migrations...
echo.
python migrations\001_init_schema.py

REM Run seeding
echo.
echo Seeding initial data...
echo.
python migrations\002_seed_data.py

REM Configuration file creation
echo.
echo Creating configuration files...
if not exist ".env" (
    copy .env.example .env
    echo ^✓ .env file created (please update with your settings)
) else (
    echo ^✓ .env file already exists
)

echo.
echo =========================================
echo ^✓ Installation Complete!
echo =========================================
echo.
echo To start the application, run:
echo   venv\Scripts\activate.bat
echo   streamlit run app.py
echo.
echo Default Login Credentials:
echo   Username: admin
echo   Password: admin@123
echo.
echo Note: Change the default password after first login!
echo.
pause
