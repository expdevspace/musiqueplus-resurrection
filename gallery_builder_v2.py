#!/usr/bin/env python3
"""
MTV Resurrection Gallery Builder

This script generates a static HTML gallery from archived MTV content.
It collects files from specified directories and generates a browseable interface.
"""
import os
import sys
import glob
import logging
import shutil
from pathlib import Path
from typing import Dict, List, Any, Optional

import click
from jinja2 import Environment, FileSystemLoader, select_autoescape
from tqdm import tqdm

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('gallery_builder.log')
    ]
)
logger = logging.getLogger(__name__)

# Default configuration
DEFAULT_CONFIG = {
    'archive_dir': 'mtv_archive',
    'output_dir': 'docs',  # for GitHub Pages
    'supported_formats': {
        'wayback': ['*.html'],
        'youtube': ['*.mp4', '*.webm', '*.mkv'],
    }
}

# HTML template
template_str = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>MTV Resurrection</title>
    <style>
        :root {
            --bg-color: #0a0a0a;
            --text-color: #0f0;
            --accent-color: #f00;
            --section-bg: #111;
            --hover-color: #0f0;
        }
        
        body { 
            background: var(--bg-color); 
            color: var(--text-color); 
            font-family: 'Courier New', monospace;
            line-height: 1.6;
            margin: 0;
            padding: 0;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }
        
        header {
            text-align: center;
            padding: 20px 0;
            border-bottom: 2px solid var(--accent-color);
            margin-bottom: 30px;
        }
        
        h1 {
            color: var(--accent-color);
            margin: 0;
            font-size: 2.5em;
        }
        
        .section {
            background: var(--section-bg);
            border-radius: 8px;
            padding: 20px;
            margin-bottom: 30px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
        }
        
        h2 {
            color: var(--accent-color);
            border-bottom: 1px solid #333;
            padding-bottom: 10px;
            margin-top: 0;
        }
        
        ul {
            list-style-type: none;
            padding: 0;
            margin: 0;
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
            gap: 15px;
        }
        
        li {
            padding: 10px;
            background: rgba(255, 255, 255, 0.05);
            border-radius: 4px;
            transition: all 0.3s ease;
        }
        
        li:hover {
            background: rgba(0, 255, 0, 0.1);
            transform: translateY(-2px);
        }
        
        a {
            color: var(--text-color);
            text-decoration: none;
            display: block;
            padding: 5px 0;
        }
        
        a:hover {
            color: var(--hover-color);
            text-decoration: underline;
        }
        
        .file-info {
            font-size: 0.9em;
            color: #888;
            margin-top: 5px;
        }
        
        footer {
            text-align: center;
            margin-top: 40px;
            padding: 20px 0;
            border-top: 1px solid #333;
            font-size: 0.9em;
            color: #666;
        }
        
        @media (max-width: 768px) {
            ul {
                grid-template-columns: 1fr;
            }
            
            .container {
                padding: 10px;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>MTV Resurrection</h1>
            <p>Preserving the legacy of MTV</p>
        </header>
        
        <div class="section">
            <h2>Wayback Captures</h2>
            {% if wayback %}
            <ul>
                {% for item in wayback %}
                <li>
                    <a href="{{ item.path }}" target="_blank">
                        {{ item.name }}
                        <div class="file-info">
                            {{ item.size }} • {{ item.last_modified }}
                        </div>
                    </a>
                </li>
                {% endfor %}
            </ul>
            {% else %}
            <p>No Wayback captures found.</p>
            {% endif %}
        </div>
        
        <div class="section">
            <h2>YouTube Archives</h2>
            {% if youtube %}
            <ul>
                {% for item in youtube %}
                <li>
                    <a href="{{ item.path }}" target="_blank">
                        {{ item.name }}
                        <div class="file-info">
                            {{ item.size }} • {{ item.last_modified }}
                        </div>
                    </a>
                </li>
                {% endfor %}
            </ul>
            {% else %}
            <p>No YouTube videos found.</p>
            {% endif %}
        </div>
        
        <footer>
            <p>Generated on {{ generated_date }} • 
               {{ wayback|length }} Wayback captures • 
               {{ youtube|length }} YouTube videos</p>
        </footer>
    </div>
</body>
</html>
"""


def get_file_metadata(file_path: str) -> Dict[str, str]:
    """Get metadata for a file."""
    try:
        stat = os.stat(file_path)
        return {
            'name': os.path.basename(file_path),
            'path': file_path.replace('\\', '/'),  # Ensure forward slashes for web
            'size': _format_size(stat.st_size),
            'last_modified': _format_date(stat.st_mtime)
        }
    except OSError as e:
        logger.error(f"Error getting metadata for {file_path}: {e}")
        return {}


def _format_size(size_bytes: int) -> str:
    """Convert file size to human-readable format."""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.1f} PB"


def _format_date(timestamp: float) -> str:
    """Format timestamp to readable date."""
    from datetime import datetime
    return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')


def collect_files(directory: str, patterns: List[str]) -> List[Dict[str, str]]:
    """Collect files matching patterns from directory."""
    files = []
    for pattern in patterns:
        try:
            for file_path in glob.glob(os.path.join(directory, '**', pattern), recursive=True):
                if os.path.isfile(file_path):
                    metadata = get_file_metadata(file_path)
                    if metadata:
                        files.append(metadata)
        except Exception as e:
            logger.error(f"Error collecting files with pattern {pattern} in {directory}: {e}")
    
    # Sort by name
    return sorted(files, key=lambda x: x['name'].lower())


def ensure_directory(directory: str) -> bool:
    """Ensure directory exists, create if it doesn't."""
    try:
        os.makedirs(directory, exist_ok=True)
        return True
    except OSError as e:
        logger.error(f"Error creating directory {directory}: {e}")
        return False


def copy_assets(archive_dir: str, output_dir: str) -> None:
    """Copy necessary assets to output directory."""
    try:
        # Create necessary subdirectories
        for subdir in ['wayback', 'youtube']:
            src_dir = os.path.join(archive_dir, subdir)
            dst_dir = os.path.join(output_dir, subdir)
            
            if os.path.exists(src_dir):
                ensure_directory(dst_dir)
                
                # Copy files with progress bar
                files = [f for f in os.listdir(src_dir) if os.path.isfile(os.path.join(src_dir, f))]
                for file in tqdm(files, desc=f"Copying {subdir} files"):
                    src = os.path.join(src_dir, file)
                    dst = os.path.join(dst_dir, file)
                    try:
                        if not os.path.exists(dst) or os.path.getmtime(src) > os.path.getmtime(dst):
                            shutil.copy2(src, dst)
                    except Exception as e:
                        logger.error(f"Error copying {src} to {dst}: {e}")
    except Exception as e:
        logger.error(f"Error copying assets: {e}")


def generate_html(metadata: Dict[str, List[Dict[str, str]]], output_file: str) -> bool:
    """Generate HTML from template and metadata."""
    try:
        env = Environment(autoescape=select_autoescape(['html', 'xml']))
        template = env.from_string(template_str)
        
        from datetime import datetime
        html = template.render(
            **metadata,
            generated_date=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        )
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html)
            
        logger.info(f"Successfully generated {output_file}")
        return True
    except Exception as e:
        logger.error(f"Error generating HTML: {e}")
        return False


@click.command()
@click.option('--archive-dir', default=DEFAULT_CONFIG['archive_dir'],
              help='Directory containing archived content')
@click.option('--output-dir', default=DEFAULT_CONFIG['output_dir'],
              help='Output directory for generated files')
@click.option('--skip-copy', is_flag=True, help='Skip copying assets')
@click.option('--debug', is_flag=True, help='Enable debug logging')
def main(archive_dir: str, output_dir: str, skip_copy: bool, debug: bool) -> None:
    """Generate a static HTML gallery from archived MTV content."""
    if debug:
        logger.setLevel(logging.DEBUG)
    
    logger.info("Starting MTV gallery generation")
    
    # Ensure directories exist
    if not ensure_directory(archive_dir):
        logger.error(f"Archive directory {archive_dir} does not exist and could not be created")
        sys.exit(1)
        
    if not ensure_directory(output_dir):
        logger.error(f"Could not create output directory {output_dir}")
        sys.exit(1)
    
    # Copy assets if needed
    if not skip_copy:
        logger.info("Copying assets...")
        copy_assets(archive_dir, output_dir)
    
    # Collect files
    logger.info("Collecting files...")
    metadata = {}
    
    for category, patterns in DEFAULT_CONFIG['supported_formats'].items():
        category_dir = os.path.join(archive_dir, category)
        if os.path.exists(category_dir):
            files = collect_files(category_dir, patterns)
            # Update paths to be relative to output_dir
            for file in files:
                file['path'] = os.path.join(category, os.path.basename(file['path']))
            metadata[category] = files
            logger.info(f"Found {len(files)} {category} files")
    
    # Generate HTML
    output_file = os.path.join(output_dir, 'index.html')
    if generate_html(metadata, output_file):
        logger.info("Gallery generation completed successfully")
    else:
        logger.error("Failed to generate gallery")
        sys.exit(1)


if __name__ == '__main__':
    main()