from config import TIMES
from core.tools import check_on_symbols
from core.errors import BadParams

from pydantic import BaseModel, validator
from typing import Optional

class NewUser(BaseModel):
    user_id: int
    invited_by: Optional[int] = None

class GetUser(BaseModel):
    user_id: int

class DeleteUser(BaseModel):
    user_id: int

class GetClassmates(BaseModel):
    user_id: int

class GetHelpers(BaseModel):
    user_id: int

class ActivateKey(BaseModel):
    user_id: int
    key: str

    @validator('key')
    def check_key(cls, value):
        if check_on_symbols(value):
            return value
        raise BadParams("validation missed key parameter")

class RemoveRole(BaseModel):
    user_id: int

class GetMailingTime(BaseModel):
    time: str

    @validator('time')
    def check_time(cls, value):
        if value in TIMES:
            return value
        raise BadParams("validation missed time parameter")


class SwitchBan(BaseModel):
    user_id: int
    ban: bool

class SwitchAccess(BaseModel):
    user_id: int
    access: int

class GetAllUser(BaseModel):
    ...

class CreateInviteKey(BaseModel):
    uid: int
    role: int

class DeleteKey(BaseModel):
    uid: int
    key: Optional[str] = None

    @validator('key')
    def check_key(cls, value):
        if check_on_symbols(value):
            return value
        raise BadParams("validation missed key parameter")

class GetKeysByID(BaseModel):
    user_id: int

class RemoveInvited(BaseModel):
    user_id: int
    role: int