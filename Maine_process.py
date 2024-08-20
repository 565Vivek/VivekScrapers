import requests
from bs4 import BeautifulSoup
import urllib.parse
import re

def clean_text(text):
    # Remove multiple newlines and leading/trailing whitespace
    cleaned_text = re.sub(r'\n+', '\n', text)  # Replace multiple newlines with a single newline
    cleaned_text = re.sub(r'[ \t]+', ' ', cleaned_text)  # Replace multiple spaces/tabs with a single space
    cleaned_text = cleaned_text.strip()  # Remove leading/trailing whitespace
    return cleaned_text

def scrape_maine():
    base_url = "https://legislature.maine.gov/"
    main_url = "https://legislature.maine.gov/statutes/"
    response = requests.get(main_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    titles = soup.find("ul", class_="title_list").find_all('a', href=True)
    
    for title in titles:
        title_href = title['href']
        title_url = urllib.parse.urljoin(main_url, title_href.lstrip('/'))
        
        titles_response = requests.get(title_url)
        titles_soup = BeautifulSoup(titles_response.content, 'html.parser')
        chapters = titles_soup.find("div", class_="title_toc MRSTitle_toclist col-sm-10").find_all('a', href=True)
        
        for chap in chapters:
            trimmed_url = title_url.split("title")[0]
            chap_href = chap['href']
            chap_url = urllib.parse.urljoin(trimmed_url, chap_href.lstrip('/'))

            chap_response = requests.get(chap_url)
        
            chap_soup = BeautifulSoup(chap_response.content, 'html.parser')
            sub_chapters = chap_soup.find("div", class_="chapter_toclist col-sm-10").find_all('a', href=True)
            
            for sub_chap in sub_chapters:
                sub_chap_href = sub_chap['href']
                sub_chap_url = urllib.parse.urljoin(trimmed_url, sub_chap_href.lstrip('/'))
                
                sub_chap_response = requests.get(sub_chap_url)
                sub_chap_soup = BeautifulSoup(sub_chap_response.content, 'html.parser')
                sub_chap_content = sub_chap_soup.find("div", class_="col-sm-12 MRSSection status_current").get_text()
                print(clean_text(sub_chap_content))

scrape_maine()