from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def greet():
    return "Welcome to the Market Data API!"


@app.get("/symbols/{symbol}/annual/{year}")
def get_market_data(symbol: str, year: int):
    # TODO implementation 
    return {"symbol": symbol, "year": year}