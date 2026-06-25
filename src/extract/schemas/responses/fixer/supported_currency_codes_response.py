from datetime import date
from typing_extensions import Annotated

from pydantic import BaseModel, ConfigDict, Field

from src.extract.schemas.responses.common_response import FixerErrorRecord

class _SupportedCurrencyCodesSuccess(BaseModel):
    model_config = ConfigDict(frozen=True)

    success: bool
    date: date
    rates: dict[str, float]

class _SupportedCurrencyCodesFailure(BaseModel):
    model_config = ConfigDict(frozen=True)

    success: bool
    error: FixerErrorRecord

SupportedCurrencyCodesResponse = Annotated[
    _SupportedCurrencyCodesSuccess | _SupportedCurrencyCodesFailure,
    Field(discriminator='success')
]