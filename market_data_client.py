import httpx
from config import API_KEY, API_URL, EXTERNAL_REQUEST_TIMEOUT


async def fetch_monthly_data(symbol: str) -> dict:
    params = {
        "function": "TIME_SERIES_MONTHLY",
        "symbol": symbol,
        "apikey": API_KEY,
    }

    async with httpx.AsyncClient(timeout=EXTERNAL_REQUEST_TIMEOUT) as client:
        try:
            response = await client.get(API_URL, params=params)
            response.raise_for_status()
        except httpx.TimeoutException:
            raise RuntimeError("Data source request timed out")
        except httpx.HTTPStatusError as e:
            raise RuntimeError(f"Data source returned HTTP {e.response.status_code}")
        except httpx.RequestError as e:
            raise RuntimeError(f"Network error reaching Data Source: {e}")
    try:
         data = response.json()
    except Exception as e:
        raise ValueError(f"Invalid JSON response from Data Source: {e}") from e

    if "Error Message" in data:
        raise ValueError(f"Invalid symbol '{symbol}'")

    if "Information" in data:
        raise ValueError(f"API rate limit reached")
    
    if "Note" in data:
        raise ValueError(f"Error Note: {data['Note']}")

    if "Monthly Time Series" not in data:
        raise ValueError(f"Unexpected response: {data}")

    return data["Monthly Time Series"]