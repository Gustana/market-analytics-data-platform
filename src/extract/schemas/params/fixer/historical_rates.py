from pydantic import Field, BaseModel, ConfigDict

class HistoricalRatesParam(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    # comma-separated list of currency codes
    currency_codes: str = Field(..., alias='symbols')