import pandas as pd
from requests_html import HTMLSession
from bs4 import BeautifulSoup
import re
import time
from adb_handler import ADB

adb = ADB()

session = HTMLSession()

def get_google_search_results(query):
    query = query.replace(' ', '+')
    url = f'https://www.google.com/search?q={query}'
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    response = session.get(url, headers=headers)
    if response.status_code == 429:
        adb.toggle_internet()
        time.sleep(1)
    return response.text

def extract_linkedin_urls(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    linkedin_urls = []
    
    for a_tag in soup.find_all('a', href=True):
        href = a_tag['href']
        if href:
            if href.startswith("https://in.linkedin.com/in/"):
                linkedin_urls.append(href)
            else:
                print(f"1: {href}")
        else:
            print(f"2: {href}")
    return linkedin_urls


def get_all_linkedin_urls(query):
    all_linkedin_urls = []
    html_content = get_google_search_results(query)
    linkedin_urls = extract_linkedin_urls(html_content)
    all_linkedin_urls.extend(linkedin_urls)
    
    return all_linkedin_urls



input= pd.read_csv("/Users/abhishekrajput/Desktop/harsh_upwork/input.csv" , encoding="ISO-8859-1").fillna(0)

url_list=[]
for i in range(0,len(input)):
    query = "site:linkedin.com " +  input['Company'][i] + " "+input['Designation'][i]+ " "+input['Location'][i]
    print(query)
    num_pages = 1 
    linkedin_urls = get_all_linkedin_urls(query)
    print(linkedin_urls)
    time.sleep(1.5)
    url_list.extend(linkedin_urls)