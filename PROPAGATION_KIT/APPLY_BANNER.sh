#!/bin/bash
# Quick script to apply status banner to a repo README
# Usage: ./APPLY_BANNER.sh <repo_path> <status> <purpose> <not_for>

REPO_PATH="$1"
STATUS="$2"
PURPOSE="$3"
NOT_FOR="$4"

if [ -z "$REPO_PATH" ] || [ -z "$STATUS" ] || [ -z "$PURPOSE" ] || [ -z "$NOT_FOR" ]; then
    echo "Usage: $0 <repo_path> <status> <purpose> <not_for>"
    echo "Example: $0 ~/Projects/ZoraAPI 'Active' 'API library for Zora' 'Core theory development'"
    exit 1
fi

README="$REPO_PATH/README.md"

if [ ! -f "$README" ]; then
    echo "README.md not found at $README"
    exit 1
fi

BANNER="> **Status:** $STATUS  
> **Canonical Repository:** [MQGT-SCF](https://github.com/Cbaird26/MQGT-SCF)  
> **Purpose:** $PURPOSE  
> **Not for:** $NOT_FOR

---

"

# Check if banner already exists
if grep -q "Status:" "$README"; then
    echo "Banner already exists in $README"
    exit 0
fi

# Create backup
cp "$README" "$README.bak"

# Prepend banner
echo -e "$BANNER$(cat "$README")" > "$README"

echo "Banner applied to $README"
echo "Backup saved to $README.bak"

