from datetime import date

from src.extract.clients.base_client import BaseClient
from src.extract.schemas.responses.fixer.historical_rates_response import HistoricalRatesResponse
from src.extract.schemas.responses.fixer.latest_rates_response import LatestRatesResponse
from src.extract.schemas.responses.fixer.supported_currency_codes_response import SupportedCurrencyCodesResponse
from src.extract.schemas.params.fixer.historical_rates import HistoricalRatesParam
from src.extract.schemas.params.fixer.latest_rates import LatestRatesParam
from src.extract.schemas.params.fixer.supported_currency_codes import SupportedCurrencyCodesParam
from src.extract.utils.constants import Constants


class FixerClient(BaseClient):
    def __init__(self, api_key:str):
        super().__init__(base_url=Constants.FIXER_BASE_URL)
        self._api_key = api_key

    def get_latest_rates(self, request_param: LatestRatesParam) -> LatestRatesResponse:
        if type(request_param) != LatestRatesParam:
            raise TypeError(f'params must be type of {LatestRatesParam.__name__}')
        
        _params = request_param.model_dump(by_alias=True, exclude_none=True)
        
        _params[Constants.FIXER_API_KEY_PARAM_NAME] = self._api_key

        return self.get('/latest', _params)

    def get_historical_rates(self, dateValue: date, request_params: HistoricalRatesParam) -> HistoricalRatesResponse:
        if type(request_params) != HistoricalRatesParam:
            raise TypeError(f'params must be type of {HistoricalRatesParam.__name__}')
        
        _params = request_params.model_dump(by_alias=True, exclude_none=True)
        
        _params[Constants.FIXER_API_KEY_PARAM_NAME] = self._api_key

        if type(dateValue) != date:
            raise TypeError(f'invalid date: {dateValue}')
        
        formatted_date_str = dateValue.strftime("%Y-%m-%d")

        return self.get(f'/{formatted_date_str}', _params, HistoricalRatesResponse)

    def get_supported_currency_codes(self, request_params: SupportedCurrencyCodesParam) -> SupportedCurrencyCodesResponse:
        if type(request_params) != SupportedCurrencyCodesParam:
            raise TypeError(f'params must be type of {SupportedCurrencyCodesParam.__name__}')
        
        _params = request_params.model_dump(by_alias=True, exclude_none=True)

        _params[Constants.FIXER_API_KEY_PARAM_NAME] = self._api_key
        
        return self.get('/symbols', _params, SupportedCurrencyCodesResponse)