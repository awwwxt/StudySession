from aiohttp import ClientTimeout, ClientResponse
from abc import ABC, abstractmethod
from random import choice
from typing import Union, Any

class Client:
    def __init__(self, timeout: float):
        self.timeout = ClientTimeout(timeout)
        self._proxy = []
        self._cached_proxy: Union[str, None] = None

    @property
    def proxy(self, use_cache: bool = True) -> str:
        if not self._cached_proxy is None and use_cache:
            return self._cached_proxy
        return choice(self._proxy)

    @abstractmethod
    async def create_request(self, **kwargs) -> ClientResponse:
        ...

    @abstractmethod
    async def get(self, **kwargs) -> Any:
        ...