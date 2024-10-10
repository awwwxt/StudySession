from core.errors import BadParams
from config import TIMES
from core.tools import check_group, check_lesson, check_link

from pydantic import BaseModel, validator
from typing import Optional

class GetChat(BaseModel):
    group: Optional[str] = None
    chat_id: Optional[int] = None

    @validator("group")
    def checkgroup(cls, value):
        if check_group(value):
            return value
        raise BadParams("validation missed group parameter")

class SetMailingChat(BaseModel):
    chat_id: int
    mailing: Optional[str] = None

    @validator('mailing')
    def check_time(cls, value):
        if value in TIMES:
            return value
        raise BadParams("validation missed mailing parameter")

class SetStatusChat(BaseModel):
    chat_id: int
    opened: bool

class SetLinkChat(BaseModel):
    chat_id: int
    link: Optional[str] = None

    @validator("link")
    def checklink(cls, value):
        if value is None or check_link(value):
            return value
        raise BadParams("validation missed link parameter")

class SetGroupChat(BaseModel):
    chat_id: int
    group: str

    @validator("group")
    def checkgroup(cls, value):
        if check_group(value):
            return value
        raise BadParams("validation missed group parameter")


class CreateChat(BaseModel):
    chat_id: int
    creator_id: int
    group: str

    @validator("group")
    def checkgroup(cls, value):
        if check_group(value):
            return value
        raise BadParams("validation missed group parameter")

class DeleteChat(BaseModel):
    chat_id: int

class GetMailingChat(BaseModel):
    time: str

    @validator('time')
    def check_time(cls, value):
        if value in TIMES:
            return value
        raise BadParams("validation missed time parameter")
