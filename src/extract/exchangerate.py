from extract.clients.exchangerate import ExchangerateClient
from extract.schemas.params.exchangerate import TimeFrameRateParam
from extract.schemas.responses.exchangerate.time_frame_rate import TimeFrameRateResponse


def extract_time_frame_rates(client: ExchangerateClient, request_param: TimeFrameRateParam) -> TimeFrameRateResponse:
    return client.get_time_frame_rates(request_param)