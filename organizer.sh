#!/bin/bash

ARCHIVE_DIR="archive"
LOG_FILE="organizer.log"
ORIGINAL="grades.csv"

# 1. Create the archive directory if it does not exist
if [ ! -d "$ARCHIVE_DIR" ]; then
    mkdir "$ARCHIVE_DIR"
fi

# 2. Make sure there is a grades.csv to archive
if [ ! -f "$ORIGINAL" ]; then
    echo "Error: $ORIGINAL not found in the current directory."
    exit 1
fi

# 3. Rename with timestamp and move into the archive
TIMESTAMP=$(date +%Y%m%d-%H%M%S)
ARCHIVED_NAME="grades_${TIMESTAMP}.csv"
# Avoid overwriting an archive created in the same second
COUNT=1
while [ -e "$ARCHIVE_DIR/$ARCHIVED_NAME" ]; do
    ARCHIVED_NAME="grades_${TIMESTAMP}_${COUNT}.csv"
    COUNT=$((COUNT + 1))
done
mv "$ORIGINAL" "$ARCHIVE_DIR/$ARCHIVED_NAME"

# 4. Workspace reset: new empty grades.csv
touch "$ORIGINAL"

# 5. Append to the log (accumulates across runs)
echo "Timestamp: $TIMESTAMP | Original: $ORIGINAL | Archived: $ARCHIVE_DIR/$ARCHIVED_NAME" >> "$LOG_FILE"

echo "Archived $ORIGINAL as $ARCHIVE_DIR/$ARCHIVED_NAME"
