from TelegramNotificationService import sendTelegramMessage
from ScraperService import getApartmentListings
from SmartFilterService import filterListings

def main():
    print("🔍 Scraping listings...")
    listings = getApartmentListings()
    print(f"Scraped {len(listings)} new listings.")
    filteredListings = filterListings(listings)
    print(f"Found {len(filteredListings)} new listings with matching criteria.")
    
    for listing in filteredListings:
        sendTelegramMessage(listing)

if __name__ == "__main__":
    main()
