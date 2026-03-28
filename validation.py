from pydantic import BaseModel, field_validator
import datetime
from config import SYMBOL_MAX_LENGTH


class MarketDataRequest(BaseModel):
    symbol: str
    year: int

    @field_validator("symbol")
    @classmethod
    def symbol_must_be_valid(cls, value: str) -> str:
        if not value.isalpha():
            raise ValueError("Symbol must contain letters only")
        if len(value) > SYMBOL_MAX_LENGTH:
            raise ValueError(f"Symbol must be {SYMBOL_MAX_LENGTH} characters or fewer")
        return value.upper()

    @field_validator("year")
    @classmethod
    def year_must_be_valid(cls, value: int) -> int:
        if value < 0:
            raise ValueError("Year must be non negative")
        if len(str(value)) != 4:
            raise ValueError("Year must be a 4 digit number")
        if value > datetime.datetime.now().year:
            raise ValueError("Year cannot be in the future")
        return value