from services.telegram_notification_service import sendTelegramMessage
from services.scraper_service import getApartmentListings
from services.smart_filter_service import filterListings

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
