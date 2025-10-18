#!/usr/bin/env python3
import json
import os
import time
from pathlib import Path
from typing import Optional, List, Dict
import logging

# Set up logging
logger = logging.getLogger(__name__)

class CookieManager:
    def __init__(self, cookie_dir: str = "cookies"):
        self.cookie_dir = Path(cookie_dir)
        self.cookie_dir.mkdir(exist_ok=True)
        self.current_cookie_file = None
        self.cookie_files = []
        self.usage_stats = {}
        self.stats_file = self.cookie_dir / "usage_stats.json"
        self._load_stats()
        self._scan_cookie_files()
        
    def _scan_cookie_files(self):
        self.cookie_files = list(self.cookie_dir.glob("*.txt"))
        if not self.cookie_files:
            logger.warning(f"No cookie files found in {self.cookie_dir}")
    
    def _load_stats(self):
        if self.stats_file.exists():
            with open(self.stats_file, 'r') as f:
                self.usage_stats = json.load(f)
    
    def _save_stats(self):
        with open(self.stats_file, 'w') as f:
            json.dump(self.usage_stats, f, indent=2)
    
    def get_next_cookie_file(self) -> Optional[Path]:
        if not self.cookie_files:
            return None
        
        # Sort by least recently used
        sorted_files = sorted(
            self.cookie_files,
            key=lambda f: self.usage_stats.get(str(f), {}).get('last_used', 0)
        )
        
        self.current_cookie_file = sorted_files[0]
        
        # Update usage stats
        file_key = str(self.current_cookie_file)
        if file_key not in self.usage_stats:
            self.usage_stats[file_key] = {'count': 0, 'last_used': 0}
        
        self.usage_stats[file_key]['count'] += 1
        self.usage_stats[file_key]['last_used'] = time.time()
        self._save_stats()
        
        return self.current_cookie_file
    
    def get_yt_dlp_opts(self, base_opts: Dict = None) -> Dict:
        opts = base_opts or {}
        
        cookie_file = self.get_next_cookie_file()
        if cookie_file:
            opts['cookiefile'] = str(cookie_file)
            logger.info(f"Using cookie file: {cookie_file.name}")
        else:
            # Fallback to browser cookies
            opts['cookiesfrombrowser'] = ('firefox',)
            logger.info("No cookie files found, falling back to Firefox browser cookies")
        
        return opts
    
    def add_cookie_file(self, source_path: str, name: Optional[str] = None):
        source = Path(source_path)
        if not source.exists():
            raise FileNotFoundError(f"Cookie file not found: {source_path}")
        
        if name:
            dest = self.cookie_dir / name
        else:
            # Use timestamp-based name
            timestamp = int(time.time())
            dest = self.cookie_dir / f"cookies_{timestamp}.txt"
        
        # Copy file
        dest.write_text(source.read_text())
        self._scan_cookie_files()
        logger.info(f"Added cookie file: {dest.name}")
        
    def list_cookies(self) -> List[Dict]:
        result = []
        for cookie_file in self.cookie_files:
            stats = self.usage_stats.get(str(cookie_file), {})
            result.append({
                'file': cookie_file.name,
                'path': str(cookie_file),
                'usage_count': stats.get('count', 0),
                'last_used': time.strftime('%Y-%m-%d %H:%M:%S', 
                                         time.localtime(stats.get('last_used', 0)))
                            if stats.get('last_used') else 'Never'
            })
        return sorted(result, key=lambda x: x['usage_count'])