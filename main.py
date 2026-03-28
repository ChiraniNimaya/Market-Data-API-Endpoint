from fastapi import FastAPI, HTTPException, Request
from contextlib import asynccontextmanager
from pydantic_core import ValidationError
from slowapi import Limiter
from slowapi.util import get_remote_address

from config import REQUEST_RATE_LIMIT_PER_MIN
from database import init_db, save_monthly_data, get_annual_data
from market_data_client import fetch_monthly_data
from validation import MarketDataRequest

limiter = Limiter(key_func=get_remote_address)

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
        return result
    try:
        monthly_series = await fetch_monthly_data(params.symbol)
        save_monthly_data(params.symbol, monthly_series)

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