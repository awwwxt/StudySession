from web.web import SocketRoute, dispatcher
from core.models import GetUser, GetClassmates, GetHelpers, \
                 GetMailingTime, GetAllUser, GetKeysByID, GetKeys, \
                        GetChat, GetColors, GetFonts, GetMailingChat
from core.database import Router
from core.akvt.update import reupdate

from typing import Dict
from os import execv
from sys import argv, executable
from datetime import datetime

@SocketRoute.on_message(target="GetUser", private = True)
async def getuser(token: str, params: GetUser) -> str:
    user = await Router.getUser(params.user_id)
    result = {}
    if user:
        for key, value in user.__dict__.items():
            if not key.startswith("_"):
                result[key] = value
        result.update(RegistrationDate = result['RegistrationDate'].timestamp())
    else:
        result.update(reason = "no user")
    return dispatcher.generate_answer(False if "reason" in result else True, result = result)

@SocketRoute.on_message(target="GetClassmates", private = True)
async def getclassmates(token: str, params: GetClassmates) -> str:
    return dispatcher.generate_answer(result = await Router.getClassmates(params.user_id))

@SocketRoute.on_message(target="GetHelpers", private = True)
async def gethelpers(token: str, params: GetHelpers) -> str:
    return dispatcher.generate_answer(result = await Router.getHelpers(params.user_id))


@SocketRoute.on_message(target="GetMailingTime", private = True)
async def getmailingtime(token: str, params: GetMailingTime) -> str:
    return dispatcher.generate_answer(result = await Router.getMailingUsers(params.time))

@SocketRoute.on_message(target="GetAllUser", private = True)
async def getall(token: str, params: GetAllUser) -> str:
    return dispatcher.generate_answer(result = await Router.getAllUsers())

@SocketRoute.on_message(target="GetKeysByID", private = True)
async def getkeysbyid(token: str, params: GetKeysByID) -> str:
    keys =  await Router.getKeysByUID(params.user_id)
    if keys:
        return dispatcher.generate_answer(key = keys.Key, date = datetime.timestamp(keys.DateOfCreation), 
                        role = keys.Role, creator = keys.CreatorID, result = True)
    else:
        return dispatcher.generate_answer(result = None)
    
@SocketRoute.on_message(target="GetKeys", private = True)
async def getkeysbyid(token: str, params: GetKeys) -> str:
    keys = await Router.getKeysByUID(params.user_id)
    if keys:
        result = {}
        for key in keys: 
            result[key.Key] = {"date": datetime.timestamp(key.DateOfCreation), "role": key.Role, "creator": key.CreatorID}
        return dispatcher.generate_answer(result = result)
    else:
        return dispatcher.generate_answer(result = None)

@SocketRoute.on_message(target="GetChat", private = True)
async def getchat(token: str, params: GetChat) -> str:
    if not params.chat_id and not params.group: 
        return dispatcher.generate_answer(result = "Missed chat or group")
    chat = await Router.getChatByID(params.chat_id) if params.group is None \
                                     else await Router.getChatByGroup(params.group) 
    if chat:
        return dispatcher.generate_answer(
            result = True, creator_id = chat.creator_id,
            chat_id = chat.chat_id, link = chat.link,
            group = chat.group, opened = chat.opened,
            mailing = chat.mailing
        )
    else:
        return dispatcher.generate_answer(result = None)

@SocketRoute.on_message(target="GetColors", private = True)
async def getfontcolors(token: str, params: GetColors) -> str:
    return dispatcher.generate_answer(result = colors)

@SocketRoute.on_message(target="GetFonts", private = True)
async def getfonts(token: str, params: GetFonts) -> str:
    return dispatcher.generate_answer(result = GetFonts())

@SocketRoute.on_message(target="GetMailingChat", private = True)
async def getfonts(token: str, params: GetMailingChat) -> str:
    result = []
    for chat in await Router.getChatsMailing(params.time):
        result.append((chat.creator_id, chat.chat_id, chat.group))
    return dispatcher.generate_answer(result = result)