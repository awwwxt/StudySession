from core.database.scheme import ChangedLesson, User
from core.tools import datesConstructor
from config import AccessLevels

from datetime import datetime
from typing import Dict, List, Union
from sqlalchemy import select, delete, update
from abc import ABC, abstractmethod

class Lessons(ABC):
    @abstractmethod
    async def getUser(user_id: int) -> Union[bool, User]:
        ...


    async def _checkLessons(self, num: int, group: str, **kwargs: int) -> bool:
        async with self.__session__() as session:
            data = await session.execute(
                select(ChangedLesson.Group)
                    .where((ChangedLesson.LessonDate == datesConstructor(**kwargs)) 
                    & (ChangedLesson.LessonNumber == num - 1) 
                    & (ChangedLesson.Group == group))
            )
        return True if data.scalar() else False

    async def createLessons(
              self, 
              user_id: int, 
              num_lesson: int, 
              name_lesson: str, 
              group: str,
              teacher: str,
            **kwargs: int
    ) -> bool:
        date = datesConstructor(**kwargs)
        user = await self.getUser(user_id)
        if user is None or user.AccessLevel < AccessLevels[2]:
            return False        
        result = await self._checkLessons(num_lesson, group, **kwargs)
        if result:
            await self.deleteLesson(
                user_id = user_id, 
                group = group, 
                num = num_lesson, 
                **kwargs)
            
        async with self.__session__() as session:
            session.add(ChangedLesson(
                CreationDate = datetime.now(), 
                LessonDate = date,
                LessonNumber = num_lesson - 1,
                NewLesson = name_lesson,
                Group = group,
                CreatorID = user_id,
                Teacher = teacher
                        )
                    )
            await session.commit()
            return True

    async def deleteLesson(
              self, 
              user_id: int, 
              group: str, 
              num: int, 
              **kwargs: int, 
              ) -> bool:
        async with self.__session__() as session:
            if await self._checkLessons(num, group, **kwargs):
                await session.execute(delete(ChangedLesson.__table__).where(
                     (ChangedLesson.LessonDate == datesConstructor(**kwargs)) 
                    & (ChangedLesson.LessonNumber == num - 1) 
                    & (ChangedLesson.Group == group))
                )    
                await session.commit()
            else:
                await self.createLessons(
                     user_id = user_id,  
                     num_lesson = num - 1, 
                     name_lesson = "Нет пары", 
                     group = group,
                     teacher = None
                     **kwargs)
            return True

    async def getLessons(self, group: str, **kwargs) -> Dict[int, List[Union[str, int]]]:
        async with self.__session__() as session:
            data = await session.execute(
                select(ChangedLesson)
                .where((ChangedLesson.LessonDate == datesConstructor(**kwargs)) & (ChangedLesson.Group == group)))
        data = data.scalars()
        if data is None: return False
        result = dict()
        for ls in data:
            result[ls.LessonNumber] = [ls.NewLesson, ls.CreatorID]
        return result
    
    async def getLesson(self, teacher: str, num: int, **kwargs) -> Dict[int, List[Union[str, int]]]:
        async with self.__session__() as session:
            data = await session.execute(
                select(ChangedLesson)
                .where((ChangedLesson.LessonDate == datesConstructor(**kwargs))
                        & (ChangedLesson.Teacher == teacher) 
                        & (ChangedLesson.LessonNumber == num)))
        data = data.scalar()
        if data is None: return None
        return data.NewLesson, data.CreatorID, data.Group