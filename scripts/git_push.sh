#!/bin/bash

# Check if a commit message was provided as an argument
if [ -z "$1" ]; then
    echo "Usage: $0 \"your commit message\""
    exit 1
fi

commit_message="$1"

echo "Adding all changes..."
git add .

echo "Committing with message: $commit_message"
git commit -m "$commit_message"

echo "Pushing changes..."
git push

echo "Done."