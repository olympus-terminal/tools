#!/bin/bash

echo "YouTube Channel Downloader Test Script"
echo "======================================"

# Activate conda environment
source /home/drn2/miniconda3/bin/activate ytaudio

# Test 1: Show help
echo -e "\n📘 Test 1: Showing help for basic downloader"
python yt_channel_downloader.py --help

echo -e "\n📘 Test 2: Showing help for advanced downloader"
python yt_channel_advanced.py --help

# Test 3: Show progress (if any previous downloads exist)
echo -e "\n📊 Test 3: Checking download progress"
python yt_channel_downloader.py --show-progress

echo -e "\n✅ Test complete!"
echo "To download a channel, use one of these commands:"
echo ""
echo "Basic version (recommended for most users):"
echo '  python yt_channel_downloader.py "https://www.youtube.com/@channelname"'
echo ""
echo "Advanced version (with more anti-detection features):"
echo '  python yt_channel_advanced.py "https://www.youtube.com/@channelname"'
echo ""
echo "With custom delays (in seconds):"
echo '  python yt_channel_downloader.py "URL" --min-delay 60 --max-delay 180'
echo ""
echo "Download only first 10 videos:"
echo '  python yt_channel_downloader.py "URL" --limit 10'
echo ""
echo "Resume failed downloads:"
echo '  python yt_channel_downloader.py --retry-failed'