#!/usr/bin/env python3
import yt_dlp
import os
import sys
import argparse
from pathlib import Path


class YTAudioDownloader:
    def __init__(self, output_dir="downloads", audio_format="mp3", quality="192"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.audio_format = audio_format
        self.quality = quality
        
    def download_audio(self, url, custom_filename=None):
        """Download audio from YouTube video"""
        
        # Configure yt-dlp options
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': self.audio_format,
                'preferredquality': self.quality,
            }],
            'outtmpl': str(self.output_dir / '%(title)s.%(ext)s'),
            'quiet': False,
            'no_warnings': False,
            'progress_hooks': [self._progress_hook],
        }
        
        if custom_filename:
            ydl_opts['outtmpl'] = str(self.output_dir / f'{custom_filename}.%(ext)s')
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                print(f"Downloading audio from: {url}")
                info = ydl.extract_info(url, download=True)
                title = info.get('title', 'Unknown')
                print(f"\n✓ Successfully downloaded: {title}")
                return True
        except Exception as e:
            print(f"\n✗ Error downloading audio: {str(e)}")
            return False
    
    def _progress_hook(self, d):
        """Display download progress"""
        if d['status'] == 'downloading':
            percent = d.get('_percent_str', 'N/A')
            speed = d.get('_speed_str', 'N/A')
            print(f"\rDownloading: {percent} at {speed}", end='', flush=True)
        elif d['status'] == 'finished':
            print("\nConverting to audio format...")


def main():
    parser = argparse.ArgumentParser(description='Download audio from YouTube videos')
    parser.add_argument('url', help='YouTube video URL')
    parser.add_argument('-o', '--output', default='downloads', help='Output directory (default: downloads)')
    parser.add_argument('-f', '--format', default='mp3', choices=['mp3', 'wav', 'aac', 'opus', 'flac'], 
                        help='Audio format (default: mp3)')
    parser.add_argument('-q', '--quality', default='192', 
                        help='Audio quality in kbps (default: 192)')
    parser.add_argument('-n', '--name', help='Custom filename (without extension)')
    
    args = parser.parse_args()
    
    downloader = YTAudioDownloader(
        output_dir=args.output,
        audio_format=args.format,
        quality=args.quality
    )
    
    success = downloader.download_audio(args.url, args.name)
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()