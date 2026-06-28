from typing import Any, TypeVar

import httpx
from pydantic import TypeAdapter

from src.extract.clients.utils import ClientUtils
from src.extract.utils.constants import Constants
from src.extract.utils.logger import get_logger

ResponseTypeT = TypeVar('ResponseTypeT')

class BaseClient:
    def __init__(self, base_url: str):
        _timeout_config = httpx.Timeout(
            connect=Constants.CONNECTION_TIMEOUT_IN_SECOND, 
            read=Constants.READ_TIMEOUT_IN_SECOND, 
            write = Constants.WRITE_TIMEOUT_IN_SECOND,
            pool=Constants.POOL_CONNECTION_TIMEOUT_IN_SECOND
        )

        if not ClientUtils.is_url_valid(base_url):
            raise ValueError(f'invalid base_url: {base_url}')

        self._client = httpx.Client(base_url=base_url, timeout=_timeout_config)
        self._logger = get_logger(default_context={"base_url": base_url})

    def get(self, endpoint: str, request_param: dict[str, Any], response_model: type[ResponseTypeT]) -> ResponseTypeT:
        if type(endpoint) != str:
            raise TypeError(f'endpoint type must be string, passed type: {type(endpoint)}')
        
        if endpoint.split() == '' or '/' not in endpoint:
            raise ValueError(f'endpoint value invalid: {endpoint}')
        
        if type(request_param) != dict:
            raise TypeError(f'request_param must be dict type, passed type: {type(endpoint)}')
        
        try:
            response = self._client.get(endpoint, params=request_param)
            response.raise_for_status()

            return TypeAdapter(response_model).validate_python(response.json())
        except httpx.HTTPError as e:
            self._logger.error(f'Error occurred when calling the api {e}')
            raise
    
    def close(self):
        self._client.close()