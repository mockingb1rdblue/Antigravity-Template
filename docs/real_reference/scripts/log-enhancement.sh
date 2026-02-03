#!/bin/bash
# scripts/log-enhancement.sh

TITLE=$1
DESCRIPTION=$2

FILE="docs/issues-and-enhancements.md"

if [ ! -f "$FILE" ]; then
    echo "# Issues and Enhancements" > "$FILE"
    echo "" >> "$FILE"
    echo "## Active Issues" >> "$FILE"
    echo "" >> "$FILE"
    echo "## Active Enhancements" >> "$FILE"
fi

# Find last ID
LAST_ID=$(grep -oE "ENH-[0-9]+" "$FILE" | grep -oE "[0-9]+" | sort -n | tail -1)
if [ -z "$LAST_ID" ]; then
    NEXT_ID=1
else
    NEXT_ID=$((LAST_ID + 1))
fi

ID_STR=$(printf "ENH-%03d" $NEXT_ID)

# Insert after "## Active Enhancements"
sed -i '' "/## Active Enhancements/a \\
- [ ] **$ID_STR**: $TITLE - $DESCRIPTION" "$FILE"

echo "✅ Logged Enhancement: $ID_STR"
