# Market-Data-API-Endpoint
A simple REST API that can fetch market data from a 3rd party REST API, cache it locally and serve requests from a client

## Quick Start

### 1. Clone the repository

```sh
git clone <repo-url>
cd Market-Data-API-Endpoint
```

### 2. Set up Python environment (recommended)

```sh
python -m venv mdenv
mdenv\Scripts\activate  # On Windows
source mdenv/bin/activate  # On Linux/Mac
```

### 3. Install dependencies

```sh
pip install fastapi uvicorn httpx slowapi python-dotenv
```

### 4. Create a `.env` file in the project root

Sample `.env`:

```
# Your AlphaVantage API key
API_KEY=your_api_key_here

# Database path
DB_PATH="market.db"

# 3rd party API URL
ALPHAVANTAGE_URL="https://www.alphavantage.co/query?function={function}&symbol={symbol}&apikey={API_KEY}"
```

**Note:** Never commit your real API keys to version control.

### 5. Run the API server

```sh
uvicorn main:app --reload
```

### The API will be available locally at: 
http://localhost:8000/

### Test the endpoint in Swagger:
http://localhost:8000/docs

### Annual data request results can be triggered using : 
http://localhost:8000/symbols/{symbol}/annual/{year}

---

## How it works

- On startup, the app initializes the SQLite database (table is created if not exists).
- When a client requests market data, first check in local cache and show results at endpoint
- If data is not present locally, the API fetches from the external provider (using your API key), caches results, and serves from cache if available.
    eg: http://localhost:8000/symbols/IBM/annual/2024
- Rate limiting is enforced to avoid API abuse.

---

## Limitations & Future Improvements
- Enforce HTTPS for secure data transactions
- Add frontend and CORS handling
- Implement secure authentication and authorization
- Use an ORM for more efficient DB handling

---

## Libraries Used
- **FastAPI**: Web framework
- **Uvicorn**: ASGI server
- **httpx**: Async HTTP requests
- **slowapi**: Rate limiting
- **python-dotenv**: Load environment variables from `.env` file