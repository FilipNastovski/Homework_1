@echo off
echo Starting MSE Stock Scraper Setup...

:: Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Python is not installed! Please install Python 3.12 or later.
    exit /b 1
)

:: Check if virtual environment exists, create if it doesn't
if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
)

:: Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate

:: Install required dependencies
echo Installing dependencies please wait...
pip install -r requirements.txt

:: Run the main program
echo Starting the program...
python main.py

:: Deactivate virtual environment
call venv\Scripts\deactivate.bat

pause
