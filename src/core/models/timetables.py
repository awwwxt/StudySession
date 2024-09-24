from core.tools import check_group, check_lesson, check_name_lesson
from core.errors import BadParams

from pydantic import BaseModel, validator
from typing import Optional, Union

class Parser(BaseModel):
    method: str
    group: Optional[str] = None
    name: Optional[str] = None
    force_disable_time: Optional[bool] = None
    engine: str = 'release'
    in_format: str = "markdown"
    only_timetables: bool = False
    user_id: Optional[int] = None

    day: Optional[int] = None
    month: Optional[int] = None
    year: Optional[int] = None
    add_days: Optional[int] = 0

    @validator("engine")
    def checkengine(cls, value):
        if value in ("old", "release"):
            return value
        raise BadParams("validation missed engine parameter")

    @validator("in_format")
    def checkformat(cls, value):
        if value in ("text", "list", "markdown"):
            return value
        raise BadParams("validation missed format parameter")

    @validator("name")
    def checkteachername(cls, value):
        if value is None or check_lesson(value):
            return value
        raise BadParams("validation missed name parameter")

    @validator("method")
    def checkmethod(cls, value):
        if value in ("students", "teachers"):
            return value 
        raise BadParams("validation missed method parameter")

    @validator("group")
    def checkgroup(cls, value):
        if check_group(value):
            return value
        raise BadParams("validation missed group parameter")

class OnWeekParser(BaseModel):
    method: str
    group: Optional[str] = None
    name: Optional[str] = None
    engine: str = 'release'
    in_format: str = "markdown"
    only_timetables: bool = False
    user_id: Optional[int] = None

    day: Optional[int] = None
    month: Optional[int] = None
    year: Optional[int] = None

    @validator("engine")
    def checkengine(cls, value):
        if value in ("old", "release"):
            return value
        raise BadParams("validation missed engine parameter")

    @validator("in_format")
    def checkformat(cls, value):
        if value in ("text", "list", "markdown"):
            return value
        raise BadParams("validation missed format parameter")

    @validator("name")
    def checkteachername(cls, value):
        if value is None or check_lesson(value):
            return value
        raise BadParams("validation missed name parameter")

    @validator("method")
    def checkmethod(cls, value):
        if value in ("students", "teachers"):
            return value 
        raise BadParams("validation missed method parameter")

    @validator("group")
    def checkgroup(cls, value):
        if check_group(value):
            return value
        raise BadParams("validation missed group parameter")

class Changes(BaseModel):
    method: str
    name: Optional[str] = None
    user_id: Optional[int] = None

    @validator("name")
    def checkteachername(cls, value):
        if value is None or check_lesson(value):
            return value
        raise BadParams("validation missed name parameter")

    @validator("method")
    def checkmethod(cls, value):
        if value in ("students", "teachers"):
            return value 
        raise BadParams("validation missed method parameter")

class DeleteShortDay(BaseModel):
    user_id: int
    group: str

    day: Optional[int] = None
    month: Optional[int] = None
    year: Optional[int] = None

    @validator("group")
    def checkgroup(cls, value):
        if check_group(value):
            return value
        raise BadParams("validation missed group parameter")

class DeleteLesson(BaseModel):
    user_id: int
    group: str
    num: int

    day: Optional[int] = None
    month: Optional[int] = None
    year: Optional[int] = None

    @validator("group")
    def checkgroup(cls, value):
        if check_group(value):
            return value
        raise BadParams("validation missed group parameter")

class GetLessons(BaseModel):
    group: str

    day: Optional[int] = None
    month: Optional[int] = None
    year: Optional[int] = None

    @validator("group")
    def checkgroup(cls, value):
        if check_group(value):
            return value
        raise BadParams("validation missed group parameter")

class CreateShortDay(BaseModel):
    user_id: int
    group: str
    
    day: Optional[int] = None
    month: Optional[int] = None
    year: Optional[int] = None

    @validator("group")
    def checkgroup(cls, value):
        if check_group(value):
            return value
        raise BadParams("validation missed group parameter")

class CreateHomework(BaseModel):
    user_id: int
    num: int
    name_lesson: str
    group: str
    teaher_name: Optional[str] = None

    day: Optional[int] = None
    month: Optional[int] = None
    year: Optional[int] = None

    @validator("group")
    def checkgroup(cls, value):
        if check_group(value):
            return value
        raise BadParams("validation missed group parameter")
    
    @validator("teaher_name")
    def checkteachername(cls, value):
        if value is None or check_lesson(value):
            return value
        raise BadParams("validation missed teaher_name parameter")

    @validator("name_lesson")
    def checknamelesson(cls, value):
        if check_name_lesson(value):
            return value
        raise BadParams("validation missed name_lesson parameter")

class DeleteHomework(BaseModel):
    user_id: int
    group: str
    num: int
    
    day: Optional[int] = None
    month: Optional[int] = None
    year: Optional[int] = None

    @validator("group")
    def checkgroup(cls, value):
        if check_group(value):
            return value
        raise BadParams("validation missed group parameter")

class GetHomeworks(BaseModel):
    group: str

    day: Optional[int] = None
    month: Optional[int] = None
    year: Optional[int] = None

    @validator("group")
    def checkgroup(cls, value):
        if check_group(value):
            return value
        raise BadParams("validation missed group parameter")

class CreateLesson(BaseModel):
    user_id: int
    num: int
    name_lesson: str
    group: str
    teaher_name: Optional[str] = None

    day: Optional[int] = None
    month: Optional[int] = None
    year: Optional[int] = None

    @validator("group")
    def checkgroup(cls, value):
        if check_group(value):
            return value
        raise BadParams("validation missed group parameter")
    
    @validator("teaher_name")
    def checkteachername(cls, value):
        if value is None or check_lesson(value):
            return value
        raise BadParams("validation missed teaher_name parameter")

    @validator("name_lesson")
    def checknamelesson(cls, value):
        if check_name_lesson(value):
            return value
        raise BadParams("validation missed name_lesson parameter")

class SearchTeacherName(BaseModel):
    name: str

    @validator("name")
    def checkteachername(cls, value):
        if value is None or check_lesson(value):
            return value
        raise BadParams("validation missed name parameter")

class SearchGroup(BaseModel):
    group: str

    @validator("group")
    def checkgroup(cls, value):
        if check_group(value):
            return value
        raise BadParams("validation missed group parameter")