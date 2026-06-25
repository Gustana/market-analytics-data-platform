from datetime import date
from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field

from src.extract.schemas.responses.common_response import FixerErrorRecord

class _HistoricalRatesSuccess(BaseModel):
    model_config = ConfigDict(frozen=True)

    success: bool
    date: date
    base: str
    rates: dict[str, float]

class _HistoricalRatesBadFailure(BaseModel):
    model_config = ConfigDict(frozen=True)

    success: bool
    error: FixerErrorRecord

HistoricalRatesResponse = Annotated[
    _HistoricalRatesSuccess | _HistoricalRatesBadFailure,
    Field(discriminator='success')
]