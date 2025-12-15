import requests
from bs4 import BeautifulSoup
import yt_dlp
import os
import hashlib
from urllib.parse import urlparse, quote_plus
import json
import time

ARCHIVE_DIR = 'musiqueplus_archive'
os.makedirs(ARCHIVE_DIR, exist_ok=True)
os.makedirs(f'{ARCHIVE_DIR}/wayback', exist_ok=True)
os.makedirs(f'{ARCHIVE_DIR}/youtube', exist_ok=True)

def hash_file(path):
    with open(path, 'rb') as f:
        return hashlib.md5(f.read()).hexdigest()

def download_if_new(url, path):
    if os.path.exists(path):
        return False
    try:
        resp = requests.get(url, timeout=30)
        resp.raise_for_status()
        with open(path, 'wb') as f:
            f.write(resp.content)
        return True
    except:
        return False

def scrape_wayback_snapshots(domain, limit=10):
    wayback_url = f"https://web.archive.org/web/*/{domain}"
    try:
        resp = requests.get(wayback_url)
        soup = BeautifulSoup(resp.text, 'html.parser')
        links = soup.select('.sparkline a')
        snapshots = ['https://web.archive.org' + a['href'] for a in links][:limit]
        return snapshots
    except:
        return []

def download_snapshot(snapshot_url, domain):
    parsed = urlparse(snapshot_url)
    timestamp = parsed.path.split('/')[2]
    path = f'{ARCHIVE_DIR}/wayback/{domain}_{timestamp}.html'
    if download_if_new(snapshot_url, path):
        print(f"Saved Wayback: {path}")

def hoard_youtube(query, limit=5):
    ydl_opts = {
        'outtmpl': f'{ARCHIVE_DIR}/youtube/%(title)s.%(ext)s',
        'format': 'best[height<=720]',
        'quiet': False,
        'nooverwrites': True,
        'continuedl': True,
        'postprocessor_args': ['-metadata', 'comment:Resurrected by musiqueplus-resurrection'],
        'sleep_interval': 5,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        search = f"ytsearch{limit}:{query}"
        ydl.download([search])

# Targets - reduced for testing
domains = ["musiqueplus.com"]
queries = [
    "MusiquePlus VJ interview",
]

# Execute
for domain in domains:
    snapshots = scrape_wayback_snapshots(domain, 5)
    for snap in snapshots:
        download_snapshot(snap + '/http://' + domain, domain)
        time.sleep(1)

for q in queries:
    print(f"Hoards: {q}")
    hoard_youtube(q, 5)