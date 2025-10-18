#!/usr/bin/env python3
import yt_dlp
import sys
import os
from pathlib import Path

def download_audio(url, output_dir="downloads"):
    Path(output_dir).mkdir(exist_ok=True)
    
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': f'{output_dir}/%(title)s.%(ext)s',
        'ffmpeg_location': '/home/drn2/miniconda3/envs/ytaudio/bin',
        'cookiesfrombrowser': ('firefox',),
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python yt_download.py <youtube_url>")
        sys.exit(1)
    
    download_audio(sys.argv[1])