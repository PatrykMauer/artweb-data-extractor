# link_expander.py

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import time
import os
import tldextract

SEED_FILE = "data/seed_urls.txt"
OUTPUT_FILE = "data/expanded_urls.txt"
MAX_URLS = 2500
CRAWL_DEPTH = 2
ALLOWED_DOMAINS = [".art", ".gallery", ".museum"]
TIMEOUT = 10

visited = set()
discovered = set()


def is_valid_url(url):
    parsed = urlparse(url)
    if parsed.scheme not in ["http", "https"]:
        return False
    # Accept all domains and let content filtering happen later
    return True


def crawl(url, depth):
    if url in visited or len(discovered) >= MAX_URLS:
        return
    try:
        print(f"Crawling: {url} (depth {depth})")
        visited.add(url)
        print(f"Crawling: {url} (depth {depth})")
        visited.add(url)
        resp = requests.get(url, timeout=TIMEOUT)
        if resp.status_code != 200:
            return

        soup = BeautifulSoup(resp.text, "html.parser")
        body_text = soup.get_text(" ", strip=True).lower()
        image_tags = soup.find_all("img")
        art_keywords = ["art", "gallery", "painting",
                        "sculpture", "exhibition", "canvas", "drawing"]
        has_art_content = len(image_tags) > 0 or any(
            kw in body_text for kw in art_keywords)

        if not has_art_content:
            return
        for a in soup.find_all("a", href=True):
            href = urljoin(url, a["href"])
            # Clean fragments and queries
            href = href.split("#")[0].split("?")[0]

            if is_valid_url(href) and href not in discovered:
                discovered.add(href)
                if depth < CRAWL_DEPTH:
                    crawl(href, depth + 1)

    except Exception as e:
        print(f"Error crawling {url}: {e}")


def main():
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    with open(SEED_FILE, "r", encoding="utf-8") as f:
        seeds = [line.strip() for line in f if line.strip()
                 and not line.startswith("#")]

    for seed in seeds:
        if len(discovered) >= MAX_URLS:
            break
        crawl(seed, depth=0)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        for url in sorted(discovered):
            f.write(url + "\n")

    print(f"Finished. {len(discovered)} unique URLs saved to {OUTPUT_FILE}.")


if __name__ == "__main__":
    main()
