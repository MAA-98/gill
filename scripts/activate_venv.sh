#!/bin/bash

# NOTE: You have to call the script using ```source ./scripts/activate_venv.sh```

# Check if venv directory exists
if [ -d "venv" ]; then
    echo "Activating virtual environment..."
    source venv/bin/activate
else
    echo "No virtual environment found. Please create one first with:"
    echo "python3 -m venv venv"
fi