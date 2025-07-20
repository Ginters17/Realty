from TelegramNotificationService import sendTelegramMessage
from ScraperService import getApartmentListings
from ConfigReader import UNWANTED_DISTRICTS, LISTING_MIN_PRICE, LISTING_MAX_PRICE

# TODO - Move this to SmartFileService
def filterListings(listings):
    filteredListings = []

    for listing in listings:
        # Area filter - must not be in unwated district
        if any(unwanted in listing['link'] for unwanted in UNWANTED_DISTRICTS):
            continue

        # Price filter - must not be outside price boundaries
        if not (LISTING_MIN_PRICE <= listing['price'] <= LISTING_MAX_PRICE):
            continue

        # Passed all filters
        filteredListings.append(listing)

    return filteredListings

def main():
    print("🔍 Scraping listings...")
    listings = getApartmentListings()
    filteredApartments = filterListings(listings)
    print(f"Found {len(filteredApartments)} new listings with matching criteria.")
    
    for apt in filteredApartments:
        sendTelegramMessage(apt)

if __name__ == "__main__":
    main()
