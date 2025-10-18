#!/usr/bin/env python3
"""
YouTube Channel Downloader
Downloads all videos from a YouTube channel as MP3 files with rate limiting and anti-detection
"""
import yt_dlp
import sys
import os
import time
import random
import json
import argparse
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Set
from cookie_manager import CookieManager


class ChannelDownloader:
    def __init__(self,
                 output_dir: str = "downloads",
                 quality: str = "192",
                 min_delay: int = 30,
                 max_delay: int = 120,
                 use_cookies: bool = True,
                 max_retries: int = 3):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.quality = quality
        self.min_delay = min_delay
        self.max_delay = max_delay
        self.use_cookies = use_cookies
        self.max_retries = max_retries
        self.ffmpeg_path = '/home/drn2/miniconda3/envs/ytaudio/bin'
        self.cookie_manager = CookieManager() if use_cookies else None

        # Progress tracking
        self.progress_file = self.output_dir / ".channel_progress.json"
        self.progress_data = self._load_progress()

        # Statistics
        self.stats = {
            'downloaded': 0,
            'skipped': 0,
            'failed': 0,
            'total': 0
        }

    def _load_progress(self) -> Dict:
        """Load progress data from file"""
        if self.progress_file.exists():
            with open(self.progress_file, 'r') as f:
                return json.load(f)
        return {
            'downloaded_videos': {},
            'failed_videos': {},
            'channels': {}
        }

    def _save_progress(self):
        """Save progress data to file"""
        with open(self.progress_file, 'w') as f:
            json.dump(self.progress_data, f, indent=2)

    def _get_channel_id(self, url: str) -> Optional[str]:
        """Extract channel ID from URL"""
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'extract_flat': True,
        }

        if self.use_cookies and self.cookie_manager:
            ydl_opts = self.cookie_manager.get_yt_dlp_opts(ydl_opts)

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                return info.get('channel_id') or info.get('uploader_id')
        except Exception as e:
            print(f"❌ Error extracting channel ID: {e}")
            return None

    def _get_video_list(self, channel_url: str) -> List[Dict]:
        """Get list of all videos from a channel"""
        print("📋 Fetching channel video list...")

        ydl_opts = {
            'quiet': False,
            'no_warnings': False,
            'extract_flat': 'in_playlist',
            'playlistend': None,  # Get all videos
        }

        if self.use_cookies and self.cookie_manager:
            ydl_opts = self.cookie_manager.get_yt_dlp_opts(ydl_opts)

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(channel_url, download=False)

                if 'entries' not in info:
                    print("❌ No videos found in channel")
                    return []

                videos = []
                for entry in info['entries']:
                    if entry and 'id' in entry:
                        videos.append({
                            'id': entry['id'],
                            'title': entry.get('title', 'Unknown'),
                            'url': f"https://www.youtube.com/watch?v={entry['id']}",
                            'duration': entry.get('duration', 0)
                        })

                return videos
        except Exception as e:
            print(f"❌ Error fetching video list: {e}")
            return []

    def _download_video(self, video: Dict, channel_dir: Path) -> bool:
        """Download a single video as MP3"""
        video_id = video['id']

        # Check if already downloaded
        if video_id in self.progress_data['downloaded_videos']:
            print(f"⏭️  Skipping (already downloaded): {video['title']}")
            self.stats['skipped'] += 1
            return True

        # Check if failed too many times
        failed_count = self.progress_data['failed_videos'].get(video_id, {}).get('attempts', 0)
        if failed_count >= self.max_retries:
            print(f"⏭️  Skipping (max retries exceeded): {video['title']}")
            self.stats['skipped'] += 1
            return False

        ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': self.quality,
            }],
            'outtmpl': str(channel_dir / '%(title)s.%(ext)s'),
            'ffmpeg_location': self.ffmpeg_path,
            'quiet': False,
            'no_warnings': False,
            'progress_hooks': [self._progress_hook],
            'restrictfilenames': True,  # Use safe filenames
            'ignoreerrors': False,
            'no_color': False,
            'retries': 5,
            'fragment_retries': 5,
            'skip_unavailable_fragments': True,
        }

        # Add cookie options with rotation
        if self.use_cookies and self.cookie_manager:
            ydl_opts = self.cookie_manager.get_yt_dlp_opts(ydl_opts)

        try:
            print(f"\n🎵 Downloading [{self.stats['downloaded'] + 1}/{self.stats['total']}]: {video['title']}")
            print(f"   URL: {video['url']}")

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([video['url']])

            # Mark as downloaded
            self.progress_data['downloaded_videos'][video_id] = {
                'title': video['title'],
                'downloaded_at': datetime.now().isoformat(),
                'duration': video.get('duration', 0)
            }
            self._save_progress()

            print(f"✅ Successfully downloaded: {video['title']}")
            self.stats['downloaded'] += 1
            return True

        except Exception as e:
            print(f"❌ Error downloading {video['title']}: {str(e)}")

            # Track failed attempts
            if video_id not in self.progress_data['failed_videos']:
                self.progress_data['failed_videos'][video_id] = {
                    'title': video['title'],
                    'attempts': 0,
                    'last_error': '',
                    'last_attempt': ''
                }

            self.progress_data['failed_videos'][video_id]['attempts'] += 1
            self.progress_data['failed_videos'][video_id]['last_error'] = str(e)
            self.progress_data['failed_videos'][video_id]['last_attempt'] = datetime.now().isoformat()
            self._save_progress()

            self.stats['failed'] += 1
            return False

    def _progress_hook(self, d):
        """Progress callback for yt-dlp"""
        if d['status'] == 'downloading':
            percent = d.get('_percent_str', 'N/A')
            speed = d.get('_speed_str', 'N/A')
            eta = d.get('_eta_str', 'N/A')
            print(f"\r📥 Progress: {percent} | Speed: {speed} | ETA: {eta}", end='', flush=True)
        elif d['status'] == 'finished':
            print("\n🔄 Converting to MP3...")

    def _random_delay(self):
        """Add random delay between downloads"""
        delay = random.uniform(self.min_delay, self.max_delay)
        print(f"\n⏳ Waiting {delay:.1f} seconds before next download...")

        # Show countdown
        for remaining in range(int(delay), 0, -1):
            print(f"\r⏳ {remaining} seconds remaining...", end='', flush=True)
            time.sleep(1)
        print("\r" + " " * 50 + "\r", end='')  # Clear the line

    def download_channel(self, channel_url: str, limit: Optional[int] = None):
        """Download all videos from a YouTube channel"""
        print(f"🚀 Starting YouTube Channel Downloader")
        print(f"📁 Output directory: {self.output_dir}")
        print(f"🎵 Audio quality: {self.quality} kbps")
        print(f"⏱️  Delay range: {self.min_delay}-{self.max_delay} seconds")
        print("=" * 60)

        # Get channel ID
        channel_id = self._get_channel_id(channel_url)
        if not channel_id:
            print("❌ Could not identify channel")
            return False

        # Create channel directory
        channel_dir = self.output_dir / channel_id
        channel_dir.mkdir(exist_ok=True)

        # Get video list
        videos = self._get_video_list(channel_url)
        if not videos:
            print("❌ No videos found to download")
            return False

        # Apply limit if specified
        if limit:
            videos = videos[:limit]

        self.stats['total'] = len(videos)

        print(f"\n📊 Found {len(videos)} videos to process")
        print("=" * 60)

        # Update channel info in progress
        self.progress_data['channels'][channel_id] = {
            'url': channel_url,
            'total_videos': len(videos),
            'last_updated': datetime.now().isoformat()
        }
        self._save_progress()

        # Download each video
        for i, video in enumerate(videos):
            # Download video
            success = self._download_video(video, channel_dir)

            # Add delay between downloads (except for the last one)
            if i < len(videos) - 1:
                # Vary delay based on success/failure
                if not success:
                    # Longer delay after failure
                    self._random_delay()
                    time.sleep(random.uniform(10, 30))  # Extra delay after error
                else:
                    self._random_delay()

        # Print summary
        print("\n" + "=" * 60)
        print("📈 Download Summary:")
        print(f"   ✅ Downloaded: {self.stats['downloaded']}")
        print(f"   ⏭️  Skipped: {self.stats['skipped']}")
        print(f"   ❌ Failed: {self.stats['failed']}")
        print(f"   📊 Total: {self.stats['total']}")
        print("=" * 60)

        return self.stats['failed'] == 0

    def retry_failed(self):
        """Retry downloading failed videos"""
        if not self.progress_data['failed_videos']:
            print("✅ No failed videos to retry")
            return

        print(f"🔄 Retrying {len(self.progress_data['failed_videos'])} failed videos...")

        # Reset failed attempts for retry
        for video_id in list(self.progress_data['failed_videos'].keys()):
            video_data = self.progress_data['failed_videos'][video_id]
            if video_data['attempts'] >= self.max_retries:
                video_data['attempts'] = self.max_retries - 1  # Allow one more try

        self._save_progress()

    def show_progress(self):
        """Display current progress statistics"""
        print("\n📊 Channel Download Progress:")
        print("=" * 60)

        total_downloaded = len(self.progress_data['downloaded_videos'])
        total_failed = len(self.progress_data['failed_videos'])

        print(f"✅ Total downloaded: {total_downloaded}")
        print(f"❌ Total failed: {total_failed}")

        if self.progress_data['channels']:
            print("\n📺 Channels processed:")
            for channel_id, info in self.progress_data['channels'].items():
                print(f"   - {channel_id}: {info['total_videos']} videos")

        if self.progress_data['failed_videos']:
            print("\n❌ Failed videos:")
            for video_id, info in list(self.progress_data['failed_videos'].items())[:10]:
                print(f"   - {info['title'][:50]}... (attempts: {info['attempts']})")

            if len(self.progress_data['failed_videos']) > 10:
                print(f"   ... and {len(self.progress_data['failed_videos']) - 10} more")

        print("=" * 60)


def main():
    parser = argparse.ArgumentParser(
        description='Download all videos from a YouTube channel as MP3 files',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s "https://www.youtube.com/@channelname"
  %(prog)s "https://www.youtube.com/c/channelname" -o music/channel
  %(prog)s "CHANNEL_URL" --min-delay 60 --max-delay 180
  %(prog)s --show-progress
  %(prog)s --retry-failed
        """
    )

    parser.add_argument('url', nargs='?', help='YouTube channel URL')
    parser.add_argument('-o', '--output', default='downloads',
                        help='Output directory (default: downloads)')
    parser.add_argument('-q', '--quality', default='192',
                        choices=['128', '192', '256', '320'],
                        help='Audio quality in kbps (default: 192)')
    parser.add_argument('--min-delay', type=int, default=30,
                        help='Minimum delay between downloads in seconds (default: 30)')
    parser.add_argument('--max-delay', type=int, default=120,
                        help='Maximum delay between downloads in seconds (default: 120)')
    parser.add_argument('--limit', type=int,
                        help='Limit number of videos to download')
    parser.add_argument('--no-cookies', action='store_true',
                        help='Disable cookie usage')
    parser.add_argument('--max-retries', type=int, default=3,
                        help='Maximum retry attempts per video (default: 3)')
    parser.add_argument('--show-progress', action='store_true',
                        help='Show download progress and statistics')
    parser.add_argument('--retry-failed', action='store_true',
                        help='Retry previously failed downloads')

    args = parser.parse_args()

    downloader = ChannelDownloader(
        output_dir=args.output,
        quality=args.quality,
        min_delay=args.min_delay,
        max_delay=args.max_delay,
        use_cookies=not args.no_cookies,
        max_retries=args.max_retries
    )

    if args.show_progress:
        downloader.show_progress()
        sys.exit(0)

    if args.retry_failed:
        downloader.retry_failed()
        if not args.url:
            sys.exit(0)

    if not args.url:
        parser.error("URL is required unless using --show-progress or --retry-failed")

    success = downloader.download_channel(args.url, limit=args.limit)
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()