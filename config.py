from dotenv import load_dotenv
import os

EXTERNAL_REQUEST_TIMEOUT = 15 #seconds
REQUEST_RATE_LIMIT_PER_MIN = "10/minute"
SYMBOL_MAX_LENGTH = 10
DB_PATH="market.db"
ALPHAVANTAGE_URL=f"https://www.alphavantage.co/query?function={function}&symbol={symbol}&apikey={API_KEY}"

load_dotenv()
API_KEY = os.getenv("API_KEY")