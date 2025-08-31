#!/usr/bin/env python3
"""
YouTube to MP3 Downloader
Downloads audio from YouTube videos and converts to MP3 format
"""
import yt_dlp
import sys
import os
from pathlib import Path
import argparse
from cookie_manager import CookieManager


class YouTubeMP3Downloader:
    def __init__(self, output_dir="downloads", quality="192", use_cookies=True):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.quality = quality
        self.ffmpeg_path = '/home/drn2/miniconda3/envs/ytaudio/bin'
        self.use_cookies = use_cookies
        self.cookie_manager = CookieManager() if use_cookies else None
        
    def download(self, url, custom_name=None):
        """Download audio from YouTube and convert to MP3"""
        
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': self.quality,
            }],
            'outtmpl': str(self.output_dir / '%(title)s.%(ext)s'),
            'ffmpeg_location': self.ffmpeg_path,
            'quiet': False,
            'no_warnings': False,
            'progress_hooks': [self._progress_hook],
        }
        
        # Add cookie options
        if self.use_cookies and self.cookie_manager:
            ydl_opts = self.cookie_manager.get_yt_dlp_opts(ydl_opts)
        
        if custom_name:
            ydl_opts['outtmpl'] = str(self.output_dir / f'{custom_name}.%(ext)s')
        
        try:
            print(f"🎵 Downloading from: {url}")
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                title = info.get('title', 'Unknown')
                print(f"\n✅ Successfully downloaded: {title}")
                return True
        except Exception as e:
            print(f"\n❌ Error: {str(e)}")
            return False
    
    def _progress_hook(self, d):
        if d['status'] == 'downloading':
            percent = d.get('_percent_str', 'N/A')
            speed = d.get('_speed_str', 'N/A')
            print(f"\r📥 Downloading: {percent} at {speed}", end='', flush=True)
        elif d['status'] == 'finished':
            print("\n🔄 Converting to MP3...")


def main():
    parser = argparse.ArgumentParser(
        description='Download YouTube videos as MP3 files',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s "https://www.youtube.com/watch?v=VIDEO_ID"
  %(prog)s "URL" -o music -q 320
  %(prog)s "URL" -n "My Song Name"
        """
    )
    
    parser.add_argument('url', help='YouTube video URL')
    parser.add_argument('-o', '--output', default='downloads', 
                        help='Output directory (default: downloads)')
    parser.add_argument('-q', '--quality', default='192', 
                        choices=['128', '192', '256', '320'],
                        help='Audio quality in kbps (default: 192)')
    parser.add_argument('-n', '--name', 
                        help='Custom filename (without extension)')
    parser.add_argument('--no-cookies', action='store_true',
                        help='Disable cookie usage')
    
    args = parser.parse_args()
    
    downloader = YouTubeMP3Downloader(
        output_dir=args.output,
        quality=args.quality,
        use_cookies=not args.no_cookies
    )
    
    success = downloader.download(args.url, args.name)
    sys.exit(0 if success else 1)


if __name__ == '__main__':
#!/usr/bin/env python3
"""
YouTube to MP3 Downloader
Downloads audio from YouTube videos and converts to MP3 format
"""
import yt_dlp
import sys
import os
from pathlib import Path
import argparse
from cookie_manager import CookieManager


class YouTubeMP3Downloader:
    def __init__(self, output_dir="downloads", quality="192", use_cookies=True):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.quality = quality
        self.ffmpeg_path = '/home/drn2/miniconda3/envs/ytaudio/bin'
        self.use_cookies = use_cookies
        self.cookie_manager = CookieManager() if use_cookies else None
        
    def download(self, url, custom_name=None):
        """Download audio from YouTube and convert to MP3"""
        
        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': self.quality,
            }],
            'outtmpl': str(self.output_dir / '%(title)s.%(ext)s'),
            'ffmpeg_location': self.ffmpeg_path,
            'quiet': False,
            'no_warnings': False,
            'progress_hooks': [self._progress_hook],
        }
        
        # Add cookie options
        if self.use_cookies and self.cookie_manager:
            ydl_opts = self.cookie_manager.get_yt_dlp_opts(ydl_opts)
        
        if custom_name:
            ydl_opts['outtmpl'] = str(self.output_dir / f'{custom_name}.%(ext)s')
        
        try:
            print(f"🎵 Downloading from: {url}")
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                title = info.get('title', 'Unknown')
                print(f"\n✅ Successfully downloaded: {title}")
                return True
        except Exception as e:
            print(f"\n❌ Error: {str(e)}")
            return False
    
    def _progress_hook(self, d):
        if d['status'] == 'downloading':
            percent = d.get('_percent_str', 'N/A')
            speed = d.get('_speed_str', 'N/A')
            print(f"\r📥 Downloading: {percent} at {speed}", end='', flush=True)
        elif d['status'] == 'finished':
            print("\n🔄 Converting to MP3...")


def main():
    parser = argparse.ArgumentParser(
        description='Download YouTube videos as MP3 files',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s "https://www.youtube.com/watch?v=VIDEO_ID"
  %(prog)s "URL" -o music -q 320
  %(prog)s "URL" -n "My Song Name"
        """
    )
    
    parser.add_argument('url', help='YouTube video URL')
    parser.add_argument('-o', '--output', default='downloads', 
                        help='Output directory (default: downloads)')
    parser.add_argument('-q', '--quality', default='192', 
                        choices=['128', '192', '256', '320'],
                        help='Audio quality in kbps (default: 192)')
    parser.add_argument('-n', '--name', 
                        help='Custom filename (without extension)')
    parser.add_argument('--no-cookies', action='store_true',
                        help='Disable cookie usage')
    
    args = parser.parse_args()
    
    downloader = YouTubeMP3Downloader(
        output_dir=args.output,
        quality=args.quality,
        use_cookies=not args.no_cookies
    )
    
    success = downloader.download(args.url, args.name)
    sys.exit(0 if success else 1)


if __name__ == '__main__':
