import os
import requests
from bs4 import BeautifulSoup
from config import SS_BASE_URL, SS_LISTINGS_URL

SCRAPED_LINKS_FILE = "scraped_links.txt"

def loadScrapedLinks():
    if not os.path.exists(SCRAPED_LINKS_FILE):
        return set()
    with open(SCRAPED_LINKS_FILE, "r", encoding="utf-8") as f:
        return set(line.strip() for line in f)

def saveLinks(links, mode="w"):
    with open(SCRAPED_LINKS_FILE, mode, encoding="utf-8") as f:
        for link in links:
            f.write(link + "\n")

def getApartmentLinks():
    page_num = 1
    end_reached = False
    all_new_links = set()

    while not end_reached:
        url = getPageUrl(page_num)

        response = requests.get(url)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, "html.parser")

        scraped_links = loadScrapedLinks()
        new_links = []

        for row in soup.select("tr[id^=tr_]"):
            a_tag = row.select_one("a[href^='/msg/']")
            if a_tag:
                href = a_tag.get("href")
                full_url = SS_BASE_URL + href
                if full_url in scraped_links:
                    end_reached = True
                    break
                else:
                    new_links.append(full_url)

        all_new_links.update(new_links)

        if end_reached or page_num >= 3: # Safe guard lol
            break

        page_num += 1

    # When only few links found append to already scraped links, otherwise overwrite all scraped links.
    # Because if overwrite with e.g. 1 link and it gets removed then will incorrectly scrape all pages.
    if len(all_new_links) < 3:
        saveLinks(list(all_new_links), mode="a")
    else:
        saveLinks(list(all_new_links), mode="w")

    print(f"Scraped {len(all_new_links)} new listings.")
    return list(all_new_links)

def getPageUrl(page_num):
    if page_num == 1:
        return SS_LISTINGS_URL
    else:
        base_url = SS_LISTINGS_URL.rsplit('/', 1)[0]
        return f"{base_url}/page{page_num}.html"
