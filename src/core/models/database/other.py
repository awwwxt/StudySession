from core.database.scheme import (
    User, 
    ChangedLesson,
    Chat,
    Homework,
    ShortDays
)
from config import AccessLevels
from core.tools import CreateCode

from sqlalchemy import select, delete, update
from typing import Union, List, Dict, Tuple
from datetime import datetime

class Other:
    async def getAllUsers(self) -> List[Tuple[int, int, str]]:
        async with self.__session__() as session:
            data = await session.execute(select(User))
            return [(user.UserID, user.Banned) for user in data.scalars()]
        

    async def _checkUID(self, user_id: int):
        async with self.__session__() as session:
            data = await session.execute(
                select(User).where(User.UserID == user_id))
        return True if data.scalar() else False

    async def NewUser(self, user_id: int, invited_by: Union[int, None] = None) -> bool:
        if not await self._checkUID(user_id):
            async with self.__session__() as session:
                session.add(User(
                    UserID = user_id,
                    AccessLevel = AccessLevels[0], 
                    RegistrationDate = datetime.now(),
                    InvitedBy = invited_by,
                    AuthToken = CreateCode()
                ))
                await session.commit()
                return True
        return False
    
    async def getUserByToken(self, token: str) -> Union[bool, User]:
        async with self.__session__() as session:
            data = await session.execute(select(User)
                        .where(User.AuthToken == token))
        data = data.scalar()
        return data if data else False

    async def deleteUser(self, user_id: int) -> None:
        async with self.__session__() as session:
            await session.execute(delete(User.__table__).where(User.UserID == user_id))
            await session.execute(delete(ChangedLesson.__table__).where(ChangedLesson.CreatorID == user_id))
            await session.execute(delete(Homework.__table__).where(Homework.CreatorID == user_id))
            await session.execute(delete(ShortDays.__table__).where(ShortDays.CreatorID == user_id))
            await session.execute(delete(Chat.__table__).where(Chat.creator_id == user_id))
            await session.commit()
        
    async def setGroup(self, user_id: int, group: str) -> bool:
        if not await self._checkUID(user_id):
                return False
        async with self.__session__() as session:
            await session.execute(update(User)
                    .where(User.UserID == user_id)
                    .values({User.Group: group}))
            await session.commit()
            return True
    
    async def setAccess(self, user_id: int, access: int) -> bool:
        if not await self._checkUID(user_id): return False
        async with self.__session__() as session:
            await session.execute(update(User)
                    .where(User.UserID == user_id)
                    .values({User.AccessLevel: access}))
            await session.commit()
        return True
    
    async def setExtentedForm(self, user_id: int, enable: bool = False) -> bool:
        if not await self._checkUID(user_id): return False
        async with self.__session__() as session:
            await session.execute(update(User)
                .where(User.UserID == user_id)
                .values({User.EnableExtentedFormatInTimetable: enable}))
            await session.commit()
            return True
    
    async def setImageForm(self, user_id: int, enable: bool) -> bool:
        if not await self._checkUID(user_id): return False
        async with self.__session__() as session:
            await session.execute(update(User)
                .where(User.UserID == user_id)
                .values({User.EnableImageFormatTimetable: enable}))
            await session.commit()
            return True
    
    async def setMailing(self, user_id: int, time: str) -> bool:
        if not await self._checkUID(user_id): return False
        async with self.__session__() as session:
            await session.execute(update(User)
                .where(User.UserID == user_id)
                .values({User.MailingTime: time}))
            await session.commit()
            return True
    
    async def setBan(self, user_id: int, ban: bool) -> bool:
        if not await self._checkUID(user_id): return False
        async with self.__session__() as session:
            await session.execute(
                update(User)
                    .where(User.UserID == user_id)
                    .values({User.Banned: ban}))
            await session.commit()
            return True

    async def getMailingUsers(self, time: str) -> List[tuple[int, str]]:
        async with self.__session__() as session:
            data = await session.execute(select(User)
                .where(User.MailingTime == time))
            return [(user.UserID, user.Group) for user in data.scalars()]

    async def setPrivacy(self, user_id: int, enable: bool) -> bool:
        if not await self._checkUID(user_id): return False
        async with self.__session__() as session:
            await session.execute(update(User)
                .where(User.UserID == user_id)
                .values({User.PrivateProfile: enable}))
            await session.commit()
            return True
    
    async def setFontColor(self, user_id: int, color: str) -> bool:
        if not await self._checkUID(user_id): return False
        async with self.__session__() as session:
            await session.execute(update(User)
                .where(User.UserID == user_id)
                .values({User.FontColorForImage: color}))
            await session.commit()
            return True
    
    async def setBackgroundColor(self, user_id: int, color: str) -> bool:
        if not await self._checkUID(user_id): return False
        async with self.__session__() as session:
            await session.execute(update(User)
                .where(User.UserID == user_id)
                .values({User.BackgroundColorForImage: color}))
            await session.commit()
            return True

    async def setName(self, user_id: int, name: str) -> bool:
        if not await self._checkUID(user_id): return False
        async with self.__session__() as session:
            await session.execute(update(User)
                .where(User.UserID == user_id)
                .values({User.Name: name}))
            await session.commit()
        return True
            
    async def removeRole(self, user_id: int) -> bool:
        if not await self._checkUID(user_id): return False
        async with self.__session__() as session:
            await session.execute(update(User)
                .where(User.UserID == user_id)
                .values({User.AccessLevel: AccessLevels[0]}))
            await session.commit()
        return True
    
    async def setAlign(self, user_id: int, align: str) -> bool:
        if not await self._checkUID(user_id): return False
        async with self.__session__() as session:
            await session.execute(update(User)
                .where(User.UserID == user_id)
                .values({User.AlignTextForImage: align}))
            await session.commit()
            return True

    async def setFont(self, user_id: int, font: str) -> bool:
        if not await self._checkUID(user_id): return False
        async with self.__session__() as session:
            await session.execute(
                update(User)
                .where(User.UserID == user_id)
                .values({User.FontNameForImage: font}))
            await session.commit()
            return True
            
    async def setTimeInTimetables(self, user_id: int, enable: bool) -> bool:
        if not await self._checkUID(user_id): return False
        async with self.__session__() as session:
            await session.execute(
                update(User)
                .where(User.UserID == user_id)
                .values({User.EnableTimeInTimetable: enable}))
            await session.commit()
            return True
        
    async def getHelpers(self, user_id: int) -> Union[bool, List[Tuple[str, int, bool]]]:
        if (await self.getUser(user_id)).AccessLevel < AccessLevels[2]:
            return False
        async with self.__session__() as session:
            data = await session.execute(select(User)
                  .where(User.PromotedBy == user_id))
        return [(row.Group, row.UserID, row.Banned)
                for row in data.scalars()]
    
    async def getClassmates(self, user_id: int) -> Union[bool, List[Tuple[int, bool, str, datetime, bool]]]:
        user = await self.getUser(user_id)
        if user.AccessLevel < AccessLevels[2]: 
            return False
        async with self.__session__() as session:
            data = await session.execute(select(User)
                  .where(User.Group == user.Group))
        return [(row.UserID, row.Banned, row.MailingTime, 
                 row.EnableExtentedFormatInTimetable) 
                   for row in data.scalars() if not row.PrivateProfile]