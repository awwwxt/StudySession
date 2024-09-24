from core.database.scheme import DB, User
from core.models.db import Database
from core.models.database import (
    Chats, 
    Homeworks, 
    Lessons, 
    Other, 
    Shortdays,
    Keys
)

from sqlalchemy import select
from typing import Union

class DBRouter(
    Database, 
    Chats,
    Homeworks,
    Lessons,
    Other,
    Shortdays,
    Keys
):    
    def __init__(self):
        super().__init__(DB)

    async def getUser(self, user_id: int) -> Union[bool, User]:
        async with self.__session__() as session:
            data = await session.execute(select(User)
                        .where(User.UserID == user_id))
        data = data.scalar()
        return data if data else False