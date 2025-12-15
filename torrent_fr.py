import requests
from bs4 import BeautifulSoup
import os
import subprocess
import time
from urllib.parse import quote_plus

TORRENTS_DIR = 'mtv_archive_fr/torrents'
os.makedirs(TORRENTS_DIR, exist_ok=True)

def scrape_1337x_magnets(query, limit=10):
    search_url = f"https://1337x.to/search/{quote_plus(query)}/1/"
    try:
        resp = requests.get(search_url, headers={'User-Agent': 'Mozilla/5.0'})
        soup = BeautifulSoup(resp.text, 'html.parser')
        rows = soup.select('table.table-list tr')[1:limit+1]
        magnets = []
        for row in rows:
            name_link = row.select_one('.name a[href^="/torrent/"]')
            if name_link and ('480p' in name_link.text or 'DVD' in name_link.text or 'VF' in name_link.text):
                torrent_url = 'https://1337x.to' + name_link['href']
                name = name_link.text.strip()
                detail_resp = requests.get(torrent_url, headers={'User-Agent': 'Mozilla/5.0'})
                detail_soup = BeautifulSoup(detail_resp.text, 'html.parser')
                magnet_a = detail_soup.select_one('a[href^="magnet:"]')
                if magnet_a:
                    magnet = magnet_a['href']
                    magnets.append((name, magnet))
                    print(f"FR Magnet: {name}")
        return magnets[:5]
    except Exception as e:
        print(f"Scrape fail: {e}")
        return []

def download_magnet(magnet, path=TORRENTS_DIR):
    try:
        subprocess.run(['aria2c', '--dir=' + path, '--max-connection-per-server=16', '--split=16', '--seed-time=0', magnet], check=True, capture_output=True)
        print("FR Torrent summoned.")
    except:
        print("Aria2c summon failed.")

# French MusiquePlus/MTV targets: Quebec vein
targets_fr = [
    "MusiquePlus 80s emissions 480p VF",
    "MusiquePlus 90s VJ clips 480p",
    "MusiquePlus Top 10 2000s 480p",
    "MusiquePlus rap Quebec 480p",
    "Anne-Marie Losique interviews 480p",
    "MusiquePlus live performances 480p",
]

for target in targets_fr:
    print(f"FR Breach: {target}")
    magnets = scrape_1337x_magnets(target)
    for name, magnet in magnets:
        download_magnet(magnet)
    time.sleep(2)

print("French MTV vein: ghosts raised.")