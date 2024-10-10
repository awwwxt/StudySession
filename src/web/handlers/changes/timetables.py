from web.web import SocketRoute, dispatcher
from core.models import DeleteLesson, DeleteShortDay, GetLessons, CreateShortDay, \
                         CreateHomework, DeleteHomework, GetHomeworks, CreateLesson
from core.database import Router
from config import logger

@SocketRoute.on_message(target="DeleteShortDay", private = True)
async def deleteshortday(token: str, params: DeleteShortDay) -> str:
    return dispatcher.generate_answer(result = await Router.deleteShortDay(
        params.user_id, params.group, day = params.day, month = params.month, year = params.year
    ))

@SocketRoute.on_message(target="DeleteLesson", private = True)
async def deletelesson(token: str, params: DeleteLesson) -> str:
    return dispatcher.generate_answer(result = await Router.deleteLesson(
        params.user_id, params.group, params.num, day = params.day, month = params.month, year = params.year
    ))

@SocketRoute.on_message(target="GetLessons", private = True)
async def getlessons(token: str, params: GetLessons) -> str:
    return dispatcher.generate_answer(result = await Router.getLessons(
        params.group, month = params.month, year = params.year, day = params.day
    ))

@SocketRoute.on_message(target="CreateShortDay", private = True)
async def createshortday(token: str, params: CreateShortDay) -> str:
    return dispatcher.generate_answer(result = await Router.createShortDay(
        params.user_id, params.group, month = params.month, year = params.year, day = params.day
    ))

@SocketRoute.on_message(target="CreateHomework", private = True)
async def createhomework(token: str, params: CreateHomework) -> str:
    logger.info(f"created homework, {params.name_lesson}, by {params.user_id} for {params.group}")
    return dispatcher.generate_answer(result = await Router.createHomework(
        params.user_id, params.num, params.name_lesson, params.group,
                month = params.month, year = params.year, day = params.day,
                teacher = params.teaher_name
    ))

@SocketRoute.on_message(target="DeleteHomework", private = True)
async def deletehomework(token: str, params: DeleteHomework) -> str:
    return dispatcher.generate_answer(result = await Router.deleteHomework(
        params.user_id, params.group, params.num,
                month = params.month, year = params.year, day = params.day
    ))

@SocketRoute.on_message(target="GetHomeworks", private = True)
async def gethomeworks(token: str, params: GetHomeworks) -> str:
    return dispatcher.generate_answer(result = await Router.getHomeworks(
        params.group, month = params.month, year = params.year, day = params.day
    ))

@SocketRoute.on_message(target="CreateLesson", private = True)
async def createlesson(token: str, params: CreateLesson) -> str:
    logger.info(f"created lesson, {params.name_lesson}, by {params.user_id} for {params.group}")
    return dispatcher.generate_answer(result = await Router.createLessons(
        params.user_id, params.num, params.name_lesson, params.group,
                month = params.month, year = params.year, day = params.day,
                teacher = params.teaher_name
    ))
