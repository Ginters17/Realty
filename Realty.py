import requests
from bs4 import BeautifulSoup
import re
from TelegramNotificationService import sendTelegramMessage
from ScraperService import getApartmentLinks
from config import UNWANTED_DISTRICTS, LISTING_MIN_PRICE, LISTING_MAX_PRICE

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

def filterLinks(links):
    filteredLinks = []

    for link in links:
        # Area filter
        skip = False
        for unwantedDistrict in UNWANTED_DISTRICTS:
            if unwantedDistrict in link:
                skip = True
                break
        if skip:
            continue

        # Price filter
        response = requests.get(link)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, "html.parser")
        price = extractPrice(soup)
        rooms = extractRooms(soup)
        size = extractSize(soup)
        district = extractDistrict(soup)

        if LISTING_MIN_PRICE <= price <= LISTING_MAX_PRICE:
            filteredLinks.append({
                "link": link,
                "price": price,
                "rooms": rooms,
                "size": size,
                "district": district
            })

    return filteredLinks



def main():
    print("🔍 Scraping listings...")
    links = getApartmentLinks()
    filteredApartments = filterLinks(links)
    print(f"Found {len(filteredApartments)} listings with matching criteria.")
    
    for apt in filteredApartments:
        sendTelegramMessage(apt)

if __name__ == "__main__":
    main()
