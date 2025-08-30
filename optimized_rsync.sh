#!/bin/bash

# Optimized rsync for Large Scientific Data Transfers
# =====================================================
# Author: Your Name
# Purpose: Efficiently sync large datasets over long-distance SSH connections
# 
# This script addresses common bottlenecks when transferring large scientific datasets
# (genomics, ML models, HDF5 files, etc.) to remote HPC systems.
#
# Key optimizations:
# - TCP buffer tuning for high-latency connections
# - SSH cipher selection for better throughput
# - Compression options for different data types
# - Progress monitoring and resume capability

set -e

# Default values
DEFAULT_BUFFER_SIZE="524288"  # 512KB - good for most long-distance connections
DEFAULT_CIPHER="aes128-gcm@openssh.com"  # Fast, secure cipher
DEFAULT_COMPRESSION=true
DEFAULT_THREADS=4

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to display usage
usage() {
    cat << EOF
Usage: $0 [OPTIONS] SOURCE DESTINATION

Optimized rsync for large scientific data transfers over SSH.

Arguments:
    SOURCE          Source directory or file
    DESTINATION     Destination in format: [user@]host:/path

Options:
    -b SIZE         Buffer size in bytes (default: $DEFAULT_BUFFER_SIZE)
                    Common values:
                    - 262144  (256KB) for LAN transfers
                    - 524288  (512KB) for WAN transfers (default)
                    - 1048576 (1MB)   for very long distance
                    - 4194304 (4MB)   for intercontinental

    -c CIPHER       SSH cipher (default: $DEFAULT_CIPHER)
                    Fast options:
                    - aes128-gcm@openssh.com (recommended)
                    - aes128-ctr
                    - chacha20-poly1305@openssh.com

    -z              Enable compression (default: on for code, off for compressed data)
    -n              Disable compression
    
    -p              Preserve permissions and timestamps (adds -a flag)
    
    -e PATTERN      Exclude pattern (can be used multiple times)
                    Common excludes:
                    - "*.pyc" "*.pyo" "__pycache__"
                    - ".git" ".venv" "node_modules"
                    - "*.log" "wandb/"
    
    -t THREADS      Number of parallel threads (for rsync 3.2.0+)
    
    -d              Dry run - show what would be transferred
    
    -v              Verbose output
    
    -h              Show this help message

    --test-speed    Test connection speed before transfer
    --diagnose      Run network diagnostics

Examples:
    # Basic optimized transfer
    $0 ./my_data/ user@hpc.university.edu:/scratch/user/project/

    # Transfer with maximum optimization for intercontinental connection
    $0 -b 4194304 -c aes128-ctr ./large_dataset/ user@remote:/data/

    # Exclude unnecessary files and use dry run
    $0 -d -e "*.log" -e "wandb/" -e "__pycache__" ./project/ user@hpc:/home/user/

    # Transfer compressed data without additional compression
    $0 -n ./compressed_data.tar.gz user@server:/backups/

Network Tuning Tips:
    1. For connections with high latency (>50ms), increase buffer size
    2. For data that's already compressed (.h5, .tar.gz), disable compression with -n
    3. For many small files, compression (-z) helps significantly
    4. Monitor transfer with: iftop, nload, or bmon

Troubleshooting Slow Transfers:
    1. Run with --diagnose to check network path
    2. Try different ciphers (-c option)
    3. Adjust buffer sizes based on your connection
    4. Check if firewall/IDS is throttling SSH
    5. Consider using Globus or bbcp for extremely large datasets

EOF
    exit 0
}

# Function to test connection speed
test_speed() {
    local dest=$1
    print_info "Testing connection speed to $dest..."
    
    # Extract host from destination
    local host=$(echo $dest | cut -d: -f1)
    
    # Test ping
    print_info "Testing latency..."
    ping -c 5 $(echo $host | cut -d@ -f2) 2>/dev/null || print_warning "Ping failed (ICMP might be blocked)"
    
    # Test SSH speed
    print_info "Testing SSH throughput..."
    dd if=/dev/zero bs=1M count=10 2>/dev/null | ssh $host "cat > /dev/null" 2>&1 | grep -o "[0-9.]* [MG]B/s" || print_warning "SSH speed test failed"
}

# Function to run diagnostics
diagnose_connection() {
    local dest=$1
    local host=$(echo $dest | cut -d: -f1 | cut -d@ -f2)
    
    print_info "Running network diagnostics for $host..."
    
    # Check DNS
    print_info "DNS resolution:"
    nslookup $host 2>/dev/null | head -5 || host $host 2>/dev/null || print_warning "DNS lookup failed"
    
    # Check route
    print_info "Network path (first 10 hops):"
    traceroute -m 10 $host 2>/dev/null | head -15 || print_warning "Traceroute failed"
    
    # Check SSH ciphers
    print_info "Available SSH ciphers:"
    ssh -Q cipher 2>/dev/null | head -10 || print_warning "Cannot query SSH ciphers"
}

# Parse arguments
BUFFER_SIZE=$DEFAULT_BUFFER_SIZE
CIPHER=$DEFAULT_CIPHER
COMPRESSION="-z"
EXCLUDE_ARGS=""
DRY_RUN=""
VERBOSE=""
PRESERVE=""
THREADS=""
TEST_SPEED=false
DIAGNOSE=false

while [[ $# -gt 0 ]]; do
    case $1 in
        -b)
            BUFFER_SIZE="$2"
            shift 2
            ;;
        -c)
            CIPHER="$2"
            shift 2
            ;;
        -z)
            COMPRESSION="-z"
            shift
            ;;
        -n)
            COMPRESSION=""
            shift
            ;;
        -p)
            PRESERVE="-a"
            shift
            ;;
        -e)
            EXCLUDE_ARGS="$EXCLUDE_ARGS --exclude='$2'"
            shift 2
            ;;
        -t)
            # Only works with rsync 3.2.0+
            THREADS="--threads=$2"
            shift 2
            ;;
        -d)
            DRY_RUN="--dry-run"
            shift
            ;;
        -v)
            VERBOSE="-v"
            shift
            ;;
        --test-speed)
            TEST_SPEED=true
            shift
            ;;
        --diagnose)
            DIAGNOSE=true
            shift
            ;;
        -h|--help)
            usage
            ;;
        *)
            break
            ;;
    esac
done

# Check remaining arguments
if [ $# -lt 2 ]; then
    print_error "Missing required arguments"
    echo ""
    usage
fi

SOURCE="$1"
DESTINATION="$2"

# Validate source exists
if [ ! -e "$SOURCE" ]; then
    print_error "Source does not exist: $SOURCE"
    exit 1
fi

# Run diagnostics if requested
if [ "$DIAGNOSE" = true ]; then
    diagnose_connection "$DESTINATION"
    echo ""
fi

# Test speed if requested
if [ "$TEST_SPEED" = true ]; then
    test_speed "$DESTINATION"
    echo ""
fi

# Build rsync command
RSYNC_CMD="rsync"

# Basic flags
RSYNC_CMD="$RSYNC_CMD $PRESERVE $VERBOSE $COMPRESSION -P"

# Add socket options for TCP buffer tuning
RSYNC_CMD="$RSYNC_CMD --sockopts=SO_SNDBUF=$BUFFER_SIZE,SO_RCVBUF=$BUFFER_SIZE"

# Add SSH options
SSH_OPTS="-c $CIPHER"
if [ ! -z "$VERBOSE" ]; then
    SSH_OPTS="$SSH_OPTS -v"
fi
RSYNC_CMD="$RSYNC_CMD -e 'ssh $SSH_OPTS'"

# Add exclude patterns
if [ ! -z "$EXCLUDE_ARGS" ]; then
    RSYNC_CMD="$RSYNC_CMD $EXCLUDE_ARGS"
fi

# Add threading if specified
if [ ! -z "$THREADS" ]; then
    RSYNC_CMD="$RSYNC_CMD $THREADS"
fi

# Add dry run if specified
if [ ! -z "$DRY_RUN" ]; then
    RSYNC_CMD="$RSYNC_CMD $DRY_RUN"
fi

# Add source and destination
RSYNC_CMD="$RSYNC_CMD '$SOURCE' '$DESTINATION'"

# Display configuration
print_info "Configuration:"
echo "  Source:      $SOURCE"
echo "  Destination: $DESTINATION"
echo "  Buffer size: $BUFFER_SIZE bytes ($(($BUFFER_SIZE / 1024))KB)"
echo "  SSH cipher:  $CIPHER"
echo "  Compression: $([ ! -z "$COMPRESSION" ] && echo "Enabled" || echo "Disabled")"
[ ! -z "$DRY_RUN" ] && echo "  Mode:        DRY RUN (no files will be transferred)"
echo ""

# Show command
print_info "Executing command:"
echo "  $RSYNC_CMD"
echo ""

# Execute
if [ ! -z "$DRY_RUN" ]; then
    print_warning "DRY RUN MODE - No files will be transferred"
fi

eval $RSYNC_CMD

# Check exit status
if [ $? -eq 0 ]; then
    print_success "Transfer completed successfully!"
else
    print_error "Transfer failed with error code $?"
    exit $?
fi%                                                                                                                                                                                                                                                  (base) drn
