from pydantic import BaseModel, Field, ConfigDict

class TickerParam(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    mic_stock_exchange: str = Field(..., alias='exchange')
    limit: int = Field(..., gt=0, le=100)
    offset: int = Field(..., ge=0)