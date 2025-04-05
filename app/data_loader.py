import requests
from bs4 import BeautifulSoup
import time
import pickle
import os

BASE_URL = "https://www.shl.com/solutions/"
CATALOG_URL = f"{BASE_URL}/products/product-catalog/"

HEADERS = {
    "User-Agent":"Mozilla/5.0"
}

def get_assessment_links():
    """Scrapes the man assessment page and gets all individual assessment URLs"""
    res = requests.get(CATALOG_URL,headers=HEADERS)
    soup = BeautifulSoup(res.text,'html.parser')

    links = []

    for a in soup.find_all("a",href=True):
        href = a['href']
        if "/products/product-catalog/" in href and href.count("/") > 3:
            full_url = BASE_URL + href if href.startswith("/") else href
            if full_url not in links:
                links.append(full_url)

    return list(set(links))

def scrape_assessment_page(url):
    """Scrapes details from an individual assessment page"""
    res = requests.get(url,headers=[HEADERS])
    soup = BeautifulSoup(res.text,'html.parser')

    title = soup.find("h1")
    desc = soup.find("p")

    return {
        "url" : url,
        "title" : title.get_text(strip=True) if title else "No Title",
        "description" : desc.get_text(strip=True) if desc else "No Description"
    }

def scrape_all_assessment():
    """Main function to scrape the entire SHL catalog"""
    links = get_assessment_links()
    print(f"Found {len(links)} assessment pages.")

    all_data = []

    for i, link in enumerate(links):
        try:
            data = scrape_assessment_page(link)
            all_data.append(data)
            print(f"[{i+1}/{len(links)}] Scraped : {data['title']}")
            time.sleep(1)

        except Exception as ex:
            print(f"Error Scraping {link} : {ex}")

    #Save metadata to pickle
    os.makedirs("faiss_index", exist_ok=True)
    with open("faiss_index/metadata.pkl", "wb") as f:
        pickle.dump(all_data,f)

    print("✅ Saved metadata to faiss_index/metadata.pkl")
    return all_data


