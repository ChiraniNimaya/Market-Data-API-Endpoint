import requests
from config import API_KEY, API_URL


def fetch_monthly_data(symbol: str) -> dict:
    params = {
        "symbol": symbol,
        "apikey": API_KEY,
    }

    response = requests.get(API_URL, params=params)
    response.raise_for_status()
    data = response.json()

    if "Error Message" in data:
        raise ValueError(f"Invalid symbol '{symbol}'")

    if "Information" in data:
        raise ValueError("API rate limit reached")

    if "Monthly Time Series" not in data:
        raise ValueError(f"Unexpected response: {data}")

    return data["Monthly Time Series"]