#!/bin/bash

# NOTE: You have to call the script using ```source ./scripts/activate_venv.sh``` for the environment change to persist.

# Check if venv directory exists
if [ -d "venv" ]; then
    echo "Activating virtual environment..."
    source venv/bin/activate
    
        # Check if activation succeeded
    if [ -n "$VIRTUAL_ENV" ] && [[ "$VIRTUAL_ENV" == *"venv"* ]]; then
        echo "Venv is active at $VIRTUAL_ENV"
    else
        echo "Failed to activate venv."
    fi
    
else
    echo "No virtual environment found. Please create one first with:"
    echo "python3 -m venv venv"
fi
