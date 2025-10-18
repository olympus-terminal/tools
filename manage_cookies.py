#!/usr/bin/env python3
"""
Cookie Management Tool for yt-dlp
Helps manage and rotate YouTube cookies for downloads
"""
import argparse
import sys
from pathlib import Path
from cookie_manager import CookieManager
import logging

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def main():
    parser = argparse.ArgumentParser(
        description='Manage cookies for YouTube downloads',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s add cookies.txt                    # Add a cookie file
  %(prog)s add ~/Downloads/cookies.txt youtube1  # Add with custom name
  %(prog)s list                               # List all cookie files
  %(prog)s export-guide                       # Show cookie export guide
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    # Add cookie command
    add_parser = subparsers.add_parser('add', help='Add a new cookie file')
    add_parser.add_argument('file', help='Path to cookie file')
    add_parser.add_argument('name', nargs='?', help='Optional name for the cookie file')
    
    # List cookies command
    subparsers.add_parser('list', help='List all cookie files and their usage')
    
    # Export guide command
    subparsers.add_parser('export-guide', help='Show guide for exporting cookies')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    cookie_manager = CookieManager()
    
    if args.command == 'add':
        try:
            cookie_manager.add_cookie_file(args.file, args.name)
            print(f"✅ Cookie file added successfully!")
            print(f"📁 Stored in: {cookie_manager.cookie_dir}")
        except FileNotFoundError as e:
            print(f"❌ Error: {e}")
            sys.exit(1)
    
    elif args.command == 'list':
        cookies = cookie_manager.list_cookies()
        if not cookies:
            print("No cookie files found.")
            print(f"Add cookies to: {cookie_manager.cookie_dir}")
        else:
            print(f"\n📂 Cookie files in {cookie_manager.cookie_dir}:\n")
            print(f"{'File':<30} {'Usage Count':<15} {'Last Used':<20}")
            print("-" * 65)
            for cookie in cookies:
                print(f"{cookie['file']:<30} {cookie['usage_count']:<15} {cookie['last_used']:<20}")
    
    elif args.command == 'export-guide':
        print("""
📖 Cookie Export Guide for YouTube
==================================

⚠️  WARNING: Using your account with yt-dlp may risk account restrictions.
    Consider using a throwaway account for downloads.

Steps to Export YouTube Cookies:
--------------------------------
1. Open a NEW private/incognito browser window
2. Log into YouTube with the account you want to use
3. Navigate to: https://www.youtube.com/robots.txt
4. Use a browser extension to export cookies:
   - Chrome: "Get cookies.txt LOCALLY" or "EditThisCookie"
   - Firefox: "cookies.txt" extension
5. Export cookies from youtube.com domain
6. IMMEDIATELY close the private browsing window
7. Save the exported cookies to a .txt file

Adding Cookies to This Tool:
---------------------------
1. Run: python manage_cookies.py add /path/to/cookies.txt
2. The tool will automatically rotate between multiple cookie files

Important Notes:
---------------
- YouTube rotates cookies frequently
- Using private browsing helps get fresh cookies
- Avoid excessive downloads to prevent account restrictions
- Consider using multiple accounts with rotation
""")

if __name__ == '__main__':
    main()