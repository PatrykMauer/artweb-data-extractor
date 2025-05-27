# extract_lightweight.py

import requests
from bs4 import BeautifulSoup
import csv
import os
from urllib.parse import urlparse

# Configuration
INPUT_URLS_FILE = "data/seed_urls.txt"
OUTPUT_CSV_FILE = "data/art_dataset.csv"

# Art-related keywords
ART_KEYWORDS = [
    "painting", "sculpture", "etching", "canvas", "installation",
    "lithograph", "drawing", "exhibition", "portfolio", "gallery"
]

ARTISTS = ["picasso", "chagall", "dali", "monet", "matisse",
           "kahlo", "warhol", "haring", "basquiat", "alechinsky"]


def extract_features(url):
    try:
        response = requests.get(url, timeout=10)
        if response.status_code != 200:
            return None

        soup = BeautifulSoup(response.text, 'html.parser')
        title = soup.title.string.strip() if soup.title else ''
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        meta_keywords = soup.find('meta', attrs={'name': 'keywords'})
        images = soup.find_all('img')
        alt_tags = [img.get('alt', '').strip()
                    for img in images if img.get('alt')]
        links = [a.get_text(strip=True)
                 for a in soup.find_all('a') if a.get_text(strip=True)]
        body_text = soup.get_text(separator=' ', strip=True).lower()

        has_gallery = any(k in body_text
                          for k in ['gallery', 'carousel', 'slider'])
        detected_artists = [a for a in ARTISTS if a in body_text]
        context_keywords = [k for k in ART_KEYWORDS if k in body_text]

        return {
            'url': url,
            'page_title': title,
            'meta_description': meta_desc['content'].strip() if meta_desc and meta_desc.get('content') else '',
            'meta_keywords': meta_keywords['content'].strip() if meta_keywords and meta_keywords.get('content') else '',
            'image_count': len(images),
            'alt_tags': ';'.join(alt_tags),
            'link_texts': ';'.join(links),
            'has_gallery': has_gallery,
            'artist_names': ';'.join(detected_artists),
            'context_keywords': ';'.join(context_keywords),
            'contains_artwork': ''  # To be filled manually
        }

    except Exception as e:
        print(f"Failed to process {url}: {e}")
        return None


def main():
    os.makedirs(os.path.dirname(OUTPUT_CSV_FILE), exist_ok=True)

    with open(INPUT_URLS_FILE, "r", encoding="utf-8") as infile:
        urls = [line.strip() for line in infile if line.strip()
                and not line.startswith('#')]

    with open(OUTPUT_CSV_FILE, "w", newline='', encoding="utf-8-sig") as csvfile:
        fieldnames = [
            'url', 'page_title', 'meta_description', 'meta_keywords',
            'image_count', 'alt_tags', 'link_texts', 'has_gallery',
            'artist_names', 'context_keywords', 'contains_artwork']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for url in urls:
            print(f"Processing: {url}")
            data = extract_features(url)
            if data:
                writer.writerow(data)


if __name__ == "__main__":
    main()
