#!/bin/bash

# Start the setup process
echo "Starting MSE Stock Scraper Setup..."

# Check if Python is installed
python3 --version > /dev/null 2>&1
if [ $? -ne 0 ]; then
    echo "Python is not installed! Please install Python 3.12 or later."
    exit 1
fi

# Check if virtual environment directory exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate the virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install required dependencies
echo "Installing dependencies..."
pip install -r requirements.txt


# Run the main program
echo "Starting the program..."
python main.py

# Deactivate virtual environment
deactivate

# Keep the terminal open for any error output
echo "Script completed."
