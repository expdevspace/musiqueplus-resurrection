import requests
from bs4 import BeautifulSoup
import os
import json
import time
import re
from urllib.parse import quote_plus

MAGNETS_DIR = 'magnets'
os.makedirs(MAGNETS_DIR, exist_ok=True)

def scrape_1337x_magnets(query, limit=10):
    search_url = f"https://1337x.to/search/{quote_plus(query)}/1/"
    try:
        print(f"Searching for: {query}")
        # Add more headers to mimic a real browser
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }
        resp = requests.get(search_url, headers=headers, timeout=10)
        print(f"Response status: {resp.status_code}")
        if resp.status_code == 403:
            print(f"Access forbidden for {query} - site may be blocking requests")
            return []
        if resp.status_code != 200:
            print(f"Failed to fetch search results for {query}")
            return []
        soup = BeautifulSoup(resp.text, 'html.parser')
        rows = soup.select('table.table-list tr')[1:limit+1]
        magnets = []
        for row in rows:
            name_link = row.select_one('.name a[href^="/torrent/"]')
            if name_link and ('480p' in name_link.text or 'DVD' in name_link.text or 'VF' in name_link.text):
                href = name_link.get('href', '')
                if href:
                    torrent_url = 'https://1337x.to' + str(href)
                    name = name_link.text.strip()
                    print(f"Found torrent: {name}")
                    # Get torrent details
                    detail_resp = requests.get(torrent_url, headers=headers, timeout=10)
                    if detail_resp.status_code == 403:
                        print(f"Access forbidden for torrent details - site may be blocking requests")
                        continue
                    if detail_resp.status_code != 200:
                        print(f"Failed to fetch torrent details for {name}")
                        continue
                    detail_soup = BeautifulSoup(detail_resp.text, 'html.parser')
                    magnet_a = detail_soup.select_one('a[href^="magnet:"]')
                    if magnet_a:
                        magnet = magnet_a.get('href', '')
                        if magnet:
                            # Extract year from title using regex
                            year_match = re.search(r'\b(19|20)\d{2}\b', name)
                            year = year_match.group() if year_match else '1985'
                            
                            magnets.append({
                                "name": name,
                                "magnet": str(magnet),
                                "year": year,
                                "duration": "1800"  # Default 30 minutes, will be updated later
                            })
                            print(f"FR Magnet: {name} ({year})")
        return magnets[:5]
    except requests.exceptions.RequestException as e:
        print(f"Network error while scraping: {e}")
        return []
    except Exception as e:
        print(f"Scrape fail: {e}")
        return []

def save_magnets_json(magnets, filename):
    """Save magnets array to JSON file"""
    filepath = os.path.join(MAGNETS_DIR, filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(magnets, f, indent=2, ensure_ascii=False)
    print(f"Saved {len(magnets)} magnets to {filepath}")

# French MusiquePlus/MTV targets: Quebec vein
targets_fr = [
    "MusiquePlus 80s emissions 480p VF",
    "MusiquePlus 90s VJ clips 480p",
    "MusiquePlus Top 10 2000s 480p",
    "MusiquePlus rap Quebec 480p",
    "Anne-Marie Losique interviews 480p",
    "MusiquePlus live performances 480p",
]

print("Starting French torrent search...")
all_magnets = []
for target in targets_fr:
    print(f"FR Breach: {target}")
    magnets = scrape_1337x_magnets(target)
    all_magnets.extend(magnets)
    time.sleep(2)

# Save all magnets to JSON
save_magnets_json(all_magnets, 'fr.json')
print("French MTV vein: ghosts raised.")