@echo off
REM CrimeTrake Quick Start Script for Windows

echo ========================================
echo CrimeTrake Quick Start Script
echo ========================================
echo.

REM Check Python installation
python --version >nul 2>&1
if errorlevel 1 (
    echo Python is not installed or not in PATH
    echo Please install Python 3.10 or higher
    pause
    exit /b 1
)

echo Python found!
python --version
echo.

REM Create virtual environment
echo Creating virtual environment...
python -m venv venv

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo Installing dependencies...
python -m pip install --upgrade pip
pip install Django==4.2.7 pillow==10.1.0 scikit-learn==1.3.2 pandas==2.1.3 numpy==1.26.2

echo.
echo Note: Face recognition packages are optional
echo The app will work without them
echo.

REM Create .env file
if not exist .env (
    echo Creating .env file...
    copy .env.example .env
    echo Please edit .env file with your settings
)

REM Run migrations
echo Setting up database...
python manage.py makemigrations
python manage.py migrate

REM Create superuser
echo.
echo Create admin account:
python manage.py createsuperuser

REM Collect static files
echo.
echo Collecting static files...
python manage.py collectstatic --noinput

echo.
echo ========================================
echo Setup complete!
echo ========================================
echo.
echo To start the server:
echo    python manage.py runserver
echo.
echo Access at:
echo    Frontend: http://localhost:8000
echo    Admin: http://localhost:8000/admin
echo.
echo Read README.md and SETUP.md for more info
echo.
pause
