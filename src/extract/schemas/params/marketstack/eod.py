from datetime import date
from typing import Literal

from pydantic import BaseModel, Field, ConfigDict

class EodParam(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    symbols: str = Field(...)
    sort: Literal['ASC', 'DESC'] = Field(default='ASC')
    limit: int = Field(..., gt=0, le=1000)
    offset: int = Field(..., ge=0)
    date_from_inclusive: date = Field(..., alias='date_from')
    date_to_inclusive: date = Field(..., alias='date_to')