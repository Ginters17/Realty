from dotenv import load_dotenv
import os

load_dotenv()

def get_env_list(name, default=""):
    return [x.strip().lower() for x in os.getenv(name, default).split(",") if x.strip()]

def get_env_int(name):
    return int(os.getenv(name))

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
TELEGRAM_SERVICE = os.getenv("TELEGRAM_SERVICE", "mock")
SS_BASE_URL = os.getenv("SS_BASE_URL")
SS_LISTINGS_URL = os.getenv("SS_LISTINGS_URL")
UNWANTED_DISTRICTS = get_env_list("UNWANTED_DISTRICTS")
LISTING_MIN_PRICE = get_env_int("LISTING_MIN_PRICE")
LISTING_MAX_PRICE = get_env_int("LISTING_MAX_PRICE")