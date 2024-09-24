from core.builders.base import BaseBuilder

from typing import Union, Any, Dict

class BuildResultForStudents(BaseBuilder):
    def __init__(self, **data: Dict[Union[str, int], Any]):
        super().__init__(**data)

    def _toText(self, only_timetables: bool = False) -> str:
        result_lines = [f"{self.day} | {self.week}-ая неделя"]
        for i in range(6):
            Time = f"[{i + 1}, {self.time[i]}]" if self.time and not only_timetables else f"[{i + 1}]"
            string = f"\n{Time}"
            Lesson = self.lessons[i]["LessonName"]
            if i in self.edited_lesons:
                string += f"{self.edited_lesons[i][0]} edited by {self.edited_lesons[i][1]}"
            elif not Lesson is None:
                for index, obj in enumerate([
                    Lesson, 
                    self.lessons[i]["Teacher"], 
                    self.lessons[i]["Cabinet"]]):
                    if not obj is None:
                        if index == 0:
                            string += f" {obj}"
                        elif not only_timetables:
                            string += f" | {obj}"
            else:
                string += " Нет пары"
            if not only_timetables:
                if i in self.homeworks:
                    string += f"\n|-- {self.homeworks[i][0]} created by {self.homeworks[i][1]}"
            result_lines.append(string)
        return ''.join(result_lines).strip()