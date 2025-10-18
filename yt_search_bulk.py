#!/usr/bin/env python3
"""
YouTube Bulk Search Tool
Search for YouTube videos based on criteria and save URLs to a text file (one URL per line)
"""
import yt_dlp
import argparse
import sys
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional


class YouTubeSearcher:
    def __init__(self):
        pass

    def search_videos(self,
                     query: str,
                     min_duration: Optional[int] = None,
                     max_duration: Optional[int] = None,
                     sort_by: str = 'relevance',
                     max_results: int = 50,
                     date_filter: Optional[str] = None) -> List[Dict]:
        """
        Search YouTube videos with filters

        Args:
            query: Search term
            min_duration: Minimum duration in seconds (e.g., 1200 for 20 min)
            max_duration: Maximum duration in seconds
            sort_by: Sort order - 'relevance', 'upload_date', 'view_count', 'rating'
            max_results: Maximum number of results to return
            date_filter: Filter by date - 'hour', 'today', 'week', 'month', 'year'

        Returns:
            List of video dictionaries with metadata
        """
        print(f"🔍 Searching YouTube for: '{query}'")
        print(f"📊 Filters: min_duration={min_duration}s, sort={sort_by}, max_results={max_results}")

        # Build search URL with filters
        search_query = f"ytsearch{max_results}:{query}"

        # Sorting via search query
        if sort_by == 'upload_date':
            search_query = f"ytsearchdate{max_results}:{query}"

        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'extract_flat': False,  # Need full info for duration filtering
            'skip_download': True,
            'ignoreerrors': True,  # Continue on errors
            'socket_timeout': 10,
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                print("⏳ Fetching search results...")
                result = ydl.extract_info(search_query, download=False)

                if not result or 'entries' not in result:
                    print("❌ No results found")
                    return []

                videos = []
                for entry in result['entries']:
                    if not entry:  # Skip None entries (failed extractions)
                        continue

                    video_data = {
                        'id': entry.get('id'),
                        'title': entry.get('title', 'Unknown'),
                        'url': entry.get('webpage_url') or f"https://www.youtube.com/watch?v={entry.get('id')}",
                        'duration': entry.get('duration', 0),
                        'upload_date': entry.get('upload_date'),
                        'view_count': entry.get('view_count', 0),
                        'like_count': entry.get('like_count', 0),
                        'channel': entry.get('uploader', 'Unknown'),
                        'channel_url': entry.get('uploader_url', ''),
                    }

                    # Apply duration filters
                    duration = video_data['duration']
                    if min_duration and duration < min_duration:
                        continue
                    if max_duration and duration > max_duration:
                        continue

                    videos.append(video_data)

                # Apply additional sorting if needed
                if sort_by == 'view_count':
                    videos.sort(key=lambda x: x['view_count'], reverse=True)
                elif sort_by == 'rating':
                    videos.sort(key=lambda x: x['like_count'], reverse=True)
                elif sort_by == 'upload_date':
                    videos.sort(key=lambda x: x['upload_date'] or '', reverse=True)

                print(f"✅ Found {len(videos)} videos matching criteria")
                return videos

        except Exception as e:
            print(f"❌ Search error: {e}")
            return []

    def save_urls_to_file(self, videos: List[Dict], output_file: str):
        """
        Save video URLs to a file (one URL per line)

        Args:
            videos: List of video dictionaries
            output_file: Output file path
        """
        output_path = Path(output_file)

        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                for video in videos:
                    f.write(f"{video['url']}\n")

            print(f"✅ Saved {len(videos)} URLs to: {output_path}")
            return True

        except Exception as e:
            print(f"❌ Error saving to file: {e}")
            return False

    def display_results(self, videos: List[Dict]):
        """Display search results in a formatted table"""
        if not videos:
            print("No videos to display")
            return

        print("\n" + "="*100)
        print(f"{'#':<4} {'Title':<50} {'Duration':<10} {'Views':<12} {'Channel':<24}")
        print("="*100)

        for i, video in enumerate(videos, 1):
            duration_min = video['duration'] // 60
            duration_sec = video['duration'] % 60
            duration_str = f"{duration_min}:{duration_sec:02d}"

            title = video['title'][:47] + "..." if len(video['title']) > 50 else video['title']
            channel = video['channel'][:21] + "..." if len(video['channel']) > 24 else video['channel']
            views = f"{video['view_count']:,}" if video['view_count'] else "N/A"

            print(f"{i:<4} {title:<50} {duration_str:<10} {views:<12} {channel:<24}")

        print("="*100)


def parse_duration(duration_str: str) -> int:
    """
    Parse duration string to seconds
    Examples: '20m', '1h', '30s', '1h30m', '90'
    """
    duration_str = duration_str.lower().strip()
    total_seconds = 0

    # If just a number, assume minutes
    if duration_str.isdigit():
        return int(duration_str) * 60

    # Parse hours
    if 'h' in duration_str:
        parts = duration_str.split('h')
        total_seconds += int(parts[0]) * 3600
        duration_str = parts[1] if len(parts) > 1 else ''

    # Parse minutes
    if 'm' in duration_str:
        parts = duration_str.split('m')
        total_seconds += int(parts[0]) * 60
        duration_str = parts[1] if len(parts) > 1 else ''

    # Parse seconds
    if 's' in duration_str:
        parts = duration_str.split('s')
        total_seconds += int(parts[0])

    return total_seconds


def main():
    parser = argparse.ArgumentParser(
        description='Search YouTube videos and save URLs to file',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Search for videos over 20 minutes
  %(prog)s "jazz music" --min-duration 20m -o jazz_urls.txt

  # Search for recent uploads, sorted by date
  %(prog)s "python tutorial" --sort upload_date --max-results 100 -o python_vids.txt

  # Search with duration range (10-30 minutes)
  %(prog)s "meditation" --min-duration 10m --max-duration 30m -o meditation.txt

  # Search for long documentaries
  %(prog)s "documentary" --min-duration 1h -o docs.txt

Duration format:
  - 20m = 20 minutes
  - 1h = 1 hour
  - 1h30m = 1 hour 30 minutes
  - 90 = 90 minutes (default to minutes if just number)
  - 30s = 30 seconds
        """
    )

    parser.add_argument('query', help='Search query/term')
    parser.add_argument('-o', '--output', default='search_results.txt',
                       help='Output file path (default: search_results.txt)')
    parser.add_argument('--min-duration', type=str,
                       help='Minimum video duration (e.g., 20m, 1h, 1h30m)')
    parser.add_argument('--max-duration', type=str,
                       help='Maximum video duration (e.g., 30m, 2h)')
    parser.add_argument('--sort', choices=['relevance', 'upload_date', 'view_count', 'rating'],
                       default='relevance',
                       help='Sort order (default: relevance)')
    parser.add_argument('--max-results', type=int, default=50,
                       help='Maximum number of results (default: 50)')
    parser.add_argument('--display-only', action='store_true',
                       help='Only display results, do not save to file')

    args = parser.parse_args()

    # Parse durations
    min_duration = parse_duration(args.min_duration) if args.min_duration else None
    max_duration = parse_duration(args.max_duration) if args.max_duration else None

    # Create searcher
    searcher = YouTubeSearcher()

    # Perform search
    videos = searcher.search_videos(
        query=args.query,
        min_duration=min_duration,
        max_duration=max_duration,
        sort_by=args.sort,
        max_results=args.max_results
    )

    if not videos:
        print("❌ No videos found matching criteria")
        sys.exit(1)

    # Display results
    searcher.display_results(videos)

    # Save to file unless display-only
    if not args.display_only:
        success = searcher.save_urls_to_file(videos, args.output)
        sys.exit(0 if success else 1)
    else:
        print(f"\n💡 Use without --display-only to save URLs to file")
        sys.exit(0)


if __name__ == '__main__':
    main()
