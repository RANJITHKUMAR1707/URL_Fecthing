from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from urllib.parse import urljoin
import time


def fetch_all_urls(base_url):
    # Set up the WebDriver (Chrome in this case)
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)

    try:
        # Navigate to the base URL
        driver.get(base_url)

        # Give the page some time to load
        time.sleep(10)  # Adjust the sleep time as needed

        # Handle dynamic content (e.g., clicking "load more" buttons)
        try:
            while True:
                button = driver.find_element(By.ID, 'load-more-button')
                button.click()
                time.sleep(3)  # Adjust as needed to allow content to load
        except:
            print("No more 'load more' buttons found or button not present")

        # Handle iframes
        urls = set()
        iframes = driver.find_elements(By.TAG_NAME, 'iframe')
        for iframe in iframes:
            driver.switch_to.frame(iframe)
            urls.update(extract_links(driver, base_url))
            driver.switch_to.default_content()

        # Extract URLs from the main content
        urls.update(extract_links(driver, base_url))

        return list(urls)
    finally:
        # Close the WebDriver
        driver.quit()


def extract_links(driver, base_url):
    # Extract URLs and resolve relative URLs
    anchor_tags = driver.find_elements(By.TAG_NAME, 'a')
    urls = {urljoin(base_url, tag.get_attribute('href')) for tag in anchor_tags if tag.get_attribute('href')}

    return urls


# Example usage
base_url = 'https://mc-eab249be-4eef-4b5b-8f9c-232320-cd.azurewebsites.net/en/site-index'
urls = fetch_all_urls(base_url)
url_count = len(urls)

print(f'Total number of URLs fetched: {url_count}')
for url in urls:
    print(url)
