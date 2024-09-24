from core.database.scheme import Chat

from typing import List
from sqlalchemy import select, delete, update

class Chats:
    async def getChatByGroup(self, group: str) -> Chat:
        async with self.__session__() as session:
            data = await session.execute(
                select(Chat)
                .where(Chat.group == group)
            )
        return data.scalar() if data else False

    async def getChatByID(self, chat_id: int) -> Chat:
        async with self.__session__() as session:
            data = await session.execute(
                select(Chat)
                .where(Chat.chat_id == chat_id)
            )
        return data.scalar() if data else False

    async def setGroupChat(self, chat_id: int, group: str) -> bool:
        if not await self._checkChatID(chat_id): return False
        async with self.__session__() as session:
            await session.execute(update(Chat)
                .where(Chat.chat_id == chat_id)
                .values({Chat.group: group}))
            await session.commit()
            return True

    async def _checkChatID(self, chat_id: int):
        async with self.__session__() as session:
            data = await session.execute(
                select(Chat).where(Chat.chat_id == chat_id))
        return True if data.scalar() else False

    async def setLinkChat(self, chat_id: int, link: str) -> bool:
        if not await self._checkChatID(chat_id): return False
        async with self.__session__() as session:
            await session.execute(update(Chat)
                .where(Chat.chat_id == chat_id)
                .values({Chat.link: link}))
            await session.commit()
            return True
    
    async def setStatusChat(self, chat_id: int, opened: bool) -> bool:
        if not await self._checkChatID(chat_id): return False
        async with self.__session__() as session:
            await session.execute(update(Chat)
                .where(Chat.chat_id == chat_id)
                .values({Chat.opened: opened}))
            await session.commit()
            return True

    async def setMailingChat(self, chat_id: int, mailing: str) -> bool:
        if not await self._checkChatID(chat_id): return False
        async with self.__session__() as session:
            await session.execute(update(Chat)
                .where(Chat.chat_id == chat_id)
                .values({Chat.mailing: mailing}))
            await session.commit()
            return True

    async def deleteChat(self, chat_id: int) -> bool:
        if not await self._checkChatID(chat_id): return False
        async with self.__session__() as session:
            await session.execute(delete(Chat.__table__).where(Chat.chat_id == chat_id))    
            await session.commit()
            return True

    async def NewChat(self, creator_id: int, chat_id: int, group: str) -> None:
        async with self.__session__() as session:
            if not await self._checkChatID(chat_id):
                session.add(Chat(
                    creator_id = creator_id,
                    chat_id = chat_id, 
                    group = group
                ))
            else:
                await session.execute(update(Chat)
                .where(Chat.creator_id == creator_id)
                .values({Chat.chat_id: chat_id, Chat.group: group}))
            await session.commit()

    async def getChatsMailing(self, time: str) -> List[Chat]:
        async with self.__session__() as session:
            data = await session.execute(
                select(Chat)
                .where(Chat.mailing == time)
            )
        return data.scalars() if data else False