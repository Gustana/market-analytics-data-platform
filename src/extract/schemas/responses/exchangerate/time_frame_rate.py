from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, Field

from src.extract.schemas.responses.common_response import ErrorRecords


class _TimeframeRateSuccess(BaseModel):
    model_config = ConfigDict(frozen=True)

    success: bool = Literal[True]
    start_date: str
    end_date: str
    source: str
    rates: dict[str, dict[str, float]]

class _TimeFrameRateFailure(BaseModel):
    model_config = ConfigDict(frozen=True)

    success: bool = Literal[False]
    error: ErrorRecords

TimeFrameRateResponse = Annotated[
    _TimeframeRateSuccess | _TimeFrameRateFailure,
    Field(discriminator='success')
]