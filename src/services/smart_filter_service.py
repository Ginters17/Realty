from config.ConfigReader import UNWANTED_DISTRICTS, LISTING_MIN_PRICE, LISTING_MAX_PRICE

# TODO - Add AI, add room filter
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