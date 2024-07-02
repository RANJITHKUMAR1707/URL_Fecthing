from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from urllib.parse import urljoin, urlparse
import time
import json


def fetch_all_urls(base_url, target_prefix):
    # Set up the WebDriver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)

    visited_urls = set()
    urls_to_visit = {base_url}
    all_urls = set()

    def extract_links(current_url):
        # Navigate to the current URL
        driver.get(current_url)
        time.sleep(5)  # Adjust the sleep time as needed

        # Handle dynamic content (e.g., clicking "load more" buttons)
        try:
            while True:
                button = driver.find_element(By.ID, 'load-more-button')
                button.click()
                time.sleep(3)  # Adjust as needed to allow content to load
        except:
            pass  # No more "load more" buttons or button not present

        # Extract URLs from the main content and iframes
        all_urls.update(extract_links_from_page(driver, current_url))

    def extract_links_from_page(driver, base_url):
        anchor_tags = driver.find_elements(By.TAG_NAME, 'a')
        urls = {urljoin(base_url, tag.get_attribute('href')) for tag in anchor_tags if tag.get_attribute('href')}
        return {url for url in urls if url.startswith(target_prefix)}

    def save_progress():
        with open('urls_progress.json', 'w') as file:
            json.dump(list(all_urls), file)
        print(f'Saved progress with {len(all_urls)} URLs')

    def save_urls_to_txt(urls, filename='urls.txt'):
        with open(filename, 'w') as file:
            for url in sorted(urls):
                file.write(url + '\n')

    try:
        while urls_to_visit:
            current_url = urls_to_visit.pop()
            if current_url not in visited_urls:
                visited_urls.add(current_url)
                extract_links(current_url)
                for url in all_urls:
                    if url.startswith(target_prefix) and url not in visited_urls:
                        urls_to_visit.add(url)

                # Periodically save progress
                if len(visited_urls) % 10 == 0:  # Adjust the frequency as needed
                    save_progress()

        return all_urls
    except Exception as e:
        print(f'Error occurred: {e}')
        save_progress()
        raise
    finally:
        # Ensure the WebDriver is closed
        driver.quit()
        # Save final URLs to text file
        save_urls_to_txt(all_urls)


# Example usage
base_url = 'https://coats.com/en/'
target_prefix = 'https://coats.com/en/'
urls = fetch_all_urls(base_url, target_prefix)
url_count = len(urls)

print(f'Total number of unique URLs fetched: {url_count}')
for url in urls:
    print(url)
