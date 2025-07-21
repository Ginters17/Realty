import os
import requests
import re
from bs4 import BeautifulSoup
from config.config_reader import SS_BASE_URL, SS_LISTINGS_URL
from services.scraper_storage_service import load_viewed_listings, save_viewed_listings

BUCKET_NAME = "realty-scraper"
SCRAPED_LINKS_FILE = "scraped_links.txt"

def getApartmentListings():
    page_num = 1
    end_reached = False
    all_new_links = set()

    while not end_reached:
        url = getPageUrl(page_num)

        response = requests.get(url)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, "html.parser")

        scraped_links = load_viewed_listings(BUCKET_NAME, SCRAPED_LINKS_FILE)
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
        save_viewed_listings(all_new_links, BUCKET_NAME, SCRAPED_LINKS_FILE, "a")
    else:
        save_viewed_listings(all_new_links, BUCKET_NAME, SCRAPED_LINKS_FILE, "w")

    enrichedListings = [enrichLink(link) for link in all_new_links]
    return list(enrichedListings)

def getPageUrl(page_num):
    if page_num == 1:
        return SS_LISTINGS_URL
    else:
        base_url = SS_LISTINGS_URL.rsplit('/', 1)[0]
        return f"{base_url}/page{page_num}.html"

def enrichLink(link):
    response = requests.get(link)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, "html.parser")

    price = extractPrice(soup)
    rooms = extractRooms(soup)
    size = extractSize(soup)
    district = extractDistrict(soup)
    image_url = extractImageUrl(soup)

    return {
        "link": link,
        "price": price,
        "rooms": rooms,
        "size": size,
        "district": district,
        "imageUrl": image_url
    }

def extractPrice(soup):
    price_text = soup.select_one(".ads_price").text.strip().replace('\xa0', ' ')
    match = re.search(r"(\d+)", price_text)
    if match:
        return int(match.group(1))
    return None

def extractRooms(soup):
    rooms_cell = soup.select_one("#tdo_1")
    if rooms_cell:
        rooms_text = rooms_cell.text.strip()
        try:
            return int(rooms_text)
        except ValueError:
            return None
    return None

def extractSize(soup):
    area_cell = soup.select_one("#tdo_3")
    if area_cell:
        area_text = area_cell.text.strip()
        match = re.search(r"(\d+)", area_text)
        if match:
            return int(match.group(1))
    return None

def extractDistrict(soup):
    rajons_cell = soup.select_one("#tdo_856")
    if rajons_cell:
        return rajons_cell.text.strip()
    return None

def extractImageUrl(soup):    
    img_tag = soup.select_one("img.pic_thumbnail.isfoto")
    if img_tag and img_tag.get("src"):
        img_url = img_tag["src"]
        if img_url.startswith("/"):
            img_url = "https://www.ss.com" + img_url
        return img_url
    return None