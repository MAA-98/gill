#!/bin/zsh

# Source environment variables from .my_secrets for API KEY
if [ -f "${HOME}/.my_secrets" ]; then
  source "${HOME}/.my_secrets"
else
  echo "Error: ${HOME}/.my_secrets not found."
  return 1
fi

# Check for PYPI_API_KEY after sourcing .my_secrets
if [ -z "$PYPI_API_KEY" ]; then
  echo "Error: PYPI_API_KEY environment variable not set. Did you forget to add it to ~/.my_secrets?"
  return 1
fi

# Delete the old build file in home dir
rm -rf ./dist/*

# Path to your src directory and venv folder inside it
SRC_DIR="./src"
CLI_VENV="${SRC_DIR}/venv"  # adjust if your venv folder is named differently or located elsewhere
BUILD_VENV="./build-env"

# Activate the virtual environment
if [ -f "${CLI_VENV}/bin/activate" ]; then
  source "${CLI_VENV}/bin/activate"
else
  echo "Virtual environment activate script not found at ${CLI_VENV}/bin/activate"
  return 1
fi

echo "Updating requirements.txt in ${SRC_DIR}..."
pip3 freeze > "${SRC_DIR}/requirements.txt"
echo "requirements.txt updated."

# Deactivate venv after updating requirements
deactivate

# Run the script to update setup.py requires
if [ -x "./scripts/update_setup_requires.sh" ]; then
  echo "Running ./scripts/update_setup_requires.sh..."
  ./scripts/update_setup_requires.sh
  echo "Finished updating setup.py."
else
  echo "Error: ./scripts/update_setup_requires.sh not found or not executable."
  return 1
fi

# Activate build-env for building the package
if [ -f "${BUILD_VENV}/bin/activate" ]; then
  source "${BUILD_VENV}/bin/activate"
else
  echo "Virtual environment activate script not found at ${BUILD_VENV}/bin/activate"
  return 1
fi

echo "Building the package..."
python3 -m build

echo "Uploading package to TestPyPI..."
twine upload --repository testpypi dist/* -u __token__ -p "$PYPI_API_KEY"

# Deactivate build-env venv
deactivate

echo "Upload complete!"
