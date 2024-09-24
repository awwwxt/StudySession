from web.web import SocketRoute, dispatcher
from core.database import Router
from core.models import Parser, Changes, OnWeekParser, SearchTeacherName, SearchGroup
from core.akvt.engine import Engine
from core.tools import check_group, GetDatesOfWeek

from base64 import b64encode
from asyncio import gather
from config import APITOKEN
from asyncio import gather
from datetime import datetime
from typing import List, Any

release_engine = Engine("lessons.xlsx")
old_engine = Engine("lessons-old.xlsx")

@SocketRoute.on_message(target="Parser")
async def handletimetables(token: str, params: Parser) -> str:
    if token == APITOKEN:
        user_id = params.user_id
        user = await Router.getUser(user_id)
    else:
        user = await Router.getUserByToken(token)
        user_id = user.UserID
        if not check_group(params.group):
            return dispatcher.generate_answer(False, reason = "invalid group")
        
    if params.method in ("teachers", "students"):
        param = {"method": params.method, "user_id": user_id, "group": params.group, "name": params.name,
                                        "force_disable_time": params.force_disable_time, "day": params.day,
                                        "month": params.month, "year": params.year, "add_days": params.add_days}
        if params.engine == "release":
            result = await release_engine.get(**param)
        else:
            result = await old_engine.get(**param)
        if user.EnableImageFormatTimetable and not params.force_disable_time:
            return dispatcher.generate_answer(image = b64encode(await result.toBytes()).decode())
        else:
            if params.in_format == "markdown":
                result = result.toMarkDown()
            elif params.in_format == "list":
                result = result._toText(True).split("\n")
            else:
                result = result._toText(params.only_timetables)
        result = dispatcher.generate_answer(result = result)
    else:
        result = dispatcher.generate_answer(False, reason = "only teachers/students allowed")
    return result

@SocketRoute.on_message(target="Changes", private=True)
async def handlerchanges(token: str, params: Changes) -> str:
    dates1 = GetDatesOfWeek()
    dates2 = GetDatesOfWeek(7)
    param = {"method": params.method, "user_id": params.user_id, "name": params.name, "force_disable_time": True}
    
    def create_requests(dates: List[datetime]) -> List:
        requests = []
        for date in dates:
            requests.append((
                release_engine.get(**param, day=date.day, month=date.month, year=date.year),
                old_engine.get(**param, day=date.day, month=date.month, year=date.year)
            ))
        return requests

    async def fetch_data(requests: List[Any]) -> List:
        return await gather(*[gather(*req) for req in requests])

    async def process_dates(dates: List[datetime]) -> str:
        diffbuffer = []
        requests = create_requests(dates)
        results = await fetch_data(requests)
        
        for (new_response, old_response), date in zip(results, dates):
            new, old = new_response._toText(), old_response._toText()
            if new != old:
                diffbuffer.append(f"{date.day}-{date.month}-{date.year}\n\nБыло:\n{old}\n\nСтало:\n{new}\n\n")
        
        return ''.join(diffbuffer)

    if params.method in ("teachers", "students"):
        diffbuffer = await process_dates(dates1) + await process_dates(dates2)
        result = dispatcher.generate_answer(result = diffbuffer if len(diffbuffer) > 0 else "Изменения не обнаружены")
    else:
        result = dispatcher.generate_answer(False, reason = "only teachers/students allowed")

    return result

@SocketRoute.on_message(target="OnWeekParser", private = True)
async def handleronweek(token: str, params: OnWeekParser) -> str:     
    if params.method in ("teachers", "students"):
        buff = ""
        tasks = []
        for dt in GetDatesOfWeek():

            param = {"method": params.method, "user_id": params.user_id, "group": params.group, "name": params.name,
                                            "day": dt.day, "month": dt.month, "year": dt.year}
            if params.engine == "release":
                tasks.append(release_engine.get(**param))
            else:
                tasks.append(old_engine.get(**param))
           
        for result in await gather(*tasks):
            if params.in_format == "markdown":
                result = result.toMarkDown()
            else:
                result = result._toText(params.only_timetables)
            buff += f"{result}\n\n"
        result = dispatcher.generate_answer(result = buff)
    else:
        result = dispatcher.generate_answer(False, reason = "only teachers/students allowed")
    return result

@SocketRoute.on_message(target="SearchTeacherName", private = True)
async def handlerteachersname(token: str, params: SearchTeacherName) -> str:     
    return dispatcher.generate_answer(result = await release_engine._checkTeacher(params.name))

@SocketRoute.on_message(target="SearchGroup", private = True)
async def handlerstudentsgroup(token: str, params: SearchGroup) -> str:     
    return dispatcher.generate_answer(result = True if params.group in release_engine.groups.keys() else False)
