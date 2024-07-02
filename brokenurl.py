import requests
from bs4 import BeautifulSoup
import re


def extract_urls_from_page(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        urls = set()
        for link in soup.find_all('a', href=True):
            href = link['href']
            # Ensure URLs are absolute
            if href.startswith('/'):
                href = url + href
            if re.match(r'^https?://', href):
                urls.add(href.rstrip('/'))
        return urls
    except Exception as e:
        print(f"Error crawling {url}: {e}")
        return set()


def crawl_website(base_url):
    urls_to_crawl = {base_url}
    crawled_urls = set()
    all_urls = set()

    while urls_to_crawl:
        url = urls_to_crawl.pop()
        if url not in crawled_urls:
            print(f"Crawling: {url}")
            urls = extract_urls_from_page(url)
            all_urls.update(urls)
            crawled_urls.add(url)
            urls_to_crawl.update(urls - crawled_urls)
    return all_urls


def check_broken_links(urls):
    broken_links = []
    for url in urls:
        try:
            response = requests.head(url, allow_redirects=True)
            if response.status_code >= 400:
                broken_links.append((url, response.status_code))
        except requests.RequestException as e:
            print(f"Error checking {url}: {e}")
            broken_links.append((url, 'Error'))
    return broken_links


source_base_url = 'https://coats.com/en/'
source_urls = crawl_website(source_base_url)

print(f"Found {len(source_urls)} URLs on source website.")

broken_links = check_broken_links(source_urls)

if broken_links:
    print("Broken links found:")
    for url, status in broken_links:
        print(f"{url} returned status code {status}")
else:
    print("No broken links found.")
