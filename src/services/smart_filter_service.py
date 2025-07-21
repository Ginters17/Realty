from config.config_reader import UNWANTED_DISTRICTS, LISTING_MIN_PRICE, LISTING_MAX_PRICE, LISTING_MIN_SIZE, LISTING_MAX_SIZE, LISTING_MIN_ROOMS, LISTING_MAX_ROOMS, LISTING_MIN_PRICE_PER_M2

# TODO - Add AI, add room filter
def filterListings(listings):
    filteredListings = []

    for listing in listings:
        # Area filter]
        if any(unwanted in listing['link'] for unwanted in UNWANTED_DISTRICTS):
            continue

        # Price filter
        if not (LISTING_MIN_PRICE <= listing['price'] <= LISTING_MAX_PRICE):
            continue

        # Size filter
        if not (LISTING_MIN_SIZE <= listing['size'] <= LISTING_MAX_SIZE):
            continue

        # Room filter
        if not (LISTING_MIN_ROOMS <= listing['rooms'] <= LISTING_MAX_ROOMS):
            continue

        # Price per m2 filter
        if (float(listing['price']) / float(listing['size']) < LISTING_MIN_PRICE_PER_M2):
            continue

        # Passed all filters
        filteredListings.append(listing)

    return filteredListings