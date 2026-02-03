#!/bin/bash
# scripts/log-issue.sh

TYPE=$1
TITLE=$2
DESCRIPTION=$3

FILE="docs/issues-and-enhancements.md"

if [ ! -f "$FILE" ]; then
    echo "# Issues and Enhancements" > "$FILE"
    echo "" >> "$FILE"
    echo "## Active Issues" >> "$FILE"
    echo "" >> "$FILE"
    echo "## Active Enhancements" >> "$FILE"
fi

# Find last ID
LAST_ID=$(grep -oE "ISS-[0-9]+" "$FILE" | grep -oE "[0-9]+" | sort -n | tail -1)
if [ -z "$LAST_ID" ]; then
    NEXT_ID=1
else
    NEXT_ID=$((LAST_ID + 1))
fi

ID_STR=$(printf "ISS-%03d" $NEXT_ID)

# Insert after "## Active Issues"
sed -i '' "/## Active Issues/a \\
- [ ] **$ID_STR**: $TITLE - $DESCRIPTION" "$FILE"

echo "✅ Logged Issue: $ID_STR"
