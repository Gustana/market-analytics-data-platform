from pydantic import BaseModel, ConfigDict

from ..common_response import PaginationRecords

class _EodRecord(BaseModel):
    open: float
    high: float
    low: float
    close: float | None = None
    volume: float
    name: str
    exchange_code: str | None = None
    price_currency: str
    date: str

class EodResponse(BaseModel):
    model_config = ConfigDict(frozen=True)

    pagination: PaginationRecords
    data: list[_EodRecord]