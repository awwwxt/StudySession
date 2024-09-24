from core.database.scheme import ShortDays, User
from core.tools import datesConstructor
from config import AccessLevels

from datetime import datetime
from sqlalchemy import select, delete, update
from typing import Union
from abc import ABC, abstractmethod

class Shortdays:
    @abstractmethod
    async def getUser(user_id: int) -> Union[bool, User]:
        ...

    async def createShortDay(
            self, 
            user_id: int,
            group: str,
            **kwargs: int
    ) -> bool:
        user = await self.getUser(user_id)
        if user is None or user.AccessLevel < AccessLevels[2]:
            return False
        if not await self._checkShortDay(group = group, **kwargs):
            async with self.__session__() as session:
                session.add(ShortDays(
                    CreatorID = user_id,
                    Date = datesConstructor(**kwargs),
                    Group = group,
                    DateOfCreation = datetime.now()
                ))
                await session.commit()
            return True
        return False

    async def deleteShortDay(
              self, 
              user_id: int, 
              group: str, 
              **kwargs: int, 
              ) -> bool:
        user = await self.getUser(user_id)
        if user is None or user.AccessLevel < AccessLevels[2]:
            return False
        async with self.__session__() as session:
            if await self._checkShortDay(group = group, **kwargs):
                await session.execute(delete(ShortDays.__table__).where(
                    (ShortDays.Date == datesConstructor(**kwargs)) 
                    & (ShortDays.Group == group) 
                ))
                await session.commit()
                return True
            return False

    async def _checkShortDay(
            self, 
            group: str,
            **kwargs
    ) -> bool:
        async with self.__session__() as session:
            data = await session.execute(
                select(ShortDays).where(
                    (ShortDays.Date == datesConstructor(**kwargs)) 
                    & (ShortDays.Group == group)))
        return True if data.scalar() else False