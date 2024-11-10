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

:: Clear existing packages (optional, uncomment if needed)
:: pip uninstall -y -r requirements.txt

:: Install each package individually with confirmation
echo Installing pandas...
pip install pandas
if errorlevel 1 (
    echo Failed to install pandas!
    pause
    exit /b 1
)

echo Installing selenium...
pip install selenium
if errorlevel 1 (
    echo Failed to install selenium!
    pause
    exit /b 1
)

echo Installing webdriver-manager...
pip install webdriver-manager
if errorlevel 1 (
    echo Failed to install webdriver-manager!
    pause
    exit /b 1
)

:: Verify installations
echo.
echo Verifying installations...
echo.
pip list | findstr "pandas"
pip list | findstr "selenium"
pip list | findstr "webdriver-manager"

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
deactivate

pause