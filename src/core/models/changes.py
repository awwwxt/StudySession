from core.errors import BadParams
from core.tools import check_group, check_lesson
from core.tools import colors, GetFonts
from config import TIMES, ALLOWED_ALIGNS

from pydantic import BaseModel, validator
from typing import Optional

class SetGroup(BaseModel):
    user_id: int
    group: str

    @validator("group")
    def checkgroup(cls, value):
        if check_group(value):
            return value
        raise BadParams("validation missed group parameter")

class SetExt(BaseModel):
    user_id: int
    enable: bool

class SetImage(BaseModel):
    user_id: int
    enable: bool

class SetMail(BaseModel):
    user_id: int
    time: Optional[str] = None

    @validator("time")
    def check_time(cls, value):
        if value in TIMES:
            return value
        raise BadParams("validation missed time parameter")

class SetPrivacy(BaseModel):
    user_id: int
    enable: bool

class SetFontColor(BaseModel):
    user_id: int
    color: str

    @validator("color")
    def check_color(cls, value: str):
        if value in colors.keys():
            return value
        raise BadParams("validation missed color parameter")

class SetBackColor(BaseModel):
    user_id: int
    color: str

    @validator("color")
    def check_color(cls, value: str):
        if value in colors.keys():
            return value
        raise BadParams("validation missed color parameter")

class SetName(BaseModel):
    user_id: int
    name: Optional[str] = None

    @validator("name")
    def checkname(cls, value):
        if value is None or check_lesson(value):
            return value
        raise BadParams("validation missed name parameter")


class SetAlign(BaseModel):
    user_id: int
    align: str

    @validator("align")
    def check_align(cls, value):
        if value in ALLOWED_ALIGNS:
            return value
        raise BadParams("validation missed align parameter")

class SetFont(BaseModel):
    user_id: int
    font: str

    @validator("font")
    def check_font(cls, value):
        if value in GetFonts():
            return value
        raise BadParams("validation missed font parameter")

class SetTimeTimetable(BaseModel):
    user_id: int
    enable: bool