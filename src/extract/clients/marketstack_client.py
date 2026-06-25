from src.extract.clients.base_client import BaseClient
from src.extract.schemas.responses.marketstack.eod_response import EodResponse
from src.extract.schemas.responses.marketstack.ticker_response import TickerResponse
from src.extract.schemas.params.marketstack.eod import EodParam
from src.extract.schemas.params.marketstack.ticker import TickerParam
from src.extract.utils.constants import Constants

class MarketStackClient(BaseClient):
    def __init__(self, api_key: str):
        super().__init__(base_url=Constants.MARKETSTACK_BASE_URL)

        if type(api_key) != str or api_key.strip() == '':
            raise ValueError(f'invalid api key: {api_key}')

        self._api_key = api_key

    def get_eod(self, request_params: EodParam) -> EodResponse:
        if type(request_params) != EodParam:
            raise TypeError(f'params must be type of {EodParam.__name__}')
        
        _params = request_params.model_dump(exclude_none=True, by_alias=True)
        
        _params[Constants.MARKETSTACK_API_KEY_PARAM_NAME] = self._api_key

        return self.get('/eod', _params, EodResponse)

    def get_tickers(self, stock_ticker: str, request_params: TickerParam) -> TickerResponse:
        if type(request_params) != TickerParam:
            raise TypeError(f'params must be type of {TickerParam.__name__}')
        
        if (type(stock_ticker) != str 
            or stock_ticker.strip() == '' 
            or not stock_ticker.isalpha()
        ):
            raise Exception(f'stock_ticker is invalid: {stock_ticker}')
        
        _params = request_params.model_dump(exclude_none=True, by_alias=True)
        
        _params[Constants.MARKETSTACK_API_KEY_PARAM_NAME] = self._api_key

        return self.get(f'/tickers/{stock_ticker}', _params, TickerResponse)