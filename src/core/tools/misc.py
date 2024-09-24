from config import MIN_GROUP_LEN, MAX_GROUP_LEN

from typing import Callable, Any
from asyncio import get_event_loop
from concurrent.futures import ThreadPoolExecutor
from typing import Dict, Union, Optional, Any
from re import match

def sync_to_async(func: Callable[[Any, Any], Any]):
    async def wrapper(*args, **kwargs):
        loop = get_event_loop()
        with ThreadPoolExecutor() as executor:
            return await loop.run_in_executor(executor, func, *args, **kwargs)
    return wrapper

def check_on_symbols(value: Any) -> bool:
    return value is None or (match(r'^[a-zA-Z0-9]*$', str(value)) is not None)

def check_words(value: Any) -> bool:
    return not value is None and str(value).isalpha() 

def check_numbers(value: Any) -> bool:
    if str(value).isdigit():
        return int(value)
    return False

def check_group(value: Any) -> bool:
    return value is None or (match(r'^[а-яА-Я0-9]{1,4}-?[а-яА-Я0-9]{1,4}$', str(value)) and 
                        len(value) in range(MIN_GROUP_LEN, MAX_GROUP_LEN))

def check_lesson(value: Any) -> bool:
    return True if match(r"^[А-Яа-яЁё\s.-]+$", str(value)) else False

def check_name_lesson(value: Any) -> bool:
    return True if match(r"^[А-Яа-я0-9.\-()\s]+$", str(value)) else False

def check_link(value: Any) -> bool:
    return True if match(r"https:\/\/t\.me\/(joinchat\/[a-zA-Z0-9_]+|[a-zA-Z0-9_]+|c\/[\+\w]+)", str(value)) else False