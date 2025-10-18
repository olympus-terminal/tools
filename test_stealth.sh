#!/bin/bash

echo "🥷 YouTube Stealth Downloader Test"
echo "===================================="

# Activate conda environment
source /home/drn2/miniconda3/bin/activate ytaudio

# Show help
echo -e "\n📘 Showing help and stealth modes:"
python yt_stealth_downloader.py --help

echo -e "\n📊 Checking current statistics:"
python yt_stealth_downloader.py --stats

echo -e "\n✅ Test complete!"
echo ""
echo "🥷 STEALTH MODE RECOMMENDATIONS:"
echo "================================="
echo ""
echo "For maximum safety, use ONE of these approaches:"
echo ""
echo "1️⃣  PARANOID MODE (Safest - 30min to 2hr between downloads):"
echo '   python yt_stealth_downloader.py "CHANNEL_URL" --stealth paranoid'
echo ""
echo "2️⃣  HIGH MODE (Recommended - 10-40min between downloads):"
echo '   python yt_stealth_downloader.py "CHANNEL_URL" --stealth high'
echo ""
echo "3️⃣  MEDIUM MODE (Balanced - 5-20min between downloads):"
echo '   python yt_stealth_downloader.py "CHANNEL_URL" --stealth medium'
echo ""
echo "4️⃣  CUSTOM TIMING (Set your own delays in seconds):"
echo '   python yt_stealth_downloader.py "CHANNEL_URL" --min-wait 1200 --max-wait 3600'
echo ""
echo "📌 FEATURES:"
echo "  • Downloads ONE video at a time"
echo "  • Random delays between each download"
echo "  • Human-like behavior simulation"
echo "  • Daily download limits"
echo "  • Automatic resume capability"
echo "  • Time-of-day restrictions (avoids suspicious hours)"
echo "  • Random user-agent rotation"
echo "  • Slower download speeds to avoid detection"
echo ""
echo "💡 TIPS:"
echo "  • Start with --limit 1 to test"
echo "  • Use 'paranoid' mode for valuable channels"
echo "  • Create a .stop file in downloads/ to pause safely"
echo "  • Downloads auto-resume where you left off"
echo ""