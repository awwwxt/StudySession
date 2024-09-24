from core.tools import (
    GetWeek,
    GetDayOfWeek,
    datesConstructor
)
from config import ShortTimeLessons, DefaultTimeLessons
from config import (
    TIMETABLES, 
    Cache, 
    LessonCells,
    BordersCache
)
from core.errors.exceptions import StudySessionError
from core.models import StudentsParser, TeachersParser
from core.models.reader import ExcelReader
from core.database import Router
from core.builders import BuildResultForStudents, BuildResultForTeachers

from concurrent.futures import ThreadPoolExecutor
from asyncio import gather, get_event_loop
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
                ):
        num_day, name_week = GetDayOfWeek(**kwargs)
        if num_day <= (len(LessonCells) - 1) and method in ("teachers", "students"):
            lessons = LessonCells[num_day]  
        else:
            raise StudySessionError()
        user = await Router.getUser(user_id)
        if method == "students":
            if group is None:
                group = user.Group
            group_in_excel = self.groups[group]
        week = GetWeek(**kwargs)
    
        tasks = [
            Router.getHomeworks(group, **kwargs), 
            Router.getLessons(group, **kwargs),
            Router._checkShortDay(group, **kwargs)
            ]
        if method == "students":
            user = await Router.getUser(user_id)
            tasks.append(self._SearchStudents(group_in_excel, week, lessons, user.EnableExtentedFormatInTimetable))
            homeworks, _lessons, short_day, result = await gather(*tasks)
            return BuildResultForStudents(data = {"day": name_week, "time": self._getTime(short_day, user.EnableTimeInTimetable, force_disable_time), "week": week, \
                            "lessons": result, "homeworks": homeworks, "edited_lesons": _lessons}, 
                                        user_id = user_id)
        elif method == "teachers":
            tasks.append(self._SearchTeachers(name, week, lessons))
            homeworks, _lessons, short_day, result = await gather(*tasks) 
            _meta = {i: {"Lesson": None, "Homework": None} for i in range(6)}
            for i in range(6):
                _meta[i]["Homework"], _meta[i]["Lesson"] = await gather(*[
                                        Router.getHomework(name, i , **kwargs),
                                        Router.getLesson(name, i, **kwargs)
                                    ])

            return BuildResultForTeachers(data = {"lessons": result, "day": name_week,\
                                "week": week, "time": self._getTime(short_day, user.EnableTimeInTimetable, force_disable_time), \
                                                    "meta": _meta, "date": datesConstructor(**kwargs)}, 
                                                    user_id = user_id)

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
        return len(name) in range(6, 10) and name.count(".") >= 1 and name[-2] == "." 

    @staticmethod
    @lru_cache(maxsize = Cache)
    def _IsCab(obj: Optional[str]) -> bool:
        if obj is None:
            return False
        return len(obj) in (7, 6, 8) and obj.count(".") in (0, 1) and "ауд" in obj

    @lru_cache(maxsize = BordersCache)
    def _DetectBorder(self, column: Union[str, int], row: int) -> bool:
        if (not self._GetRow(column, row).border.top.style is None or
            not self._GetRow(column, row).border.bottom.style is None or 
            not self._GetRow(column, row - 1).border.bottom.style is None):
            return True
        return False
    
    @staticmethod
    def _GetRows(items: List[int], is_cab: Optional[bool] = False) -> List[int]:
        return [item + (3 if is_cab else 1) for item in items]