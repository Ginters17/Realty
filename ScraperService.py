import requests
from bs4 import BeautifulSoup
from config import SS_BASE_URL, SS_LISTINGS_URL

def getApartmentLinks():
    response = requests.get(SS_LISTINGS_URL)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, "html.parser")
    links = []

    for row in soup.select("tr[id^=tr_] a[href^='/msg/']"):
        href = row.get("href")
        full_url = SS_BASE_URL + href
        links.append(full_url)

    return list(set(links))