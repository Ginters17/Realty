import requests
from config.config_reader import TELEGRAM_TOKEN, TELEGRAM_CHAT_ID, TELEGRAM_SERVICE_IMPL

def sendTelegramMessage(apt):
    moreInfoText = createMoreInfoText(apt)
    moreInfoText = f"\n{moreInfoText}" if moreInfoText else ""

    message = (
        f"🏠 *New Apartment Found!*\n"
        f"District: *{apt['district'].title()}*\n"
        f"Price: *{apt['price']} EUR*\n"
        f"Rooms: *{apt['rooms']}*\n"
        f"Floor: *{apt['floor']}*\n"
        f"Size: *{apt['size']} m²*"
        f"{moreInfoText}\n"
        f"🔗 [View Listing]({apt['link']})"
    )
    
    if TELEGRAM_SERVICE_IMPL == "real":
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendPhoto"
        data = {
            "chat_id": TELEGRAM_CHAT_ID,
            "photo": apt['imageUrl'],
            "caption": message,
            "parse_mode": "Markdown"
        }
        response = requests.post(url, data=data)
        if response.status_code == 200:
            print("Successfully sent telegram notification with listing")
        else:
            print(f"Failed to send telegram notification. Error code {response.status_code}, {response.text}")
    else:
        print("Mock telegram service used")

def getHasAnyKeywords(apt):
    return any([
        apt['hasDishWasher'],
        apt['hasRepair'],
        apt['hasFurniture'],
        apt['hasStudioLayout']
    ])

def createMoreInfoText(apt):
    info = []
    if apt["hasDishWasher"]:
        info.append("  ▸ Dishwasher")
    if apt["hasRepair"]:
        info.append("  ▸ Renovated")
    if apt["hasFurniture"]:
        info.append("  ▸ Furnished")
    if apt["hasStudioLayout"]:
        info.append("  ▸ Studio Layout")

    return "Features:\n" + "\n".join(info) if info else ""

