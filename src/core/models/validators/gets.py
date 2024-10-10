from pydantic import BaseModel

class GetFonts(BaseModel):
    ...

class GetColors(BaseModel):
    ...

class GetKeys(BaseModel):
    user_id: int