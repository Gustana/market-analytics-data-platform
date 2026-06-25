from pydantic import BaseModel, ConfigDict

class SupportedCurrencyCodesParam(BaseModel):
    # update this model if the api needs parameters

    model_config = ConfigDict(populate_by_name=True)