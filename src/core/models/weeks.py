from typing import Optional, Union
from pydantic import BaseModel

class WeekSearch(BaseModel):
    day: Optional[int] = None
    month: Optional[int] = None
    year: Optional[int] = None
    add_days: Optional[int] = 0