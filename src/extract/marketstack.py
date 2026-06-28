from extract.schemas.params.marketstack import EodParam, TickerParam
from extract.schemas.responses.marketstack.eod_response import EodResponse
from src.extract.clients.marketstack_client import MarketStackClient
from src.extract.schemas.responses.marketstack.ticker_response import TickerResponse


def extract_tickers(client: MarketStackClient, stock_ticker: str, request_param: TickerParam) -> TickerResponse:
    return client.get_tickers(stock_ticker, request_param)

def extract_eod(client: MarketStackClient, request_param: EodParam) -> EodResponse:
    return client.get_eod(request_param)