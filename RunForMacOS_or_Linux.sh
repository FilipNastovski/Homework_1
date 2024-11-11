#!/bin/bash

# Function to check for python version
check_python() {
    python3 --version > /dev/null 2>&1
    if [[ $? -ne 0 ]]; then
        echo "Python is not installed! Please install Python 3.12 or later."
        exit 1
    fi
}

# Check for Python 3.12 or later
check_python

# Check if virtual environment exists, create if it doesn't
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "Installing dependencies from requirements.txt..."
pip install --upgrade pip
pip install -r requirements.txt

# Verify installations
echo "Verifying installations..."
pip list | grep -E "pandas|selenium|beautifulsoup4|aiohttp"

# Run the main program
echo "Running the program..."
python main.py

# Deactivate virtual environment after program execution
deactivate

echo "Script finished. The virtual environment has been deactivated."
