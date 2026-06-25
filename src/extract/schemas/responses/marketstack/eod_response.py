from pydantic import BaseModel, ConfigDict

from ..common_response import Paggination

class _EodRecord(BaseModel):
    open: int
    high: int
    low: int
    close: int
    volume: int
    name: str
    exchange_code: str
    date: str

class EodResponse(BaseModel):
    model_config = ConfigDict(frozen=True)

    paggination: Paggination
    data: list[_EodRecord]