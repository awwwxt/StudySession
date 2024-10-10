from core.tools import GenCellName, sync_to_async, check_lesson
from config import (
    TeacherCache, 
    DDoSCache, 
    Cache, 
    ROW1,
    ROW2,
    ROW4,
    ROW3,
    MAX_TEACHER_NAME_LEN,
    MIN_TEACHER_NAME_LEN 
)

from typing import Dict, Union, Optional, List
from typing import Tuple
from functools import lru_cache

from abc import ABC, abstractmethod

class TeachersParser(ABC):

    @sync_to_async
    @lru_cache(maxsize = TeacherCache)
    def _SearchTeachers(
        self,
        name: str,
        week: int, 
        lessons: List[int],
    ) -> Dict[str, Dict[int, str]]:
        result = {i: {"Group": None, "Teacher": None, "Cabinet": None, "LessonName": None} for i in range(6)}
        for row in self.__sheet__.iter_rows(min_row = lessons[0], max_row = lessons[5]):
            for cell in row:
                if not cell.value is None and name in cell.value:
                    temp2_row, temp_row = self._downRowTeachers(cell.row)
                    index = self._getIndexTeachers(temp2_row, lessons[0])
                    if temp_row > 14:
                        temp_row = temp_row - (4 * ((temp_row - 14) // 4 + 1))
                    if (week == 1 and not self._DetectBorder(cell.column - 1, cell.row - 1)) or (week == 2 and temp_row in (ROW2, ROW3) and not self._DetectBorder(cell.column - 1, cell.row)): 
                        if temp_row == ROW2:
                            lesson = self._GetRow(cell.column - 1, cell.row - 1).value
                            if self._IsLesson(lesson):
                                result[index]["LessonName"] = lesson
                            elif "ауд." in lesson:
                                result[index]["LessonName"], result[index]["Cabinet"] = lesson.split("ауд.")
                            if "ауд." in cell.value:
                                result[index]["Teacher"], result[index]["Cabinet"] = cell.value.split("ауд.")
                            else:
                                result[index]["Teacher"] = cell.value
                            if result[index]["Cabinet"] is None:
                                cab = self._GetRow(cell.column - 1, cell.row + 1).value
                                result[index]["Cabinet"] = cab if self._IsCab(cab) else self._GetRow(cell.column - 1, cell.row + 2).value
                        elif temp_row == ROW3:
                            if not self._GetRow(cell.column - 1, cell.row - 1).value == cell.value:
                                if self._IsTeacher(cell.value):
                                    result[index]["Cabinet"], result[index]["Teacher"] = self._GetRow(cell.column - 1, cell.row + 1).value, cell.value
                                else:
                                    data = cell.value.split("ауд.")
                                    if len(data) == 2:
                                        result[index]["Teacher"], result[index]["Cabinet"] = data
                                if not self._IsCab(result[index]["Cabinet"]): self._GetRow(cell.column - 1, cell.row + 2).value
                                result[index]["LessonName"] = self._GetRow(cell.column - 1, cell.row - 2).value
                    elif week == 2 and self._DetectBorder(cell.column - 1, cell.row - 1):
                        if temp_row in (ROW3, ROW4):
                            lesson = self._GetRow(cell.column - 1, cell.row - 1).value
                            if self._IsTeacher(cell.value):
                                result[index]["Teacher"] = cell.value
                            elif "ауд." in cell.value:
                                result[index]["Teacher"], result[index]["Cabinet"] = cell.value.split("ауд.")
                            elif "ауд." in lesson:
                                result[index]["LessonName"], result[index]["Cabinet"] = lesson.split("ауд.")
                            if result[index]['LessonName'] is None:
                                result[index]["LessonName"] = lesson
                    if list(result[index].values()).count(None) <= 2:
                        result[index]['Group'], = [key for key, value in self.groups.items() \
                                                        if GenCellName(cell.column - 1) == value]
        return result

    @sync_to_async
    @lru_cache(maxsize = DDoSCache)
    def _checkTeacher(self, name: str) -> bool:
        if not name is None and check_lesson(name) and not name in self.groups \
                and not name in ("Часы", "Дни") \
                and (name.count(".") in (0, 1, 2) or name.count("-") == 1) and len(name) < MAX_TEACHER_NAME_LEN:
            for row in self.__sheet__.iter_rows():
                for cell in row:
                    if cell.value and name in cell.value and MIN_TEACHER_NAME_LEN <= len(cell.value) < MAX_TEACHER_NAME_LEN \
                                and (cell.value.count("-") == 1 or cell.value.count(".") in (1, 2)) and not "ауд." in cell.value:
                        return cell.value
        return False
    
    @staticmethod
    @lru_cache(maxsize = Cache)
    def _IsLesson(obj: str) -> bool:
        return not obj is None and not "ауд." in obj and not obj[-2] == "."
    
    @staticmethod
    @lru_cache(maxsize = Cache)
    def _downRowTeachers(row: int) -> Tuple[int, int]:
        if row > 35:
            row = row - (25 * ((row - 35) // 25 + 1))
        temp_row = row
        if temp_row > 14:
            temp_row = temp_row - (4 * ((temp_row - 14) // 4 + 1))
        return row, temp_row

    @lru_cache(maxsize = Cache)
    def _getIndexTeachers(self, row: int, lessons: int) -> int:
        if lessons > 14:
            lessons = self._downRowTeachers(lessons)
            if isinstance(lessons, tuple):
                lessons = lessons[1]
        return (abs(row - lessons)) // 4
    
    @staticmethod
    @abstractmethod
    def _IsTeacher(name: Union[str, None]) -> bool:
        ...

    @staticmethod
    @abstractmethod
    def _IsCab(obj: Optional[str]) -> bool:
        ...

    @property
    @abstractmethod
    def groups(self) -> Dict[str, str]:
        ...