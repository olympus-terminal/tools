#!/bin/bash
# This script recursively finds directories with names like "checkpoint-<number>"
# and deletes those that are not multiples of 1000.
#
# Usage:
#   ./delete_checkpoints.sh
#
# CAUTION: Verify your directories and backup as needed before running this script.

find . -type d -name "checkpoint-*" | while read -r dir; do
    base=$(basename "$dir")
    # Remove the "checkpoint-" prefix
    num=${base#checkpoint-}
    # Check that the extracted value is a valid integer
    if [[ "$num" =~ ^[0-9]+$ ]]; then
        if (( num % 1000 != 0 )); then
            echo "Deleting $dir (number: $num is not a multiple of 1000)"
            rm -rf "$dir"
        else
            echo "Keeping $dir (number: $num is a multiple of 1000)"
        fi
    else
        echo "Skipping $dir (extracted value '$num' is not an integer)"
    fi
done

