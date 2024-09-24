from core.database.scheme import Homework
from core.tools import datesConstructor
from config import AccessLevels

from datetime import datetime
from sqlalchemy import select, delete, update
from typing import Union, List, Dict

class Homeworks:
    async def _checkHomework(
            self,
            group: str, 
            num: int,
            **kwargs: int
            ) -> bool:
        async with self.__session__() as session:
            data = await session.execute(
                select(Homework.Group).where((Homework.LessonDate == datesConstructor(**kwargs)) & \
                           (Homework.LessonNumber == num - 1 ) & \
                                    (Homework.Group == group)))
        return True if data.scalar() else False

    async def createHomework(
              self,     
              user_id: int, 
              num_lesson: int, 
              name_lesson: str, 
              group: str,
              teacher: str,
              **kwargs: int) -> bool:
        user = await self.getUser(user_id)
        if user is None or user.AccessLevel < AccessLevels[2]:
            return False
        if await self._checkHomework(group, num_lesson, **kwargs):
            await self.deleteHomework(
                user_id = user_id, 
                group = group, 
                num = num_lesson, 
                **kwargs)
        async with self.__session__() as session:
            session.add(Homework(
                CreationDate = datetime.now(), LessonDate = datesConstructor(**kwargs),
                LessonNumber = num_lesson - 1, Homework = name_lesson,
                Group = group, CreatorID = user_id, Teacher = teacher))
                                         
            await session.commit()
        return True
        
    async def deleteHomework(
              self, 
              user_id: int, 
              group: str, 
              num: int, 
              **kwargs: int, 
              ) -> bool:
        user = await self.getUser(user_id)
        if user is None or user.AccessLevel < AccessLevels[2]:
            return False
        if await self._checkHomework(group, num, **kwargs):                
            async with self.__session__() as session:
                    await session.execute(delete(Homework.__table__).where(
                            (Homework.LessonDate == datesConstructor(**kwargs)) & 
                            (Homework.LessonNumber == num - 1) & 
                            (Homework.Group == group)))    
                    await session.commit()
                    return True
        return False

    async def getHomeworks(self, group: str, **kwargs: int) -> Dict[int, List[Union[int, str]]]:
        async with self.__session__() as session:
            data = await session.execute(
                select(Homework)
                .where((Homework.LessonDate == datesConstructor(**kwargs)) & (Homework.Group == group))
            )
        result = dict()
        for hw in data.scalars():
            result[hw.LessonNumber] = [hw.Homework, hw.CreatorID]
        return result
    
    async def getHomework(self,  teacher: str, num: int, **kwargs: int) -> Dict[int, List[Union[int, str]]]:
        async with self.__session__() as session:
            data = await session.execute(
                select(Homework)
                .where((Homework.LessonDate == datesConstructor(**kwargs)) & (Homework.Teacher == teacher)
                       & (Homework.LessonNumber == num))
            )
        data = data.scalar()
        if not data is None:
            return data.Homework, data.CreatorID, data.Group