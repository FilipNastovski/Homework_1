#!/bin/bash

# Activate the virtual environment
source ./.venv/bin/activate

# Run the Python program
python main.py

# Deactivate the virtual environment after the script ends
deactivate

# Keep the terminal open
echo "Press Enter to close..."