#!/usr/bin/env python3

import requests
import re
import os
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def get_pdf_links(url):
    try:
        r = requests.get(url)
        r.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching URL: {e}")
        return []

    soup = BeautifulSoup(r.content, 'html.parser')
    pattern = re.compile(r'\.pdf$', re.IGNORECASE)
    links = []

    for link in soup.find_all('a'):
        href = link.get('href')
        if href and pattern.search(href):
            full_url = urljoin(url, href)  # handle relative URLs
            links.append(full_url)

    return links

def download_file(url, folder='.'):
    local_filename = os.path.join(folder, url.split('/')[-1])
    try:
        with requests.get(url, stream=True) as r:
            r.raise_for_status()
            with open(local_filename, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
        print(f"Downloaded: {local_filename}")
    except Exception as e:
        print(f"Failed to download {url}: {e}")

def main():
    url = input("Enter the website URL to scrape for PDFs: ").strip()
    pdf_links = get_pdf_links(url)

    if not pdf_links:
        print("No PDF links found.")
        return

    print("\nPDF files found:")
    for i, link in enumerate(pdf_links):
        print(f"{i+1}: {link}")

    choices = input("\nEnter the number(s) of the PDF(s) to download (e.g., 1 or 1,3,5): ")
    indices = set()
    for part in choices.split(','):
        part = part.strip()
        if part.isdigit():
            idx = int(part) - 1
            if 0 <= idx < len(pdf_links):
                indices.add(idx)

    if not indices:
        print("No valid selections made.")
        return

    for i in sorted(indices):
        download_file(pdf_links[i])

if __name__ == "__main__":
    main()

