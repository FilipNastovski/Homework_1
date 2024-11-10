@echo off
REM Activate the virtual environment
call .\.venv\Scripts\activate.bat

REM Run the Python program
python main.py

REM Deactivate the virtual environment after the script ends
deactivate

timeout /t 1000
