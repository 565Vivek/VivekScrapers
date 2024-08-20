import requests
from bs4 import BeautifulSoup
import urllib.parse

def scrape_idaho():
    base_url = "https://legislature.idaho.gov/"
    main_url = "https://legislature.idaho.gov/statutesrules/idstat/"
    response = requests.get(main_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    table = soup.find("table")
    if table:
        links = table.find_all('a', href=True)
        
        for title in links:
            title_href = title['href']
            title_url = urllib.parse.urljoin(base_url, title_href.lstrip('/'))
            
            titles_response = requests.get(title_url)
            titles_soup = BeautifulSoup(titles_response.content, 'html.parser')
            titles_table = titles_soup.find("table")
            
            if titles_table:
                chapters = titles_table.find_all('a', href=True)
                
                for chap in chapters:
                    chap_href = chap['href']
                    chap_url = urllib.parse.urljoin(base_url, chap_href.lstrip('/'))
                    print(f"Chapter URL: {chap_url}")
                    
                    chap_response = requests.get(chap_url)
                    chap_soup = BeautifulSoup(chap_response.content, 'html.parser')
                    chap_table = chap_soup.find("table")
                    
                    if chap_table:
                        sub_chapters = chap_table.find_all('a', href=True)
                        
                        for sub_chap in sub_chapters:
                            sub_chap_href = sub_chap['href']
                            sub_chap_url = urllib.parse.urljoin(base_url, sub_chap_href.lstrip('/'))
                            
                            sub_chap_response = requests.get(sub_chap_url)
                            sub_chap_soup = BeautifulSoup(sub_chap_response.content, 'html.parser')
                            sub_chap_content = sub_chap_soup.find("div", style="line-height: 12pt; text-align: justify; text-indent: 5.9%; padding-top: 12pt")
                            
                            if sub_chap_content:
                                print(sub_chap_content.text.strip())             
scrape_idaho()