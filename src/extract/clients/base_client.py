from typing import TypeVar

import httpx
from pydantic import BaseModel

from src.extract.utils.constants import Constants
from src.extract.utils.logger import get_logger

ResponseTypeT = TypeVar('ResponseTypeT', bound=BaseModel)

class BaseClient:
    def __init__(self, base_url: str):
        _timeout_config = httpx.Timeout(
            connect=Constants.CONNECTION_TIMEOUT_IN_SECOND, 
            read=Constants.READ_TIMEOUT_IN_SECOND, 
            write = Constants.WRITE_TIMEOUT_IN_SECOND,
            pool=Constants.POOL_CONNECTION_TIMEOUT_IN_SECOND
        )

        self._client = httpx.Client(base_url=base_url, timeout=_timeout_config)
        self._logger = get_logger(default_context={"base_url": base_url})

    def get(self, endpoint: str, params: dict, response_model: type[ResponseTypeT]) -> ResponseTypeT:
        try:
            response = self._client.get(endpoint, params=params)
            response.raise_for_status()

            return response_model.model_validate(response.json())
        except Exception as e:
            self._logger.error(f'Error occurred when calling the api {e}')
    
    def close(self):
        self._client.close()