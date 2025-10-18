#!/usr/bin/env python3
"""
YouTube Stealth Channel Downloader
Ultra-cautious, one-at-a-time downloader with human-like behavior
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
from datetime import datetime, timedelta, time as dt_time
from typing import Dict, List, Optional, Tuple
from cookie_manager import CookieManager
import logging


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    handlers=[
        logging.FileHandler('stealth_downloader.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class StealthChannelDownloader:
    """Ultra-cautious downloader that mimics human behavior"""

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
                 min_wait: int = 300,      # 5 minutes minimum
                 max_wait: int = 1800,      # 30 minutes maximum
                 use_cookies: bool = True,
                 stealth_mode: str = "high"):

        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.quality = quality
        self.min_wait = min_wait
        self.max_wait = max_wait
        self.use_cookies = use_cookies
        self.stealth_mode = stealth_mode
        self.ffmpeg_path = '/home/drn2/miniconda3/envs/ytaudio/bin'
        self.cookie_manager = CookieManager() if use_cookies else None

        # Progress tracking
        self.progress_file = self.output_dir / ".stealth_progress.json"
        self.progress_data = self._load_progress()

        # Session tracking
        self.session_id = hashlib.md5(str(datetime.now()).encode()).hexdigest()[:8]
        self.session_start = datetime.now()
        self.downloads_today = self._get_downloads_today()

        # Stealth parameters based on mode
        self.stealth_params = self._get_stealth_params()

    def _get_stealth_params(self) -> Dict:
        """Get parameters based on stealth mode"""
        modes = {
            'low': {
                'min_wait': 120,      # 2 minutes
                'max_wait': 600,      # 10 minutes
                'daily_limit': 50,
                'night_hours': None,
                'work_hours': None,
                'variance': 0.2
            },
            'medium': {
                'min_wait': 300,      # 5 minutes
                'max_wait': 1200,     # 20 minutes
                'daily_limit': 20,
                'night_hours': (23, 7),  # Avoid 11pm-7am
                'work_hours': None,
                'variance': 0.3
            },
            'high': {
                'min_wait': 600,      # 10 minutes
                'max_wait': 2400,     # 40 minutes
                'daily_limit': 10,
                'night_hours': (22, 8),  # Avoid 10pm-8am
                'work_hours': (9, 17),   # Prefer 9am-5pm
                'variance': 0.5
            },
            'paranoid': {
                'min_wait': 1800,     # 30 minutes
                'max_wait': 7200,     # 2 hours
                'daily_limit': 5,
                'night_hours': (21, 9),  # Avoid 9pm-9am
                'work_hours': (10, 16),  # Only 10am-4pm
                'variance': 0.7
            }
        }

        params = modes.get(self.stealth_mode, modes['high'])
        # Override with command line args if provided
        if self.min_wait:
            params['min_wait'] = self.min_wait
        if self.max_wait:
            params['max_wait'] = self.max_wait

        return params

    def _load_progress(self) -> Dict:
        """Load progress data"""
        if self.progress_file.exists():
            with open(self.progress_file, 'r') as f:
                return json.load(f)
        return {
            'downloaded_videos': {},
            'failed_videos': {},
            'channels': {},
            'daily_downloads': {},
            'sessions': []
        }

    def _save_progress(self):
        """Save progress data"""
        with open(self.progress_file, 'w') as f:
            json.dump(self.progress_data, f, indent=2, default=str)

    def _get_downloads_today(self) -> int:
        """Get number of downloads today"""
        today = datetime.now().strftime('%Y-%m-%d')
        return self.progress_data.get('daily_downloads', {}).get(today, 0)

    def _update_daily_downloads(self):
        """Update daily download counter"""
        today = datetime.now().strftime('%Y-%m-%d')
        if 'daily_downloads' not in self.progress_data:
            self.progress_data['daily_downloads'] = {}

        self.progress_data['daily_downloads'][today] = self.downloads_today + 1
        self.downloads_today += 1
        self._save_progress()

    def _check_time_restrictions(self) -> Tuple[bool, str]:
        """Check if current time is appropriate for downloading"""
        current_hour = datetime.now().hour

        # Check night hours restriction
        night_hours = self.stealth_params.get('night_hours')
        if night_hours:
            start, end = night_hours
            if start > end:  # Spans midnight
                if current_hour >= start or current_hour < end:
                    return False, f"Night hours ({start}:00-{end}:00). Waiting..."
            else:
                if start <= current_hour < end:
                    return False, f"Night hours ({start}:00-{end}:00). Waiting..."

        # Check work hours preference
        work_hours = self.stealth_params.get('work_hours')
        if work_hours:
            start, end = work_hours
            if not (start <= current_hour < end):
                return False, f"Outside work hours ({start}:00-{end}:00). Consider waiting..."

        return True, "Time check passed"

    def _check_daily_limit(self) -> Tuple[bool, str]:
        """Check if daily download limit reached"""
        daily_limit = self.stealth_params.get('daily_limit', 999)
        if self.downloads_today >= daily_limit:
            return False, f"Daily limit ({daily_limit}) reached. Resume tomorrow."

        remaining = daily_limit - self.downloads_today
        return True, f"{remaining} downloads remaining today"

    def _human_like_delay(self) -> float:
        """Calculate human-like delay with patterns"""
        base_min = self.stealth_params['min_wait']
        base_max = self.stealth_params['max_wait']
        variance = self.stealth_params['variance']

        # Base delay
        delay = random.uniform(base_min, base_max)

        # Add variance for more randomness
        variance_factor = random.uniform(1 - variance, 1 + variance)
        delay *= variance_factor

        # Longer delays after multiple downloads
        if self.downloads_today > 5:
            delay *= 1.5
        elif self.downloads_today > 10:
            delay *= 2.0

        # Add "break" periods (simulating human breaks)
        if random.random() < 0.1:  # 10% chance of long break
            print("☕ Taking a coffee break...")
            delay += random.uniform(900, 1800)  # 15-30 min break

        # Round to make it look more human (humans don't wait exactly 523.7 seconds)
        if delay < 300:
            delay = round(delay / 10) * 10  # Round to nearest 10 seconds
        else:
            delay = round(delay / 60) * 60  # Round to nearest minute

        return max(base_min, delay)

    def _simulate_human_behavior(self):
        """Simulate human-like browsing behavior"""
        behaviors = [
            "👀 Browsing other videos...",
            "📖 Reading comments...",
            "🔍 Checking video details...",
            "📱 Switching tabs...",
            "☕ Getting a drink...",
            "🚶 Taking a short break...",
            "📺 Watching part of the video...",
            "💭 Thinking about next video...",
        ]

        if random.random() < 0.3:  # 30% chance
            behavior = random.choice(behaviors)
            print(f"\n{behavior}")
            time.sleep(random.uniform(5, 20))

    def _get_video_list(self, channel_url: str, days_filter: Optional[int] = None) -> List[Dict]:
        """Get video list from channel"""
        print("📋 Fetching channel videos (this may take a moment)...")

        # Ensure we're fetching the videos tab
        if '@' in channel_url and '/videos' not in channel_url:
            channel_url = channel_url.rstrip('/') + '/videos'
            logger.info(f"Using videos tab URL: {channel_url}")

        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'extract_flat': 'in_playlist',
            'playlistend': None,
            'user_agent': random.choice(self.USER_AGENTS),
        }

        if self.use_cookies and self.cookie_manager:
            ydl_opts = self.cookie_manager.get_yt_dlp_opts(ydl_opts)

        # Calculate cutoff date if days filter is set
        cutoff_date = None
        if days_filter:
            cutoff_date = datetime.now() - timedelta(days=days_filter)
            print(f"📅 Filtering videos from last {days_filter} days (since {cutoff_date.strftime('%Y-%m-%d')})")

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(channel_url, download=False)

                if 'entries' not in info:
                    logger.warning("No entries found in channel info")
                    return []

                videos = []
                skipped_count = 0
                date_filtered_count = 0

                for entry in info['entries']:
                    if not entry:
                        continue

                    # Skip None entries
                    if 'id' not in entry:
                        skipped_count += 1
                        continue

                    video_id = entry['id']

                    # Skip if ID looks like a channel/playlist ID instead of video ID
                    # Channel IDs start with UC, Playlist IDs don't look like video IDs
                    # Valid YouTube video IDs are 11 characters long
                    if not video_id or video_id.startswith('UC') or len(video_id) != 11:
                        logger.warning(f"Skipping invalid video ID: {video_id}")
                        skipped_count += 1
                        continue

                    # Filter by upload date if requested
                    if cutoff_date and 'timestamp' in entry:
                        upload_date = datetime.fromtimestamp(entry['timestamp'])
                        if upload_date < cutoff_date:
                            date_filtered_count += 1
                            continue

                    videos.append({
                        'id': video_id,
                        'title': entry.get('title', 'Unknown'),
                        'url': f"https://www.youtube.com/watch?v={video_id}",
                        'duration': entry.get('duration', 0),
                        'upload_date': entry.get('upload_date', 'Unknown')
                    })

                if skipped_count > 0:
                    logger.info(f"Skipped {skipped_count} invalid entries")

                if date_filtered_count > 0:
                    logger.info(f"Filtered out {date_filtered_count} videos older than {days_filter} days")

                # Shuffle for more random appearance
                if self.stealth_mode in ['high', 'paranoid']:
                    random.shuffle(videos)

                logger.info(f"Found {len(videos)} valid videos from channel")
                return videos

        except Exception as e:
            logger.error(f"Error fetching videos: {e}")
            return []

    def _download_single_video(self, video: Dict, channel_dir: Path) -> bool:
        """Download a single video with maximum stealth"""
        video_id = video['id']

        # Check if already downloaded
        if video_id in self.progress_data['downloaded_videos']:
            print(f"⏭️  Already downloaded: {video['title'][:50]}...")
            return True

        # Check failed attempts
        failed_info = self.progress_data.get('failed_videos', {}).get(video_id, {})
        if failed_info.get('attempts', 0) >= 3:
            print(f"⏭️  Skipping (too many failures): {video['title'][:50]}...")
            return False

        # Simulate human behavior before download
        self._simulate_human_behavior()

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
            'restrictfilenames': True,
            'ignoreerrors': False,
            'no_color': False,
            'retries': 3,
            'fragment_retries': 3,
            'skip_unavailable_fragments': True,
            'user_agent': random.choice(self.USER_AGENTS),
            'throttled_rate': '50K',  # Slower download speed
            'http_chunk_size': 10485760,
            'sleep_interval_requests': 1,  # Sleep between requests
            'max_sleep_interval': 5,
        }

        if self.use_cookies and self.cookie_manager:
            ydl_opts = self.cookie_manager.get_yt_dlp_opts(ydl_opts)

        try:
            print(f"\n🎵 Downloading: {video['title'][:60]}...")
            print(f"   📊 Today's downloads: {self.downloads_today + 1}/{self.stealth_params['daily_limit']}")

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([video['url']])

            # Mark as downloaded
            self.progress_data['downloaded_videos'][video_id] = {
                'title': video['title'],
                'downloaded_at': datetime.now().isoformat(),
                'session': self.session_id
            }
            self._update_daily_downloads()
            self._save_progress()

            print(f"✅ Successfully downloaded: {video['title'][:50]}...")
            return True

        except Exception as e:
            logger.error(f"Download failed: {e}")
            print(f"❌ Failed to download: {str(e)[:100]}...")

            # Check if it's a permanent failure
            error_msg = str(e).lower()
            is_permanent = ('unavailable' in error_msg or
                          'private' in error_msg or
                          'deleted' in error_msg or
                          'removed' in error_msg)

            # Record failure
            if video_id not in self.progress_data.get('failed_videos', {}):
                self.progress_data['failed_videos'][video_id] = {
                    'title': video['title'],
                    'attempts': 0,
                    'permanent_failure': is_permanent
                }
            else:
                self.progress_data['failed_videos'][video_id]['permanent_failure'] = is_permanent

            self.progress_data['failed_videos'][video_id]['attempts'] += 1
            self._save_progress()

            return False

    def _progress_hook(self, d):
        """Progress display"""
        if d['status'] == 'downloading':
            percent = d.get('_percent_str', 'N/A')
            speed = d.get('_speed_str', 'N/A')
            eta = d.get('_eta_str', 'N/A')
            # Less frequent updates to reduce noise
            if random.random() < 0.1:  # Only update 10% of the time
                print(f"\r📥 {percent} | {speed} | ETA: {eta}", end='', flush=True)
        elif d['status'] == 'finished':
            print("\n🔄 Converting to MP3...")

    def _wait_with_countdown(self, seconds: float, reason: str = ""):
        """Show countdown with reason"""
        total = int(seconds)
        print(f"\n⏳ Waiting {total} seconds {reason}")
        print(f"   💤 Stealth mode: {self.stealth_mode}")

        # Show progress bar
        for remaining in range(total, 0, -1):
            if remaining % 60 == 0:  # Update every minute
                mins = remaining // 60
                print(f"   ⏰ {mins} minute{'s' if mins != 1 else ''} remaining...")

            # Allow interrupt with Ctrl+C
            try:
                time.sleep(1)
            except KeyboardInterrupt:
                print("\n⛔ Interrupted by user")
                raise

        print("   ✅ Wait complete, proceeding...")

    def download_channel(self, channel_url: str, limit: Optional[int] = None, days: Optional[int] = None):
        """Download channel with maximum stealth"""
        print(f"🥷 YouTube Stealth Channel Downloader")
        print(f"📁 Output: {self.output_dir}")
        print(f"🎵 Quality: {self.quality} kbps")
        print(f"🛡️ Stealth mode: {self.stealth_mode}")
        print(f"⏱️  Wait time: {self.stealth_params['min_wait']}s - {self.stealth_params['max_wait']}s")
        print(f"📊 Daily limit: {self.stealth_params['daily_limit']}")
        if days:
            print(f"📅 Date filter: Last {days} days")
        print(f"🆔 Session: {self.session_id}")
        print("=" * 70)

        # Check time restrictions
        time_ok, time_msg = self._check_time_restrictions()
        if not time_ok:
            print(f"⏰ {time_msg}")
            if self.stealth_mode == 'paranoid':
                print("   Exiting due to paranoid mode time restrictions.")
                return False

        # Check daily limit
        limit_ok, limit_msg = self._check_daily_limit()
        print(f"📊 {limit_msg}")
        if not limit_ok:
            print("   Please run again tomorrow.")
            return False

        # Get video list
        videos = self._get_video_list(channel_url, days_filter=days)
        if not videos:
            print("❌ No videos found in channel")
            print("   This could mean:")
            print("   - The channel has no videos")
            print("   - The channel URL is incorrect")
            print("   - The channel requires authentication")
            print("   - yt-dlp couldn't parse the channel page")
            if days:
                print(f"   - No videos were uploaded in the last {days} days")
            return False

        # Apply limit
        if limit:
            videos = videos[:limit]

        # Adjust limit based on daily limit
        remaining_today = self.stealth_params['daily_limit'] - self.downloads_today
        if len(videos) > remaining_today:
            print(f"📝 Limiting to {remaining_today} videos due to daily limit")
            videos = videos[:remaining_today]

        print(f"\n📊 Found {len(videos)} videos to process")

        # Create channel directory
        channel_name = "channel_" + hashlib.md5(channel_url.encode()).hexdigest()[:8]
        channel_dir = self.output_dir / channel_name
        channel_dir.mkdir(exist_ok=True)

        # Log channel
        self.progress_data['channels'][channel_name] = {
            'url': channel_url,
            'session': self.session_id,
            'started': datetime.now().isoformat()
        }
        self._save_progress()

        # Download videos one at a time with long waits
        downloaded = 0
        failed = 0

        print("\n🚀 Starting ultra-cautious download process...")
        print("   ℹ️  Press Ctrl+C to pause safely\n")

        for i, video in enumerate(videos):
            # Check daily limit again
            limit_ok, _ = self._check_daily_limit()
            if not limit_ok:
                print("\n📊 Daily limit reached. Resume tomorrow.")
                break

            # Check for stop file
            stop_file = self.output_dir / '.stop'
            if stop_file.exists():
                print("\n⛔ Stop signal detected")
                stop_file.unlink()
                break

            # Download video
            print(f"\n{'='*70}")
            print(f"Video {i+1}/{len(videos)}")

            success = self._download_single_video(video, channel_dir)

            if success:
                downloaded += 1
            else:
                failed += 1
                # Only add extra delay for non-permanent failures (e.g., rate limiting, network issues)
                # Don't wait extra for videos that are unavailable/private/deleted
                failed_info = self.progress_data.get('failed_videos', {}).get(video['id'], {})
                if not failed_info.get('permanent_failure'):
                    print("⚠️  Adding extra delay after failure...")
                    time.sleep(random.uniform(60, 180))

            # Don't wait after last video
            if i < len(videos) - 1:
                # Calculate wait time
                wait_time = self._human_like_delay()

                # Random chance of super long wait
                if random.random() < 0.05:  # 5% chance
                    print("\n🌙 Taking extended break (simulating sleep/work)...")
                    wait_time += random.uniform(3600, 7200)  # 1-2 hours

                self._wait_with_countdown(
                    wait_time,
                    f"(video {i+2}/{len(videos)} next)"
                )

        # Summary
        print("\n" + "="*70)
        print("📈 Session Summary:")
        print(f"   ✅ Downloaded: {downloaded}")
        print(f"   ❌ Failed: {failed}")
        print(f"   📊 Today's total: {self.downloads_today}")
        print(f"   ⏱️  Session duration: {str(datetime.now() - self.session_start).split('.')[0]}")
        print("="*70)

        # Log session
        self.progress_data['sessions'].append({
            'id': self.session_id,
            'date': datetime.now().isoformat(),
            'downloaded': downloaded,
            'failed': failed,
            'channel': channel_url
        })
        self._save_progress()

        return failed == 0

    def show_stats(self):
        """Show download statistics"""
        print("\n📊 Stealth Downloader Statistics")
        print("="*70)

        total = len(self.progress_data.get('downloaded_videos', {}))
        failed = len(self.progress_data.get('failed_videos', {}))

        print(f"Total downloaded: {total}")
        print(f"Total failed: {failed}")

        # Daily stats
        if self.progress_data.get('daily_downloads'):
            print("\nDaily downloads:")
            for date, count in sorted(self.progress_data['daily_downloads'].items())[-7:]:
                print(f"  {date}: {count} downloads")

        # Session history
        if self.progress_data.get('sessions'):
            print(f"\nRecent sessions: {len(self.progress_data['sessions'])}")
            for session in self.progress_data['sessions'][-5:]:
                print(f"  {session['date'][:10]}: {session['downloaded']} downloaded")

        print("="*70)


def main():
    parser = argparse.ArgumentParser(
        description='Ultra-cautious YouTube channel downloader with stealth mode',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Stealth Modes:
  low      : 2-10 min delays, 50 videos/day
  medium   : 5-20 min delays, 20 videos/day, avoids night
  high     : 10-40 min delays, 10 videos/day, work hours preferred (default)
  paranoid : 30min-2hr delays, 5 videos/day, strict time windows

Examples:
  %(prog)s "https://www.youtube.com/@channelname"
  %(prog)s "URL" --stealth paranoid
  %(prog)s "URL" --stealth medium --limit 10
  %(prog)s "URL" --days 7  # Only videos from last 7 days
  %(prog)s "URL" --days 30 --limit 5  # Last 30 days, max 5 videos
  %(prog)s "URL" --min-wait 900 --max-wait 3600
  %(prog)s --stats
        """
    )

    parser.add_argument('url', nargs='?', help='YouTube channel URL')
    parser.add_argument('-o', '--output', default='downloads',
                        help='Output directory (default: downloads)')
    parser.add_argument('-q', '--quality', default='192',
                        choices=['128', '192', '256', '320'],
                        help='Audio quality in kbps (default: 192)')
    parser.add_argument('--stealth', default='high',
                        choices=['low', 'medium', 'high', 'paranoid'],
                        help='Stealth mode level (default: high)')
    parser.add_argument('--min-wait', type=int,
                        help='Override minimum wait in seconds')
    parser.add_argument('--max-wait', type=int,
                        help='Override maximum wait in seconds')
    parser.add_argument('--limit', type=int,
                        help='Limit number of videos to download')
    parser.add_argument('--days', type=int,
                        help='Only download videos from the last X days')
    parser.add_argument('--no-cookies', action='store_true',
                        help='Disable cookie usage')
    parser.add_argument('--stats', action='store_true',
                        help='Show download statistics')

    args = parser.parse_args()

    downloader = StealthChannelDownloader(
        output_dir=args.output,
        quality=args.quality,
        min_wait=args.min_wait or 0,
        max_wait=args.max_wait or 0,
        use_cookies=not args.no_cookies,
        stealth_mode=args.stealth
    )

    if args.stats:
        downloader.show_stats()
        sys.exit(0)

    if not args.url:
        parser.error("URL required unless using --stats")

    try:
        success = downloader.download_channel(args.url, limit=args.limit, days=args.days)
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⛔ Download paused by user")
        print("   Run again to resume from where you left off")
        sys.exit(130)


if __name__ == '__main__':
    main()