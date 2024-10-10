from core.http import Client
from core.tools.dates import GetCurrentMonth
from core.errors import ClientError
from config import (
    TEMP, 
    logger,
    NAMES_TIMETABLE_SOURCE, 
    MAX_DOWNLOAD_ATTEMPS
)

from fake_useragent import UserAgent; useragent = UserAgent()

from typing import Any, Tuple, List, Dict, Union
from aiohttp import ClientSession, ClientResponse

from bs4 import BeautifulSoup
from asyncio import gather
import aiofiles

class Parser(Client):
    def __init__(self, **kwargs: Any):
        super().__init__(**kwargs)
        self.url = "https://www.akvt.ru/students/raspisanie-zanyatij/"
        self.headers = {
            "Connection": "keep-alive",
            "User-Agent": useragent.random
        }

    async def create_request(self, **kwargs) -> Union[bytes, None]:
        for _ in range(MAX_DOWNLOAD_ATTEMPS):
            async with ClientSession() as session:
                try:
                    async with session as response:
                        response = await session.get(**kwargs) 
                        if response.status == 200:
                            return await response.read()
                        else:
                            raise ClientError(status = response.status, url = kwargs.get("url"))
                except Exception as error:
                    raise ClientError(url = kwargs.get("url"), error = error)
        return None

    def ParseLinks(self, page: str) -> Dict[str, str]:
        soup = BeautifulSoup(page, 'lxml')
        result = {}
        for link in soup.find_all("a", href = True):
            link = link.get("href")
            if link.endswith(".xls"):
                for key, value in NAMES_TIMETABLE_SOURCE.items():
                    if any(val in link for val in value):
                        result[key] = link
        return result     

    async def download(self, url: str, save_as: str) -> bool: 
        request = await self.create_request(url = url)
        if request:
            async with aiofiles.open(save_as, "wb") as file:
                await file.write(request)
            logger.success(f"{self.__class__.__name__} -> saved {url} at {save_as}")
            return True
        return False

    async def get(self) -> Tuple[List[str], List[str], List[str]]:
        for _ in range(MAX_DOWNLOAD_ATTEMPS):
            response = await self.create_request(url = self.url)  

            if response:
                links = self.ParseLinks(response.decode())

                files = list(map(lambda targ: f"{TEMP}{targ}.xls", links.keys()))
                result = await gather(*[self.download(url, files[index]) for index, url in enumerate(links.values())])
                if not None in result and len(result) == len(NAMES_TIMETABLE_SOURCE.keys()):
                    return files
        raise ClientError(error = "Cannot download all documents, unknown error")