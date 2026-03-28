from fastapi import FastAPI, HTTPException, Request
from contextlib import asynccontextmanager
from pydantic_core import ValidationError
from slowapi import Limiter
from slowapi.util import get_remote_address
import logging

from config import REQUEST_RATE_LIMIT_PER_MIN
from database import init_db, save_monthly_data, get_annual_data
from market_data_client import fetch_monthly_data
from validation import MarketDataRequest

limiter = Limiter(key_func=get_remote_address)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s"
)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        init_db()
    except RuntimeError as e:
        raise RuntimeError(f"Failed to initialize database: {e}") from e
    yield

app = FastAPI(lifespan=lifespan)

@app.get("/")
def greet():
    return "Welcome to the Market Data API!"


@app.get("/symbols/{symbol}/annual/{year}")
@limiter.limit(REQUEST_RATE_LIMIT_PER_MIN)
async def get_market_data(request: Request, symbol: str, year: int):
    try:
        params = MarketDataRequest(symbol=symbol, year=year)
    except ValidationError as e:
        raise HTTPException(status_code=422, detail=e.errors())
    
    result = get_annual_data(params.symbol, params.year)
    if result:
        logger.info(f"Data was found from local cache for symbol='{params.symbol}' year={params.year}")
        return result
    logger.info(f"Data was not found from local cache for symbol='{params.symbol}' year={params.year}")
    try:
        monthly_series = await fetch_monthly_data(params.symbol)
        logger.info(f"Data fetched from API for symbol='{params.symbol}' year={params.year}")
        
        save_monthly_data(params.symbol, monthly_series)
        logger.info(f"New Data saved to database for symbol='{params.symbol}' year={params.year}")

        result = get_annual_data(params.symbol, params.year)
        if result is None:
            raise HTTPException(
                status_code=404,
                detail=f"No data for '{params.symbol}' in year {params.year}",
            )
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{e} Retry later.")