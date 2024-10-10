from core.tools import (
    GetWeek,
    GetDayOfWeek
)
from config import ShortTimeLessons, DefaultTimeLessons
from config import (
    TIMETABLES, 
    Cache, 
    LessonCells,
    BordersCache,
    MAX_TEACHER_NAME_LEN,
    MIN_TEACHER_NAME_LEN,
    MAX_LESSON_LEN,
    MAX_TEACHER_NAME_UNIQUE_LEN
)
from core.errors.exceptions import StudySessionError
from core.models import StudentsParser, TeachersParser
from core.models.reader import ExcelReader
from core.database import Router
from core.builders import BuilderTable

from asyncio import gather
from typing import Union, List, Optional
from functools import lru_cache

class Engine(ExcelReader, TeachersParser, StudentsParser):
    def __init__(self, lessons: str):
        super().__init__(f"{TIMETABLES}{lessons}")
    async def get(self,
                  method: str,
                  user_id: int,
                  group: Optional[str] = None,
                  name: Optional[str] = None,
                  force_disable_time: Optional[bool] = False,
                  **kwargs: int
                ) -> BuilderTable:
        num_day, name_week = GetDayOfWeek(**kwargs)
        if num_day <= (len(LessonCells) - 1) and method in ("teachers", "students"):
            lessons = LessonCells[num_day]  
        else:
            raise StudySessionError(message = "Нельзя получить расписание на воскресенье", is_warning = True)
        user = await Router.getUser(user_id)
        if method == "students":
            if group is None:
                group = user.Group
            group_in_excel = self.groups[group]
        week = GetWeek(**kwargs)
    
        tasks = [Router._checkShortDay(group, **kwargs)]

        if method == "students":
            tasks.append(Router.getHomeworks(group, **kwargs)), 
            tasks.append(Router.getLessons(group, **kwargs)),
            tasks.append(self._SearchStudents(group_in_excel, week, lessons, user.EnableExtentedFormatInTimetable))
            short_day, homeworks, edited_lessons, result = await gather(*tasks)

        elif method == "teachers":
            tasks.append(self._SearchTeachers(name, week, lessons))
            short_day, result = await gather(*tasks)

            homeworks, edited_lessons = {}, {}
            for i in range(6):
                homeworks[i], edited_lessons[i] = await gather(*[
                            Router.getHomework(name, i , **kwargs),
                            Router.getLesson(name, i, **kwargs)
                        ])

        return BuilderTable(
                    day = name_week,
                    time = self._getTime(short_day, user.EnableTimeInTimetable, force_disable_time),
                    week = week,
                    disable_time = force_disable_time,
                    lessons = result,
                    homeworks = homeworks,
                    edited_lessons = edited_lessons,
                    user_id = user.UserID
                )

    @staticmethod
    @lru_cache(maxsize = Cache)
    def _getTime(short: bool, enable: bool, force_disable: bool) -> Union[List[str], None]:
        if enable and not force_disable:
            return ShortTimeLessons if short else DefaultTimeLessons
        return None

    @staticmethod
    @lru_cache(maxsize = Cache)
    def _IsTeacher(name: Union[str, None]) -> bool:
        if name is None:
            return False
        if "ауд." in name:
            return False
        return (MIN_TEACHER_NAME_LEN <= len(name) <= MAX_TEACHER_NAME_LEN or len(set(name)) < MAX_TEACHER_NAME_UNIQUE_LEN) and \
                                             name.count(".") >= 1 

    @staticmethod
    @lru_cache(maxsize = Cache)
    def _IsCab(obj: Optional[str]) -> bool:
        if obj is None:
            return False
        return MIN_TEACHER_NAME_LEN <= len(obj) <= MAX_LESSON_LEN and obj.count(".") in (0, 1) and "ауд" in obj

    @lru_cache(maxsize = BordersCache)
    def _DetectBorder(self, column: Union[str, int], row: int) -> bool:
        if (not self._GetRow(column, row).border.top.style is None or
            not self._GetRow(column, row).border.bottom.style is None or 
            not self._GetRow(column, row - 1).border.bottom.style is None):
            return True
        return False
    
    @staticmethod
    def _GetRows(items: List[int], is_cab: Optional[bool] = False) -> List[int]:
        return [item + (2 if is_cab else 1) for item in items]