#!/usr/bin/env python3
import yt_dlp
import sys
from pathlib import Path

def download_audio(url, output_dir="downloads"):
    Path(output_dir).mkdir(exist_ok=True)
    
    # Download audio without conversion (keeping original format)
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': f'{output_dir}/%(title)s.%(ext)s',
    }
    
    print(f"Downloading from: {url}")
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        print(f"Downloaded: {info.get('title', 'Unknown')}")
        print(f"Note: Audio saved in original format. Install ffmpeg to convert to MP3.")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python yt_download_simple.py <youtube_url>")
        sys.exit(1)
    
    download_audio(sys.argv[1])