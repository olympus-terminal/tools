# YouTube Audio Downloader

A simple Python tool to download audio from YouTube videos for personal/educational use.

## Installation

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

2. Install FFmpeg (required for audio conversion):
- Ubuntu/Debian: `sudo apt install ffmpeg`
- MacOS: `brew install ffmpeg`
- Windows: Download from [ffmpeg.org](https://ffmpeg.org/download.html)

## Usage

Basic usage:
```bash
python yt_audio_downloader.py "https://www.youtube.com/watch?v=VIDEO_ID"
```

Options:
- `-o, --output`: Output directory (default: downloads)
- `-f, --format`: Audio format: mp3, wav, aac, opus, flac (default: mp3)
- `-q, --quality`: Audio quality in kbps (default: 192)
- `-n, --name`: Custom filename (without extension)

Examples:
```bash
# Download as MP3 with default settings
python yt_audio_downloader.py "https://www.youtube.com/watch?v=VIDEO_ID"

# Download as FLAC with custom name
python yt_audio_downloader.py "https://www.youtube.com/watch?v=VIDEO_ID" -f flac -n "my_audio"

# Download to specific folder with high quality
python yt_audio_downloader.py "https://www.youtube.com/watch?v=VIDEO_ID" -o my_music -q 320
```

## Legal Notice

This tool is for personal/educational use only. Respect copyright laws and YouTube's Terms of Service. Only download content you have permission to download.