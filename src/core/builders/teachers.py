from core.builders.base import BaseBuilder

from typing import Any, Dict, Union, Any

class BuildResultForTeachers(BaseBuilder):
    def __init__(self, **data: Dict[Union[str, int], Any]):
        super().__init__(**data)

    def _toText(self, only_timetables: bool = False) -> str:
        result_lines = [f"{self.day} | {self.week}-ая неделя"]

        for i in range(6):
            group = self.lessons[i]["Group"]
            string = f"[{self.time[i]}, {i + 1}]" if self.time and not only_timetables else f"[{i + 1}]"
            if not group is None or not self.meta[i]["Lesson"] is None:
                if not self.meta[i]["Lesson"] is None:
                    string += f' {self.meta[i]["Lesson"][2]} | {self.meta[i]["Lesson"][0]} by {self.meta[i]["Lesson"][1]}'
                elif not self.lessons[i]["LessonName"] is None:
                    string += f' {self.lessons[i]["LessonName"]}'
                if self.meta[i]["Homework"] is None:
                    for obj in (
                        self.lessons[i]["Cabinet"], 
                        self.lessons[i]["Teacher"],
                        group):
                            if not obj is None:
                                string += f" | {obj.strip()}"
                if not only_timetables and not self.meta[i]["Homework"] is None:
                    string += f"\n|-- {self.meta[i]['Homework'][2]} | {self.meta[i]['Homework'][0]} by {self.meta[i]['Homework'][1]}"
                result_lines.append(f"\n{string}")
            else:
                result_lines.append(f"\n{string} Нет пары")
        return ''.join(result_lines).strip()