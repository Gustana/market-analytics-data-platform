from datetime import date

from pydantic import BaseModel, ConfigDict, Field


class TimeFrameRateParam(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    start_date_inclusive: date = Field(..., alias='start_date')
    end_date_inclusive: date = Field(..., alias='end_date')
    source: str = Field(default='USD')
    currencies: str = Field(...)