#!/bin/bash

# rsync_retry.sh - Robust rsync with automatic retry for flaky connections
# =========================================================================
# Use this when transferring large data over unreliable VPNs or long-distance connections.
# Automatically resumes interrupted transfers and retries on failure.
#
# Usage:
#   rsync_retry.sh SOURCE DESTINATION [MAX_RETRIES] [RETRY_DELAY]
#
# Examples:
#   rsync_retry.sh mydata/ user@server:/scratch/transfer/
#   rsync_retry.sh mydata/ user@server:/scratch/transfer/ 20 30
#
# Flags used:
#   -r  recursive
#   -v  verbose
#   -z  compress during transfer
#   -P  --partial --progress (keep partial files, show progress)
#   -t  preserve modification times
#   --timeout  detect stalled connections

set -u

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Default values
MAX_RETRIES=${3:-100}      # Default: retry up to 100 times
RETRY_DELAY=${4:-10}       # Default: wait 10 seconds between retries
TIMEOUT=60                 # Detect stalled connections after 60 seconds

# Validate arguments
if [ $# -lt 2 ]; then
    echo -e "${RED}Usage: $0 SOURCE DESTINATION [MAX_RETRIES] [RETRY_DELAY]${NC}"
    echo ""
    echo "Examples:"
    echo "  $0 mydata/ user@server:/path/"
    echo "  $0 mydata/ user@server:/path/ 50 15"
    exit 1
fi

SOURCE="$1"
DESTINATION="$2"

# Check source exists
if [ ! -e "$SOURCE" ]; then
    echo -e "${RED}Error: Source does not exist: $SOURCE${NC}"
    exit 1
fi

echo -e "${GREEN}Starting rsync with auto-retry${NC}"
echo "  Source:      $SOURCE"
echo "  Destination: $DESTINATION"
echo "  Max retries: $MAX_RETRIES"
echo "  Retry delay: ${RETRY_DELAY}s"
echo "  Timeout:     ${TIMEOUT}s"
echo ""

ATTEMPT=0

while [ $ATTEMPT -lt $MAX_RETRIES ]; do
    ATTEMPT=$((ATTEMPT + 1))

    echo -e "${YELLOW}[Attempt $ATTEMPT/$MAX_RETRIES]${NC} $(date '+%Y-%m-%d %H:%M:%S')"

    rsync -rvzPt --timeout=$TIMEOUT "$SOURCE" "$DESTINATION"

    EXIT_CODE=$?

    if [ $EXIT_CODE -eq 0 ]; then
        echo ""
        echo -e "${GREEN}Transfer completed successfully!${NC}"
        exit 0
    fi

    echo -e "${RED}Rsync failed (exit code: $EXIT_CODE)${NC}"

    if [ $ATTEMPT -lt $MAX_RETRIES ]; then
        echo "Retrying in ${RETRY_DELAY}s..."
        sleep $RETRY_DELAY
    fi
done

echo -e "${RED}Max retries ($MAX_RETRIES) exceeded. Transfer failed.${NC}"
exit 1
