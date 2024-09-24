from core.database.scheme import InviteKeys, User
from core.tools.generators import CreateCode

from sqlalchemy import select, delete, update
from typing import Union, List, Dict, Tuple
from datetime import datetime
from abc import ABC, abstractmethod

class Keys(ABC):
    @abstractmethod
    async def setAccess(user_id: int, role: int) -> bool:
        ...

    async def _getKeyData(self, key: str) -> Union[bool, Tuple[int, int]]:
        async with self.__session__() as session:
            data: InviteKeys = await session.execute(select(
                                            (InviteKeys))
                                            .where(InviteKeys.Key == key))
        data = data.scalar()
        return False if data is None else (data.CreatorID, data.Role)
    
    async def createInviteKey(self, uid: int, role: int) -> Union[bool, str]:
        async with self.__session__() as session:
            key = CreateCode()
            while await self._getKeyData(key):
                key = CreateCode()
            session.add(InviteKeys(
                DateOfCreation = datetime.now(), 
                CreatorID = uid,
                Key = key,
                Role = role))
            await session.commit()
            return key

    async def deleteKey(self, uid: int, key: str) -> None:
        async with self.__session__() as session:
            await session.execute(
                 delete(InviteKeys.__table__)
                 .where(((InviteKeys.CreatorID == uid) & 
                        (InviteKeys.Key == key) if key else (InviteKeys.CreatorID == uid))))               
            await session.commit()

    async def getKeysByUID(self, user_id: int) -> InviteKeys:
        user = await self.getUser(user_id)
        async with self.__session__() as session:
            data = await session.execute(
                select(InviteKeys)
                .where(InviteKeys.CreatorID == user_id)
            )
        return (data.scalars() if user.AccessLevel == 4 else data.scalar()) if data else False

    async def activateKey(self, user_id: int, key: str) -> bool:
        user = await self.getUser(user_id)
        result = await self._getKeyData(key)
        if result and user:
            await self.deleteKey(result[0], key)
            await self.setAccess(user_id, result[1])
            async with self.__session__() as session:
                await session.execute(update(User)
                    .where(User.UserID == user_id)
                    .values({User.PromotedBy: result[0]})
                )
                await session.commit()
            return True
        return False
    
    async def deleteInvited(self, user_id: int, role: int):
        async with self.__session__() as session:
            await session.execute(update(User)
            .where(User.UserID == user_id)
            .values({User.PromotedBy: None, User.AccessLevel: role})
            )
            await session.commit()