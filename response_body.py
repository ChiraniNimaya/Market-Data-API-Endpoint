def annual_market_data_response(max_high: float, min_low: float, annual_volume: int) -> dict:
    return {
            "high": max_high,
            "low": min_low,
            "volume": annual_volume
        }