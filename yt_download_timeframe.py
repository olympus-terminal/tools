#!/usr/bin/env python3
import yt_dlp
import sys
import os
import re
from pathlib import Path
from datetime import datetime, timedelta
import argparse

def sanitize_filename(filename):
    """Remove special characters from filename, keeping only alphanumeric, dash, and underscore"""
    # Replace spaces with underscores
    filename = filename.replace(' ', '_')
    # Remove all special characters except alphanumeric, dash, underscore, and dot
    filename = re.sub(r'[^\w\-_\.]', '', filename)
    # Replace multiple underscores with single underscore
    filename = re.sub(r'_+', '_', filename)
    # Remove leading/trailing underscores
    filename = filename.strip('_')
    return filename

def download_audio_by_timeframe(url, output_dir="downloads", date_after=None, date_before=None):
    Path(output_dir).mkdir(exist_ok=True)
    
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': f'{output_dir}/%(upload_date)s_%(title)s.%(ext)s',
        'ffmpeg_location': '/home/drn2/miniconda3/envs/ytaudio/bin',
        'ignoreerrors': True,
        'quiet': False,
        'no_warnings': False,
        'restrictfilenames': True,  # This helps with some special characters
    }
    
    # Add date filters if specified
    if date_after:
        ydl_opts['dateafter'] = date_after.strftime('%Y%m%d')
    if date_before:
        ydl_opts['datebefore'] = date_before.strftime('%Y%m%d')
    
    # Custom output template processor to sanitize filename
    def process_info(info):
        if 'title' in info:
            info['title'] = sanitize_filename(info['title'])
        return info
    
    ydl_opts['postprocessor_hooks'] = {
        'before_dl': [process_info]
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        # Extract info first to check if it's a playlist or channel
        info = ydl.extract_info(url, download=False)
        
        if info.get('_type') in ['playlist', 'channel']:
            print(f"Processing {info.get('_type')}: {info.get('title', 'Unknown')}")
            print(f"Total videos: {len(info.get('entries', []))}")
            
            # Filter entries by date if needed
            if date_after or date_before:
                filtered_entries = []
                for entry in info.get('entries', []):
                    if entry is None:
                        continue
                    upload_date_str = entry.get('upload_date', '')
                    if upload_date_str:
                        upload_date = datetime.strptime(upload_date_str, '%Y%m%d')
                        if date_after and upload_date < date_after:
                            continue
                        if date_before and upload_date > date_before:
                            continue
                        filtered_entries.append(entry)
                
                print(f"Videos matching date criteria: {len(filtered_entries)}")
                
                # Download filtered entries
                for entry in filtered_entries:
                    # Sanitize title for display
                    clean_title = sanitize_filename(entry.get('title', 'Unknown'))
                    print(f"\nDownloading: {clean_title} (uploaded: {entry.get('upload_date', 'Unknown')})")
                    
                    # Update the title in the entry for filename
                    entry['title'] = clean_title
                    ydl.process_info(entry)
                    ydl.download([entry['webpage_url']])
            else:
                # Download all if no date filter
                ydl.download([url])
        else:
            # Single video
            upload_date_str = info.get('upload_date', '')
            if upload_date_str:
                upload_date = datetime.strptime(upload_date_str, '%Y%m%d')
                if date_after and upload_date < date_after:
                    print(f"Video uploaded on {upload_date.strftime('%Y-%m-%d')} is before the specified date {date_after.strftime('%Y-%m-%d')}")
                    return
                if date_before and upload_date > date_before:
                    print(f"Video uploaded on {upload_date.strftime('%Y-%m-%d')} is after the specified date {date_before.strftime('%Y-%m-%d')}")
                    return
            
            clean_title = sanitize_filename(info.get('title', 'Unknown'))
            print(f"Downloading: {clean_title} (uploaded: {upload_date_str})")
            info['title'] = clean_title
            ydl.process_info(info)
            ydl.download([url])

def parse_date(date_str):
    """Parse date string in various formats"""
    for fmt in ['%Y-%m-%d', '%Y/%m/%d', '%d-%m-%Y', '%d/%m/%Y']:
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            continue
    
    # Try relative dates
    if date_str.lower() == 'today':
        return datetime.now()
    elif date_str.lower() == 'yesterday':
        return datetime.now() - timedelta(days=1)
    elif date_str.lower().endswith('days'):
        days = int(date_str.split()[0])
        return datetime.now() - timedelta(days=days)
    elif date_str.lower().endswith('weeks'):
        weeks = int(date_str.split()[0])
        return datetime.now() - timedelta(weeks=weeks)
    elif date_str.lower().endswith('months'):
        months = int(date_str.split()[0])
        return datetime.now() - timedelta(days=months*30)
    elif date_str.lower().endswith('years'):
        years = int(date_str.split()[0])
        return datetime.now() - timedelta(days=years*365)
    
    raise ValueError(f"Unable to parse date: {date_str}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Download YouTube audio from videos within a specific timeframe')
    parser.add_argument('url', help='YouTube video, playlist, or channel URL')
    parser.add_argument('-o', '--output', default='downloads', help='Output directory (default: downloads)')
    parser.add_argument('--after', help='Download videos uploaded after this date (e.g., 2023-01-01, "7 days", "2 weeks")')
    parser.add_argument('--before', help='Download videos uploaded before this date (e.g., 2023-12-31, "today", "1 month")')
    
    args = parser.parse_args()
    
    date_after = None
    date_before = None
    
    try:
        if args.after:
            date_after = parse_date(args.after)
            print(f"Filtering videos uploaded after: {date_after.strftime('%Y-%m-%d')}")
        
        if args.before:
            date_before = parse_date(args.before)
            print(f"Filtering videos uploaded before: {date_before.strftime('%Y-%m-%d')}")
        
        download_audio_by_timeframe(args.url, args.output, date_after, date_before)
        
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Download error: {e}")
        sys.exit(1)