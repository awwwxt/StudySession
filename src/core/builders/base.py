from core.tools import DrawPNG, GetMarkdown
from config import DEFAULT_BUFF_SIZE

from typing import Dict, Tuple, List
    
class BuilderTable:
    MARKDOWN_TEMPLATE = '`{}`'

    def __init__(
            self,
            day: str,
            time: Tuple[str, str, str, str, str, str],
            disable_time: bool,
            week: int,
            lessons: List[Dict[str, str]],
            homeworks: Dict[int, Tuple[str, int]],
            edited_lessons: Dict[int, Tuple[str, int]],
            user_id: int,
            buff_size: int = DEFAULT_BUFF_SIZE
    ):
        self.result = []
        self.day = day
        self.time = time
        self.week = week
        self.user_id = user_id
        for i in range(buff_size):
            string = time[i] if not disable_time and time else f"[{i + 1}]"
            if not i in edited_lessons or (edited_lessons and i in edited_lessons and edited_lessons[i] is None):
                if lessons[i]["LessonName"] or ("Cabinet" in lessons[i] and not lessons[i]["Cabinet"] is None):
                    if disable_time:
                        string += f" {lessons[i]['LessonName']}"
                    else:
                        for value in lessons[i].values():
                            if not value is None:
                                string += f" | {value.strip()}"
                        string = string.replace(" |", "", 1)
                else:
                    string += " Нет пары"
            elif i in edited_lessons and not edited_lessons[i] is None:
                string += f" {edited_lessons[i][0]} edited by {edited_lessons[i][1]}"
            else:
                string += " Нет пары"
            if not disable_time and homeworks and i in homeworks and not homeworks[i] is None:
                string += f"\n{homeworks[i][0]} edited by {homeworks[i][1]}"
            self.result.append(string)

    def toPlain(self) -> None:
        result = "\n".join(self.result)
        return f"{self.week}-ая неделя | {self.day}\n{result}"

    def toMarkDown(self) -> str:
        return self.MARKDOWN_TEMPLATE.format(GetMarkdown(self.toPlain()))

    async def toBytes(self) -> bytes:
        return await DrawPNG(self.toPlain(), self.user_id) 

    @property
    def toArray(self) -> List[str]:
        return self.result