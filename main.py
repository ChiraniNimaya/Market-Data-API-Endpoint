from fastapi import FastAPI, HTTPException
import requests
from contextlib import asynccontextmanager
from database import init_db, save_monthly_data, get_annual_data
from market_data_client import fetch_monthly_data

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(lifespan=lifespan)

@app.get("/")
def greet():
    return "Welcome to the Market Data API!"


@app.get("/symbols/{symbol}/annual/{year}")
async def get_market_data(symbol: str, year: int):
    result = get_annual_data(symbol, year)
    if result:
        return result
    try:
        monthly_series = fetch_monthly_data(symbol)
        save_monthly_data(symbol, monthly_series)

        result = get_annual_data(symbol, year)
        if result is None:
            raise HTTPException(
                status_code=404,
                detail=f"No data for '{symbol.upper()}' in year {year}",
            )

        return result

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))