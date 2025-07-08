#!/bin/bash

# Check if venv is active (optional)
if [ -z "$VIRTUAL_ENV" ]; then
    echo "Warning: Virtual environment is not active."
    echo "Continuing but it's recommended to activate it first."
fi

echo "Updating requirements.txt with currently installed packages..."
pip freeze > requirements.txt
echo "requirements.txt updated."