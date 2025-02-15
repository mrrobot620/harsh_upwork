from seleniumbase import Driver
from selenium.webdriver.common.by import By
import pandas as pd
import os
import csv
from urllib.parse import quote_plus
from concurrent.futures import ThreadPoolExecutor


class Scraper:
    def __init__(self, driver):
        self.driver = driver

    def read_file(self, filename: str):
        if not os.path.exists(filename):
            print("Error: Input File not Found | Exiting")
            return None
        df = pd.read_csv(filename)
        return df.fillna("")

    def file_creator(self, company: str, designation: str, location: str, links: list[str]):
        with open('data.csv', 'a', newline='') as f:
            writer = csv.writer(f)
            for link in links:
                writer.writerow([company, designation, location, link])

    def open_google(self, row):
        company = row["Company"]
        designation = row['Designation']
        location = row["Location"]
        search_query = f'site:linkedin.com/in {company} {designation} {location}'
        encoded_query = quote_plus(search_query)

        print(f'Scraping Data For: {company} | {designation} | {location}')

        self.driver.get(f'https://www.google.com/search?q={encoded_query}')

        try:
            captcha = self.driver.find_elements(By.ID, "captcha-form")
        except Exception:
            pass

        if captcha is not None:
            print(f"Google Captcha Found | Changing Ip")

        try:
            search_results = self.driver.find_elements(By.CSS_SELECTOR, "a")
        except Exception:
            print(f'Error occurred while opening Google:')
            return

        links = [result.get_attribute("href") for result in search_results if result.get_attribute(
            "href") and result.get_attribute("href").startswith('https://in.linkedin.com/')]
        self.file_creator(company, designation, location, links[:5])


def run_scraper(row, driver):
    scraper = Scraper(driver)
    scraper.open_google(row)


if __name__ == "__main__":
    filename = "input.csv"
    if not os.path.exists(filename):
        print("Error: Input File not Found | Exiting")
    else:
        df = pd.read_csv(filename).fillna("")

        drivers = [Driver(uc=True) for _ in range(3)]

        with ThreadPoolExecutor(max_workers=3) as executor:
            futures = []
            for idx, row in enumerate(df.iterrows()):
                _, row_data = row
                driver = drivers[idx % 3]
                futures.append(executor.submit(run_scraper, row_data, driver))

            for future in futures:
                future.result()

        for driver in drivers:
            driver.quit()
