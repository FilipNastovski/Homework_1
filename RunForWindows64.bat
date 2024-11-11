@echo off
echo Starting MSE Stock Scraper Setup...

:: Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Python is not installed! Please install Python 3.12 or later.
    pause
    exit /b 1
)

:: Check if virtual environment exists, create if it doesn't
if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
)

:: Activate virtual environment and show confirmation
echo Activating virtual environment...
call venv\Scripts\activate
echo Virtual environment activated!

:: Install packages from requirements.txt
echo Installing dependencies from requirements.txt...
pip install -r requirements.txt
if errorlevel 1 (
    echo Failed to install required packages!
    pause
    exit /b 1
)

:: Verify installations
echo.
echo Verifying installations...
echo.
pip list

:: Run the main program
echo.
echo Starting the program...
python main.py

:: Keep the window open if there's an error
if errorlevel 1 (
    echo An error occurred! Check the output above.
    pause
)

:: Deactivate virtual environment
call venv\Scripts\deactivate.bat

pause
