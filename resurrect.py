import requests
from bs4 import BeautifulSoup
import yt_dlp
import os
import time
import subprocess
from urllib.parse import quote_plus

ARCHIVE_DIR = 'musiqueplus_archive'
TORRENTS_DIR = os.path.join(ARCHIVE_DIR, 'torrents')
os.makedirs(TORRENTS_DIR, exist_ok=True)
os.makedirs(f'{ARCHIVE_DIR}/youtube', exist_ok=True)

# Purge bullshit (optional: comment if you want to keep)
for f in os.listdir(f'{ARCHIVE_DIR}/youtube'):
    os.remove(os.path.join(f'{ARCHIVE_DIR}/youtube', f))

def hoard_youtube(query, limit=10):
    ydl_opts = {
        'outtmpl': f'{ARCHIVE_DIR}/youtube/%(title)s.%(ext)s',
        'format': 'best[height<=480]',  # 480p cap
        'quiet': False,
        'nooverwrites': True,
        'continuedl': True,
        'postprocessor_args': ['-metadata', 'comment:Resurrected by Yngr0ss - English vein'],
        'sleep_interval': 2,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        search = f"ytsearch{limit}:{query} full episode English"
        ydl.download([search])

def scrape_1337x_magnets(query, limit=5):
    search_url = f"https://1337x.to/search/{quote_plus(query)}/1/"
    try:
        resp = requests.get(search_url, timeout=10)
        soup = BeautifulSoup(resp.text, 'html.parser')
        rows = soup.select('table.table-list tr')[1:limit+1]
        magnets = []
        for row in rows:
            name_link = row.select_one('.name a[href^="/torrent/"]')
            if name_link:
                torrent_url = 'https://1337x.to' + name_link['href']
                name = name_link.text.strip()
                detail_resp = requests.get(torrent_url, timeout=10)
                detail_soup = BeautifulSoup(detail_resp.text, 'html.parser')
                magnet_a = detail_soup.select_one('a[href^="magnet:"]')
                if magnet_a:
                    magnet = magnet_a['href']
                    magnets.append((name, magnet))
                    print(f"Magnet hoarded: {name}")
        return magnets
    except:
        return []

def download_magnet(magnet, path=TORRENTS_DIR):
    if subprocess.call(['aria2c', '--dir=' + path, '--max-connection-per-server=16', '--split=16', magnet], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) == 0:
        print("Torrent summoned.")
    else:
        print("Aria2c ritual failed — check install.")

# The good vein: English 480p targets
targets = [
    "Room Raiders full episodes 480p English",
    "Snoop Dogg Father Hood full episodes 480p English",
    "Keeping Up with the Kardashians full episodes 480p English",
    "Gene Simmons Family Jewels full episodes 480p English",
    "Dogg After Dark Snoop full episodes 480p English",
]

# Execute: torrents first, youtube fallback
for target in targets:
    print(f"Breaching: {target}")
    magnets = scrape_1337x_magnets(target)
    for name, magnet in magnets:
        download_magnet(magnet)
    # Fallback hoard
    hoard_youtube(target, 5)
    time.sleep(3)  # Veil breath

print("Vein purified. Empire swells.")