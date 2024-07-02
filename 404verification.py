import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time


def read_urls_from_excel(file_path, sheet_name):
    """Reads URLs from an Excel file."""
    df = pd.read_excel(file_path, sheet_name=sheet_name)
    return df['URL'].tolist()


def is_element_present(url, by, value, driver):
    """Checks if an element is present on the web page at the given URL using an existing WebDriver."""
    try:
        driver.get(url)
        time.sleep(5)  # Wait for the page to fully load

        driver.find_element(by, value)
        return True
    except NoSuchElementException:
        return False


def process_urls(urls, by, value, output_file_path):
    """Processes the URLs and checks for the presence of the element."""
    results = []
    driver = webdriver.Chrome()  # Initialize the WebDriver once

    for i, url in enumerate(urls):
        try:
            element_present = is_element_present(url, by, value, driver)
            results.append({'URL': url, '404 found': element_present})
        except Exception as e:
            print(f"Error processing {url}: {e}")
            results.append({'URL': url, 'Element Present': 'Error'})

        # Save intermediate results after each URL
        write_results_to_excel(results, output_file_path)

    driver.quit()  # Quit the WebDriver after processing all URLs
    return results


def write_results_to_excel(results, output_file_path):
    """Writes the results to an Excel file."""
    df = pd.DataFrame(results)
    df.to_excel(output_file_path, index=False)


def main():
    input_file_path = 'C:\\Users\\ranjithkumar.sivakum\\Downloads\\URL_List.xlsx'
    sheet_name = 'Sheet1'
    element_xpath = "//label[contains(text(),'Sorry,')]"
    output_file_path = '110_URL_results.xlsx'

    urls = read_urls_from_excel(input_file_path, sheet_name)
    process_urls(urls, By.XPATH, element_xpath, output_file_path)


if __name__ == '__main__':
    main()
