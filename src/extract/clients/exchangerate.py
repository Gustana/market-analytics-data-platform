from src.extract.schemas.responses.exchangerate.time_frame_rate import TimeFrameRateResponse
from src.extract.clients.base_client import BaseClient
from src.extract.schemas.params.exchangerate import TimeFrameRateParam
from src.extract.utils.constants import Constants


class ExchangerateClient(BaseClient):
    def __init__(self, api_key:str):
        super().__init__(Constants.EXCHANGERATE_BASE_URL)

        if type(api_key) != str:
            raise TypeError(f'api_key type invalid: {type(api_key)}')
        
        if api_key.strip() == '':
            raise ValueError(f'api_key value invalid: {api_key}')
        
        self._api_key = api_key

    def get_time_frame_rates(self, request_param: TimeFrameRateParam) -> TimeFrameRateResponse:
        if type(request_param) != TimeFrameRateParam:
            raise TypeError(f'request_param must be type of {TimeFrameRateParam.__name__}')
        
        _request_param = request_param.model_dump(by_alias=True, exclude_none=True)
        _request_param[Constants.EXCHANGERATE_API_KEY_PARAM_NAME] = self._api_key

        return self.get('/timeframe', _request_param, TimeFrameRateResponse)