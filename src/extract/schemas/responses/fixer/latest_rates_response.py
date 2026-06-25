from datetime import date
from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field

from src.extract.schemas.responses.common_response import FixerErrorRecord

class _LatestRatesSuccess(BaseModel):
    model_config = ConfigDict(frozen=True)

    success: bool
    base: str
    date: date
    rates: dict[str, float]

class _LatestRatesFailure(BaseModel):
    model_config = ConfigDict(frozen=True)

    success: bool
    error: FixerErrorRecord

LatestRatesResponse = Annotated[
    _LatestRatesSuccess | _LatestRatesFailure,
    Field(discriminator='success')
]