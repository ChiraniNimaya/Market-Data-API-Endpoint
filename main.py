from fastapi import FastAPI, HTTPException
import requests
from contextlib import asynccontextmanager
from database import init_db

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(lifespan=lifespan)

@app.get("/")
def greet():
    return "Welcome to the Market Data API!"


@app.get("/symbols/{symbol}/annual/{year}")
def get_market_data(symbol: str, year: int):
    # TODO implementation 
    return {"symbol": symbol, "year": year}