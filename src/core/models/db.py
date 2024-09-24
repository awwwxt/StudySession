from config import DATABASE

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker

from uvloop import run
from typing import Any

class Database:
    def __init__(self, tables: Any):
        self.tables = tables
        self.__engine__ = create_async_engine(
                f"sqlite+aiosqlite:///{DATABASE}", 
                connect_args={'check_same_thread': False}
            )
        __async_session__ = sessionmaker(self.__engine__, class_ = AsyncSession)
        self.__session__ = __async_session__
        run(self.__init_tables__())

    async def __init_tables__(self) -> None:
        async with self.__engine__.begin() as conn:
            await conn.run_sync(self.tables.metadata.create_all)