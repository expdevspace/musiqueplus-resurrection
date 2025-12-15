import os
import glob
import json
from jinja2 import Environment, FileSystemLoader  # pip install jinja2 if not hexed in

ARCHIVE_DIR = 'musiqueplus_archive'
OUTPUT_DIR = 'docs'  # for GitHub Pages
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Collect artifacts
wayback_files = glob.glob(f'{ARCHIVE_DIR}/wayback/*.html')
youtube_vids = glob.glob(f'{ARCHIVE_DIR}/youtube/*.mp4')  # assuming yt-dlp grabs mp4
metadata = {
    'wayback': [{'name': os.path.basename(f), 'path': f.replace(ARCHIVE_DIR, '').lstrip('/')} for f in wayback_files],
    'youtube': [{'name': os.path.basename(f), 'path': f.replace(ARCHIVE_DIR, '').lstrip('/')} for f in youtube_vids],
}

# Jinja template for index.html
template_str = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>MusiquePlus Resurrection</title>
    <style>
        body { background: #000; color: #0f0; font-family: monospace; }
        a { color: #f00; }
        .section { margin: 20px; }
    </style>
</head>
<body>
    <h1>MusiquePlus Empire</h1>
    <div class="section">
        <h2>Wayback Captures</h2>
        <ul>
        {% for item in wayback %}
            <li><a href="{{ item.path }}">{{ item.name }}</a></li>
        {% endfor %}
        </ul>
    </div>
    <div class="section">
        <h2>YouTube Hoards</h2>
        <ul>
        {% for item in youtube %}
            <li><a href="{{ item.path }}">{{ item.name }}</a></li>
        {% endfor %}
        </ul>
    </div>
</body>
</html>
"""

env = Environment()
template = env.from_string(template_str)
html = template.render(metadata)

with open(f'{OUTPUT_DIR}/index.html', 'w', encoding='utf-8') as f:
    f.write(html)

# Copy artifacts to docs (symbolic if local, but for git: hard copy light ones)
# os.system(f'cp -r {ARCHIVE_DIR}/* {OUTPUT_DIR}/')  # tweak if too heavy; git lfs later