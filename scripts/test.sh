#!/bin/zsh

# Activate virtual environment for testing
if [ -f "./test-env/bin/activate" ]; then
    source ./test-env/bin/activate
else 
    echo "Virtual environment activate script not found at ./test-env/bin/activate"
    return 1
fi

# Upgrade pip just in case
pip3 install --upgrade pip

# Install or reinstall gill from TestPyPI without cache
pip3 install --force-reinstall --no-cache-dir --extra-index-url https://test.pypi.org/simple/ gill

echo "Installation complete. You can now run 'gill' CLI."
