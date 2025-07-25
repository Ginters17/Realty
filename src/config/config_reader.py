from dotenv import load_dotenv
import os

load_dotenv()

def get_env_list(name, default=""):
    return [x.strip().lower() for x in os.getenv(name, default).split(",") if x.strip()]

def get_env_int(name):
    return int(os.getenv(name))

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
TELEGRAM_SERVICE_IMPL = os.getenv("TELEGRAM_SERVICE_IMPL", "mock")
SS_BASE_URL = os.getenv("SS_BASE_URL")
SS_LISTINGS_URL = os.getenv("SS_LISTINGS_URL")
GCP_SERVICE_ACCOUNT_KEY = os.getenv("GCP_SERVICE_ACCOUNT_KEY")
GCS_SERVICE_IMPL = os.getenv("GCS_SERVICE_IMPL")
UNWANTED_DISTRICTS = get_env_list("UNWANTED_DISTRICTS")
LISTING_MIN_PRICE = get_env_int("LISTING_MIN_PRICE")
LISTING_MAX_PRICE = get_env_int("LISTING_MAX_PRICE")
LISTING_MIN_SIZE = get_env_int("LISTING_MIN_SIZE")
LISTING_MAX_SIZE = get_env_int("LISTING_MAX_SIZE")
LISTING_MIN_ROOMS = get_env_int("LISTING_MIN_ROOMS")
LISTING_MAX_ROOMS = get_env_int("LISTING_MAX_ROOMS")
LISTING_MIN_PRICE_PER_M2 = get_env_int("LISTING_MIN_PRICE_PER_M2")