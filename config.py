from dotenv import load_dotenv
import os

EXTERNAL_REQUEST_TIMEOUT = 15 #seconds

load_dotenv()

API_KEY = os.getenv("API_KEY")
DB_PATH = os.getenv("DB_PATH", "market.db")
API_URL = os.getenv("ALPHAVANTAGE_URL")