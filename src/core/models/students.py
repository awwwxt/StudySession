from core.tools import sync_to_async
from config import Cache, TimetablesCache

from typing import Dict, Union, List, Optional, Tuple
from abc import ABC, abstractmethod
from functools import lru_cache

class StudentsParser(ABC):

    @sync_to_async
    @lru_cache(maxsize = TimetablesCache)
    def _SearchStudents(self,
        cell: Union[str, int],
        week: int,
        lessons: List[int],
        ext: bool = False
    ) -> Dict[int, Dict[str, None]]:

        result = {i: {
            "LessonName": None,
            "Teacher": None,
            "Cabinet": None
        } for i in range(6)}

        lessons2week = [i + 2 for i in lessons]
        cabinets, teachers = self._GetRows(lessons, True), self._GetRows(items = lessons)
        cabinets2week, teachers2week = self._GetRows(lessons2week, True), self._GetRows(lessons2week)

        for i in range(6):
            lesson = self._GetRow(cell, lessons[i]).value, self._GetRow(cell, lessons2week[i]).value
            if not lesson == (None, None):
                if week == 1:
                    if not lesson[0] is None:
                        result[i]["LessonName"] = lesson[0].split("ауд.")[0]
                        if ext:
                            result[i]["Teacher"], result[i]["Cabinet"] = self._DistributionData(
                                self._GetRow(cell, teachers[i]).value,
                                self._GetRow(cell, cabinets[i]).value,
                                lesson[0]
                        )
                else:
                    if lesson[1] is None:
                        if not self._DetectBorder(cell, lessons2week[i]):
                            result[i]["LessonName"] = lesson[0].split("ауд.")[0]
                            if ext:
                                result[i]["Teacher"], result[i]["Cabinet"] = self._DistributionData(
                                    self._GetRow(cell, teachers[i]).value,
                                    self._GetRow(cell, cabinets[i]).value,
                                    lesson[0]
                            )
                    else:
                        if self._IsTeacher(self._GetRow(cell, lessons2week[i]).value):
                            result[i]["LessonName"] = lesson[1].split("ауд.")[0]
                            if ext:
                                result[i]["Teacher"], result[i]["Cabinet"] = self._DistributionData(
                                    self._GetRow(cell, teachers2week[i]).value,
                                    self._GetRow(cell, cabinets2week[i]).value,
                                    lesson[1]
                            )

                        else:
                            result[i]["LessonName"] = lesson[0].split("ауд.")[0]
                            if ext:
                                result[i]["Teacher"], result[i]["Cabinet"] = self._DistributionData(
                                    self._GetRow(cell, teachers[i]).value,
                                    self._GetRow(cell, cabinets[i]).value,
                                    lesson[0]
                            )
        return result


    @staticmethod
    @abstractmethod
    def _GetRows(items: List[int], is_cab: Optional[bool] = False) -> List[int]:
        ...

    @lru_cache(maxsize = Cache)
    def _DistributionData(self, teacher: Union[str, None], cabinet: Union[str, None], lesson: Union[str, None]) -> Tuple[Union[str, None], Union[str, None]]:
        if not teacher is None:
            if self._IsTeacher(teacher):
                teacher = teacher
                if not self._IsCab(cabinet):
                    cabinet = "Не удалось найти"
            else:
                if "ауд." in teacher:
                    teacher, cabinet = teacher.split("ауд.")
        else:
            if not cabinet is None:
                if self._IsCab(cabinet):
                    teacher = "Не удалось найти"
                else:
                    teacher, cabinet = cabinet.split("ауд.")
            else:
                teacher, cabinet = ["Не удалось найти" for _ in range(2)]
        if not cabinet is None:
            if not cabinet == "Не удалось найти" and not "ауд." in cabinet:
                cabinet = f"ауд.{cabinet.strip()}"
            elif cabinet == "Не удалось найти" and not lesson is None and "ауд." in lesson:
                cabinet = f'ауд.{lesson.split("ауд.")[1]}'

        if teacher is None or teacher in ("Не удалось найти", None): teacher = None
        else: teacher = teacher.strip()

        if cabinet is None or cabinet in ("Не удалось найти", None): cabinet = None
        else: cabinet = cabinet.strip()

        return teacher, cabinet

    @abstractmethod
    def _DetectBorder(self, column: Union[str, int], row: int) -> bool:
        ...

    @staticmethod
    @abstractmethod
    def _IsCab(obj: Optional[str]) -> bool:
        ...

    @staticmethod
    @abstractmethod
    def _IsTeacher(name: Union[str, None]) -> bool:
        ...
