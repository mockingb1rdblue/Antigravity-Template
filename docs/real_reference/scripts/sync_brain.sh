#!/bin/bash

# Configuration
SOURCE_DIR="/Users/mock1ng/.gemini/antigravity/brain/"
DEST_DIR="$(pwd)/docs/brain/"

# Ensure destination exists
mkdir -p "$DEST_DIR"

# Check if source exists
if [ ! -d "$SOURCE_DIR" ]; then
    echo "Error: Source directory $SOURCE_DIR does not exist."
    exit 1
fi

echo "Syncing from $SOURCE_DIR to $DEST_DIR..."

# Sync using rsync
# -a: archive mode (preserves permissions, timestamps, etc.)
# -v: verbose
# (Note: --delete removed to allow for renamed folder organization)
rsync -av "$SOURCE_DIR" "$DEST_DIR"

echo "Sync complete. Organizing folders..."
python3 scripts/organize_brain.py
echo "Organization complete."
