#!/usr/bin/env python3
"""
Advanced YouTube Channel Downloader
Enhanced version with user-agent rotation, proxy support, and advanced anti-detection
"""
import yt_dlp
import sys
import os
import time
import random
import json
import argparse
import hashlib
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Set, Tuple
from cookie_manager import CookieManager
import logging


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('channel_downloader.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class AdvancedChannelDownloader:
    # User agents for rotation
    USER_AGENTS = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15',
    ]

    def __init__(self,
                 output_dir: str = "downloads",
                 quality: str = "192",
                 min_delay: int = 45,
                 max_delay: int = 180,
                 use_cookies: bool = True,
                 max_retries: int = 3,
                 proxy: Optional[str] = None,
                 batch_size: int = 5):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.quality = quality
        self.min_delay = min_delay
        self.max_delay = max_delay
        self.use_cookies = use_cookies
        self.max_retries = max_retries
        self.proxy = proxy
        self.batch_size = batch_size
        self.ffmpeg_path = '/home/drn2/miniconda3/envs/ytaudio/bin'
        self.cookie_manager = CookieManager() if use_cookies else None

        # Progress tracking
        self.progress_file = self.output_dir / ".channel_progress_advanced.json"
        self.progress_data = self._load_progress()

        # Session management
        self.session_id = hashlib.md5(str(datetime.now()).encode()).hexdigest()[:8]
        self.downloads_in_session = 0
        self.last_download_time = None

        # Statistics
        self.stats = {
            'downloaded': 0,
            'skipped': 0,
            'failed': 0,
            'total': 0,
            'bytes_downloaded': 0,
            'time_started': datetime.now()
        }

    def _load_progress(self) -> Dict:
        """Load progress data from file"""
        if self.progress_file.exists():
            with open(self.progress_file, 'r') as f:
                return json.load(f)
        return {
            'downloaded_videos': {},
            'failed_videos': {},
            'channels': {},
            'sessions': []
        }

    def _save_progress(self):
        """Save progress data to file"""
        with open(self.progress_file, 'w') as f:
            json.dump(self.progress_data, f, indent=2, default=str)

    def _log_session(self):
        """Log session information"""
        session_info = {
            'id': self.session_id,
            'started': self.stats['time_started'].isoformat(),
            'ended': datetime.now().isoformat(),
            'downloaded': self.stats['downloaded'],
            'failed': self.stats['failed'],
            'skipped': self.stats['skipped']
        }
        self.progress_data['sessions'].append(session_info)
        self._save_progress()

    def _get_random_user_agent(self) -> str:
        """Get a random user agent"""
        return random.choice(self.USER_AGENTS)

    def _adaptive_delay(self) -> float:
        """Calculate adaptive delay based on download patterns"""
        base_delay = random.uniform(self.min_delay, self.max_delay)

        # Add jitter
        jitter = random.uniform(-5, 5)

        # Increase delay after multiple downloads
        if self.downloads_in_session > 10:
            base_delay *= 1.5
        elif self.downloads_in_session > 20:
            base_delay *= 2

        # Add longer pause every N downloads
        if self.downloads_in_session > 0 and self.downloads_in_session % self.batch_size == 0:
            print(f"🛏️  Taking extended break after {self.batch_size} downloads...")
            base_delay += random.uniform(120, 300)  # 2-5 minute break

        return max(self.min_delay, base_delay + jitter)

    def _get_video_list_with_metadata(self, channel_url: str) -> List[Dict]:
        """Get detailed video list with metadata"""
        print("📋 Fetching detailed channel information...")

        ydl_opts = {
            'quiet': False,
            'no_warnings': False,
            'extract_flat': False,  # Get full metadata
            'playlistend': None,
            'ignoreerrors': True,
            'user_agent': self._get_random_user_agent(),
        }

        if self.proxy:
            ydl_opts['proxy'] = self.proxy

        if self.use_cookies and self.cookie_manager:
            ydl_opts = self.cookie_manager.get_yt_dlp_opts(ydl_opts)

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                # First, get basic channel info
                ydl_opts_flat = ydl_opts.copy()
                ydl_opts_flat['extract_flat'] = 'in_playlist'

                with yt_dlp.YoutubeDL(ydl_opts_flat) as ydl_flat:
                    info = ydl_flat.extract_info(channel_url, download=False)

                    if 'entries' not in info:
                        print("❌ No videos found in channel")
                        return []

                    videos = []
                    channel_name = info.get('channel', info.get('uploader', 'Unknown'))

                    print(f"📺 Channel: {channel_name}")
                    print(f"📊 Total videos found: {len(info['entries'])}")

                    for entry in info['entries']:
                        if entry and 'id' in entry:
                            videos.append({
                                'id': entry['id'],
                                'title': entry.get('title', 'Unknown'),
                                'url': f"https://www.youtube.com/watch?v={entry['id']}",
                                'duration': entry.get('duration', 0),
                                'upload_date': entry.get('upload_date', ''),
                                'view_count': entry.get('view_count', 0),
                                'channel_name': channel_name
                            })

                    # Sort by upload date (newest first) or keep original order
                    videos.sort(key=lambda x: x.get('upload_date', ''), reverse=True)

                    return videos

        except Exception as e:
            logger.error(f"Error fetching video list: {e}")
            print(f"❌ Error fetching video list: {e}")
            return []

    def _download_video_with_fallback(self, video: Dict, channel_dir: Path) -> bool:
        """Download video with multiple quality fallbacks"""
        video_id = video['id']

        # Check if already downloaded
        if video_id in self.progress_data['downloaded_videos']:
            print(f"⏭️  Skipping (already downloaded): {video['title'][:60]}...")
            self.stats['skipped'] += 1
            return True

        # Check failure history
        failed_info = self.progress_data['failed_videos'].get(video_id, {})
        if failed_info.get('attempts', 0) >= self.max_retries:
            if not failed_info.get('permanent_failure'):
                print(f"⏭️  Skipping (max retries): {video['title'][:60]}...")
                self.stats['skipped'] += 1
            return False

        # Quality fallback options
        quality_options = [self.quality, '192', '128', '96']
        quality_options = list(dict.fromkeys(quality_options))  # Remove duplicates

        for attempt, quality in enumerate(quality_options):
            ydl_opts = {
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': quality,
                }],
                'outtmpl': str(channel_dir / '%(title)s.%(ext)s'),
                'ffmpeg_location': self.ffmpeg_path,
                'quiet': False,
                'no_warnings': False,
                'progress_hooks': [self._progress_hook],
                'restrictfilenames': True,
                'ignoreerrors': False,
                'no_color': False,
                'retries': 10,
                'fragment_retries': 10,
                'skip_unavailable_fragments': True,
                'user_agent': self._get_random_user_agent(),
                'http_chunk_size': 10485760,  # 10MB chunks
                'throttled_rate': '100K',  # Limit speed if throttled
            }

            if self.proxy:
                ydl_opts['proxy'] = self.proxy

            if self.use_cookies and self.cookie_manager:
                ydl_opts = self.cookie_manager.get_yt_dlp_opts(ydl_opts)

            try:
                print(f"\n🎵 Downloading [{self.stats['downloaded'] + 1}/{self.stats['total']}]: {video['title'][:60]}...")
                if quality != self.quality:
                    print(f"   📉 Using fallback quality: {quality} kbps")
                print(f"   📅 Upload date: {video.get('upload_date', 'Unknown')}")
                print(f"   ⏱️  Duration: {video.get('duration', 0) // 60}:{video.get('duration', 0) % 60:02d}")

                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([video['url']])

                # Success - save progress
                self.progress_data['downloaded_videos'][video_id] = {
                    'title': video['title'],
                    'downloaded_at': datetime.now().isoformat(),
                    'duration': video.get('duration', 0),
                    'quality': quality,
                    'session': self.session_id
                }
                self._save_progress()

                print(f"✅ Downloaded: {video['title'][:60]}...")
                self.stats['downloaded'] += 1
                self.downloads_in_session += 1
                self.last_download_time = datetime.now()

                # Clear any failure records
                if video_id in self.progress_data['failed_videos']:
                    del self.progress_data['failed_videos'][video_id]
                    self._save_progress()

                return True

            except yt_dlp.utils.DownloadError as e:
                error_msg = str(e).lower()
                if 'video unavailable' in error_msg or 'private video' in error_msg:
                    print(f"⚠️  Video unavailable or private: {video['title'][:60]}...")
                    # Mark as permanent failure
                    self._record_failure(video, str(e), permanent=True)
                    self.stats['skipped'] += 1
                    return False
                elif 'sign in' in error_msg:
                    print(f"⚠️  Age-restricted or sign-in required: {video['title'][:60]}...")
                    self._record_failure(video, str(e))
                    if attempt == len(quality_options) - 1:
                        self.stats['failed'] += 1
                    continue
                else:
                    logger.warning(f"Download error for {video['title']}: {e}")
                    if attempt < len(quality_options) - 1:
                        print(f"⚠️  Retrying with lower quality...")
                        time.sleep(random.uniform(5, 15))
                        continue

            except Exception as e:
                logger.error(f"Unexpected error downloading {video['title']}: {e}")
                print(f"❌ Error: {str(e)[:100]}...")

        # All attempts failed
        self._record_failure(video, "All quality options failed")
        self.stats['failed'] += 1
        return False

    def _record_failure(self, video: Dict, error: str, permanent: bool = False):
        """Record a failed download attempt"""
        video_id = video['id']
        if video_id not in self.progress_data['failed_videos']:
            self.progress_data['failed_videos'][video_id] = {
                'title': video['title'],
                'attempts': 0,
                'errors': [],
                'permanent_failure': permanent
            }

        fail_record = self.progress_data['failed_videos'][video_id]
        fail_record['attempts'] += 1
        fail_record['errors'].append({
            'error': error[:200],
            'timestamp': datetime.now().isoformat()
        })
        fail_record['permanent_failure'] = permanent
        self._save_progress()

    def _progress_hook(self, d):
        """Enhanced progress callback"""
        if d['status'] == 'downloading':
            percent = d.get('_percent_str', 'N/A')
            speed = d.get('_speed_str', 'N/A')
            eta = d.get('_eta_str', 'N/A')
            size = d.get('_total_bytes_str', 'N/A')
            print(f"\r📥 {percent} | {size} | {speed} | ETA: {eta}", end='', flush=True)
        elif d['status'] == 'finished':
            size = d.get('total_bytes', 0)
            self.stats['bytes_downloaded'] += size
            print(f"\n🔄 Converting to MP3 ({self._format_bytes(size)})...")

    def _format_bytes(self, bytes: int) -> str:
        """Format bytes to human readable string"""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if bytes < 1024.0:
                return f"{bytes:.1f} {unit}"
            bytes /= 1024.0
        return f"{bytes:.1f} TB"

    def _show_delay_countdown(self, delay: float):
        """Show an enhanced countdown with progress bar"""
        total_seconds = int(delay)
        print(f"\n⏳ Waiting {total_seconds} seconds before next download...")

        for remaining in range(total_seconds, 0, -1):
            bar_length = 30
            progress = (total_seconds - remaining) / total_seconds
            filled = int(bar_length * progress)
            bar = '█' * filled + '░' * (bar_length - filled)

            print(f"\r⏳ [{bar}] {remaining}s remaining", end='', flush=True)
            time.sleep(1)

        print("\r" + " " * 60 + "\r", end='')  # Clear line

    def download_channel(self,
                        channel_url: str,
                        limit: Optional[int] = None,
                        reverse: bool = False,
                        date_after: Optional[str] = None):
        """Download all videos from a channel with advanced options"""
        print(f"🚀 Advanced YouTube Channel Downloader v2.0")
        print(f"📁 Output: {self.output_dir}")
        print(f"🎵 Quality: {self.quality} kbps")
        print(f"⏱️  Delay: {self.min_delay}-{self.max_delay}s")
        print(f"🔄 Batch size: {self.batch_size} videos")
        if self.proxy:
            print(f"🌐 Using proxy: {self.proxy}")
        print(f"🆔 Session: {self.session_id}")
        print("=" * 70)

        # Get video list
        videos = self._get_video_list_with_metadata(channel_url)
        if not videos:
            print("❌ No videos found to download")
            return False

        # Filter by date if specified
        if date_after:
            cutoff_date = date_after.replace('-', '')
            videos = [v for v in videos if v.get('upload_date', '') >= cutoff_date]
            print(f"📅 Filtered to videos after {date_after}: {len(videos)} videos")

        # Reverse order if requested (oldest first)
        if reverse:
            videos.reverse()
            print("🔄 Downloading in reverse order (oldest first)")

        # Apply limit
        if limit:
            videos = videos[:limit]
            print(f"📊 Limited to {limit} videos")

        self.stats['total'] = len(videos)

        # Extract channel name from first video
        channel_name = videos[0].get('channel_name', 'Unknown').replace(' ', '_')
        channel_dir = self.output_dir / channel_name
        channel_dir.mkdir(exist_ok=True)

        print(f"\n📊 Processing {len(videos)} videos from: {channel_name}")
        print("=" * 70)

        # Update channel info
        self.progress_data['channels'][channel_name] = {
            'url': channel_url,
            'total_videos': len(videos),
            'session': self.session_id,
            'last_updated': datetime.now().isoformat()
        }
        self._save_progress()

        # Download videos
        for i, video in enumerate(videos):
            # Check for stop signal (create a .stop file to pause)
            stop_file = self.output_dir / '.stop'
            if stop_file.exists():
                print("\n⛔ Stop signal detected. Pausing downloads...")
                stop_file.unlink()
                break

            # Download video
            success = self._download_video_with_fallback(video, channel_dir)

            # Adaptive delay
            if i < len(videos) - 1:
                delay = self._adaptive_delay()
                self._show_delay_countdown(delay)

        # Log session and show summary
        self._log_session()
        self._show_summary()

        return self.stats['failed'] == 0

    def _show_summary(self):
        """Show detailed download summary"""
        duration = datetime.now() - self.stats['time_started']
        print("\n" + "=" * 70)
        print("📈 Download Summary")
        print("=" * 70)
        print(f"   ✅ Downloaded: {self.stats['downloaded']}")
        print(f"   ⏭️  Skipped: {self.stats['skipped']}")
        print(f"   ❌ Failed: {self.stats['failed']}")
        print(f"   📊 Total: {self.stats['total']}")
        print(f"   💾 Data: {self._format_bytes(self.stats['bytes_downloaded'])}")
        print(f"   ⏱️  Duration: {str(duration).split('.')[0]}")
        print(f"   🆔 Session: {self.session_id}")

        if self.stats['downloaded'] > 0:
            avg_time = duration.total_seconds() / self.stats['downloaded']
            print(f"   ⚡ Avg time per video: {avg_time:.1f}s")

        print("=" * 70)

    def cleanup_duplicates(self):
        """Remove duplicate downloads based on file hash"""
        print("🧹 Scanning for duplicate files...")
        # Implementation for duplicate detection
        pass


def main():
    parser = argparse.ArgumentParser(
        description='Advanced YouTube Channel Downloader with Anti-Detection',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s "https://www.youtube.com/@channelname"
  %(prog)s "URL" --min-delay 60 --max-delay 300 --batch-size 10
  %(prog)s "URL" --limit 50 --reverse
  %(prog)s "URL" --date-after 2024-01-01
  %(prog)s "URL" --proxy http://proxy:8080
        """
    )

    parser.add_argument('url', help='YouTube channel URL')
    parser.add_argument('-o', '--output', default='downloads',
                        help='Output directory')
    parser.add_argument('-q', '--quality', default='192',
                        choices=['128', '192', '256', '320'],
                        help='Audio quality in kbps (default: 192)')
    parser.add_argument('--min-delay', type=int, default=45,
                        help='Min delay between downloads (default: 45s)')
    parser.add_argument('--max-delay', type=int, default=180,
                        help='Max delay between downloads (default: 180s)')
    parser.add_argument('--batch-size', type=int, default=5,
                        help='Videos per batch before extended break (default: 5)')
    parser.add_argument('--limit', type=int,
                        help='Limit number of videos to download')
    parser.add_argument('--reverse', action='store_true',
                        help='Download oldest videos first')
    parser.add_argument('--date-after',
                        help='Only download videos after date (YYYY-MM-DD)')
    parser.add_argument('--proxy',
                        help='Proxy server URL')
    parser.add_argument('--no-cookies', action='store_true',
                        help='Disable cookie usage')
    parser.add_argument('--max-retries', type=int, default=3,
                        help='Max retries per video (default: 3)')

    args = parser.parse_args()

    downloader = AdvancedChannelDownloader(
        output_dir=args.output,
        quality=args.quality,
        min_delay=args.min_delay,
        max_delay=args.max_delay,
        use_cookies=not args.no_cookies,
        max_retries=args.max_retries,
        proxy=args.proxy,
        batch_size=args.batch_size
    )

    try:
        success = downloader.download_channel(
            args.url,
            limit=args.limit,
            reverse=args.reverse,
            date_after=args.date_after
        )
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⛔ Download interrupted by user")
        downloader._log_session()
        downloader._show_summary()
        sys.exit(130)


if __name__ == '__main__':
    main()