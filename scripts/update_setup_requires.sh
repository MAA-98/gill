#!/bin/zsh

REQ_FILE="src/requirements.txt"
SETUP_FILE="setup.py"

if [[ ! -f "$REQ_FILE" ]]; then
  echo "Error: $REQ_FILE not found!"
  exit 1
fi

# Read non-empty, non-comment lines from requirements.txt into a Python list string
REQS="["
while read -r line; do
  # Skip empty lines and comments
  if [[ -z "$line" ]] || [[ "$line" == \#* ]]; then
    continue
  fi
  REQS+="\"$line\", "
done < "$REQ_FILE"

# Remove trailing comma and space, close bracket
REQS="${REQS%, }]"
# Backup setup.py
cp "$SETUP_FILE" "${SETUP_FILE}.bak"

# Replace install_requires=[...] with new list (assuming single-line install_requires)
sed -i '' -E "s/install_requires=\[.*\]/install_requires=$REQS/" "$SETUP_FILE"

echo "Updated install_requires in $SETUP_FILE with contents of $REQ_FILE"
