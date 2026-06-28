from src.extract.clients.base_client import BaseClient
from src.extract.schemas.responses.marketstack.eod_response import EodResponse
from src.extract.schemas.responses.marketstack.ticker_response import TickerResponse
from src.extract.schemas.params.marketstack import EodParam, TickerParam
from src.extract.utils.constants import Constants

class MarketStackClient(BaseClient):
    def __init__(self, api_key: str):
        super().__init__(base_url=Constants.MARKETSTACK_BASE_URL)

        if type(api_key) != str:
            raise TypeError(f'api_key type invalid: {type(api_key)}')
        
        if api_key.strip() == '':
            raise ValueError(f'api_key value invalid: {api_key}')
        
        self._api_key = api_key

    def get_eod(self, request_param: EodParam) -> EodResponse:
        if type(request_param) != EodParam:
            raise TypeError(f'request_param must be type of {EodParam.__name__}')
        
        _request_param = request_param.model_dump(exclude_none=True, by_alias=True)
        _request_param[Constants.MARKETSTACK_API_KEY_PARAM_NAME] = self._api_key

        return self.get('/eod', _request_param, EodResponse)

    def get_tickers(self, stock_ticker: str, request_param: TickerParam) -> TickerResponse:
        if type(request_param) != TickerParam:
            raise TypeError(f'request_param must be type of {TickerParam.__name__}')
        
        if (type(stock_ticker) != str 
            or stock_ticker.strip() == '' 
            or not stock_ticker.isalpha()
        ):
            raise ValueError(f'stock_ticker is invalid: {stock_ticker}')
        
        _request_param = request_param.model_dump(exclude_none=True, by_alias=True)
        _request_param[Constants.MARKETSTACK_API_KEY_PARAM_NAME] = self._api_key

        return self.get(f'/tickers/{stock_ticker}', _request_param, TickerResponse)