from core.http import Client
from core.tools.dates import GetCurrentMonth
from config import (
    TEMP, 
    logger,
    NAMES_TIMETABLE_SOURCE, 
    MAX_DOWNLOAD_ATTEMPS
)

from fake_useragent import UserAgent; useragent = UserAgent()

from typing import Any, Tuple, List, Dict
from aiohttp import ClientSession, ClientResponse
from bs4 import BeautifulSoup
from asyncio import gather

class Parser(Client):
    def __init__(self, **kwargs: Any):
        super().__init__(**kwargs)
        self.url = "https://www.akvt.ru/students/raspisanie-zanyatij/"
        self.headers = {
            "Connection": "keep-alive",
            "User-Agent": useragent.random
        }

    async def __create_response__(self, **kwargs) -> ClientResponse:
        try:
            async with ClientSession(timeout = self.timeout) as session:
                async with session.get(**kwargs) as response:
                    if response.status == 200:
                        return await response.content.read()
        except Exception as error:
           logger.error(f"{self.__class__.__name__}: {error}")

    def ParseLinks(self, page: str) -> Dict[str, str]:
        soup = BeautifulSoup(page.decode(), 'lxml')
        result = {}
        for link in soup.find_all("a", href = True):
            link: str = link.get("href")
            if link.endswith(".xls") and str(GetCurrentMonth()) in link:
                for key, value in NAMES_TIMETABLE_SOURCE.items():
                    if any(val in link for val in value):
                        result[key] = link
        return result     

    async def get(self) -> Any:
        return await self._start()

    async def download(self, url: str, save_as: str) -> bool: 
        try:
            request = await self.__create_response__(url = url)
            if request:
                with open(save_as, "wb") as file:
                    file.write(request)
                    logger.success(f"{self.__class__.__name__} -> saved at {url} {save_as}")
                    return True
            return False
        except Exception as error:
            logger.error(f"{self.__class__.__name__}: {error}")

    async def __download_demon(self, url: str, file: int) -> None:
        for _ in range(MAX_DOWNLOAD_ATTEMPS):
            if await self.download(url, file):
                return True
            
        logger.error(f"{self.__class__.__name__}: cannot fetch {file} from {url}")

    async def _start(self) -> Tuple[List[str], List[str]]:
        links = self.ParseLinks(await self.__create_response__(url = self.url))
        files = list(map(lambda targ: f"{TEMP}{targ}.xls", links.keys()))
        for result in await gather(*[self.__download_demon(url, files[index]) for index, url in enumerate(links.values())]):
            if not result:
                return
        return files
