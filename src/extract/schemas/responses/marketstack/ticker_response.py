from datetime import datetime

from pydantic import BaseModel, ConfigDict

class _ExchangeDate(BaseModel):
    date: datetime
    timezone_type: str
    timezone: str


class _StockExchange(BaseModel):
    name: str
    acronym: str
    mic: str
    country: str
    country_code: str
    city: str
    website: str

    date_creation: _ExchangeDate | None = None
    date_last_update: _ExchangeDate | None = None


class TickerResponse(BaseModel):
    model_config = ConfigDict(frozen=True)

    symbol: str
    name: str
    sector: str
    industry: str
    cik: str
    isin: str

    stock_exchange: _StockExchange