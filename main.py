from seleniumbase import Driver
from selenium.webdriver.common.by import By
import pandas as pd
import os
import csv
from urllib.parse import quote_plus
from concurrent.futures import ThreadPoolExecutor
from adb_handler import ADB
from datetime import datetime

adb = ADB()

def file_name() -> str:
    date = datetime.now()
    value = date.strftime("%Y-%m-%dT%H-%M-%S")
    return "data_" + value + ".csv"


chrome_options = [  
            "--incognito", 
            "--disable-extensions",  
            "--disable-popup-blocking",  
            "--blink-settings=imagesEnabled=false",  
            "--disable-dev-shm-usage",  
        ]


class Scraper:
    def __init__(self):
        self.driver = Driver(
            uc=True,  # Enable undetected ChromeDriver
            #page_load_strategy="eager",  # Load page faster
            #chromium_arg=chrome_options  # Pass Chrome arguments correctly
        )

        self.filename = file_name()

    def file_creator(self, company: str, designation: str, location: str, links: list[str]):
        with open(self.filename, 'a', newline='') as f:
            writer = csv.writer(f , quoting=csv.QUOTE_MINIMAL)
            writer.writerow([f"{company} {designation} {location}", str(links)])
            
    def open_google(self, row):
        company = row["Company"]
        designation = row['Designation']
        location = row["Location"]
        search_query = f'site:linkedin.com {company} {designation} {location}'
        encoded_query = quote_plus(search_query)

        print(f'Scraping Data For: {company} | {designation} | {location}')

        try:
            self.driver.get(f'https://www.google.com/search?q={encoded_query}') 
        except Exception as e:
            print(f"Error Occured while opening google")
            return

        current_url = self.driver.current_url

        if current_url.startswith("https://www.google.com/sorry/index?continue"):
            captcha = True
        else:
            captcha = False

        if captcha:
            print('Captcha Found | Changing IP')
            self.driver.quit()
            adb.toggle_internet()
            self.driver = Driver(uc=True)
            self.open_google(row)
             
        try:
            search_results = self.driver.find_elements(By.CSS_SELECTOR, "a")
        except Exception:
            print(f'Error occurred while opening Google:')
            return

        links = []
        
        for result in search_results:
            try:
                href = result.get_attribute("href")
                if href and href.startswith("https://in.linkedin.com/in/"):
                    links.append(href)
            except Exception as e:
                print(f"Links not found in the page")
            
        self.file_creator(company, designation, location, links[:5])


if __name__ == "__main__":
    filename = "input.csv"
    if not os.path.exists(filename):
        print("Error: Input File not Found | Exiting")
    else:
        df = pd.read_csv(filename, encoding="ISO-8859-1").fillna("")

        scraper = Scraper()

        for idx, row in enumerate(df.iterrows()):
                _, row_data = row
                scraper.open_google(row_data)
