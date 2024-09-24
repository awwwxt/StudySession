from config import StartDate, Days

from datetime import datetime, timedelta
from typing import Union, Optional, Tuple, List

def GetWeek(**kwargs: int) -> int:
    date = GetFullDate(**kwargs)
    difference = date - StartDate  
    return (difference.days // 7) % 2 + 1  

def GetFullDate(
        year: Optional[int] = None, 
        month: Optional[int] = None, 
        day: Optional[int] = None, 
        add_days: int = 0
        ) -> datetime:
    now =  datetime.now()
    return datetime(
        now.year if year is None else year, 
        now.month if month is None else month, 
        now.day if day is None else day
    ) + timedelta(days = add_days)

def GetCurrentMonth(**kwargs: int) -> int:
    return GetFullDate(**kwargs).month

def GetDatesOfWeek(add_days: int = 0) -> List[datetime]:
    today = datetime.today()
    return [
        GetFullDate(date.year, date.month, date.day, add_days) for date in [
            (today + timedelta(days = 1) if today.weekday() == 6 else today - timedelta(days = today.weekday()))
             + timedelta(days = i) for i in range(6)
        ]
    ]

def GetDay(**kwargs: int) -> int:
    return GetFullDate(**kwargs).weekday() 

def GetDayOfWeek(**kwargs: int) -> Tuple[int, Union[str, None]]:
    day = GetFullDate(**kwargs).weekday()
    return day, Days.get(day)

def datesConstructor(**kwargs: int) -> str:
    date = GetFullDate(**kwargs)
    return f"{date.day}-{date.month}-{date.year}"