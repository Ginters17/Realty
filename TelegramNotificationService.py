import requests
from ConfigReader import TELEGRAM_TOKEN, TELEGRAM_CHAT_ID, TELEGRAM_SERVICE

def sendTelegramMessage(apt):
    message = (
        f"🏠 *New Apartment Found!*\n"
        f"District: *{apt['district'].title()}*\n"
        f"Price: *{apt['price']} EUR*\n"
        f"Rooms: *{apt['rooms']}*\n"
        f"Size: *{apt['size']} m²*\n"
        f"🔗 [View Listing]({apt['link']})"
    )
    
    if TELEGRAM_SERVICE == "real":
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
