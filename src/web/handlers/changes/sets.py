from web.web import SocketRoute, dispatcher
from core.models import SetGroup, SetExt, SetImage, SetMail, SetName, SetBackColor, SetFontColor, SetPrivacy, \
                        SetAlign, SetFont, SetTimeTimetable, SetMailingChat, SetStatusChat, SetLinkChat, \
                            SetGroupChat, CreateChat, DeleteChat
from core.tools import get_fonts, colors, sync_to_async
from core.database import Router

from typing import Dict

@SocketRoute.on_message(target="SetGroup", private = True)
async def setgroup(token: str, params: SetGroup) -> str:
    return dispatcher.generate_answer(result = await Router.setGroup(params.user_id, params.group))

@SocketRoute.on_message(target="SetExt", private = True)
async def setext(token: str, params: SetExt) -> str:
    return dispatcher.generate_answer(result = await Router.setExtentedForm(params.user_id, params.enable))

@SocketRoute.on_message(target="SetImage", private = True)
async def setimage(token: str, params: SetImage) -> str:
    return dispatcher.generate_answer(result = await Router.setImageForm(params.user_id, params.enable))

@SocketRoute.on_message(target="SetMail", private = True)
async def setmail(token: str, params: SetMail) -> str:
    return dispatcher.generate_answer(result = await Router.setMailing(params.user_id, params.time))

@SocketRoute.on_message(target="SetPrivacy", private = True)
async def setprivacy(token: str, params: SetPrivacy) -> str:
    return dispatcher.generate_answer(result = await Router.setPrivacy(params.user_id, params.enable))

@SocketRoute.on_message(target="SetFontColor", private = True)
async def setfontcolor(token: str, params: SetFontColor) -> str:
    return dispatcher.generate_answer(result = await Router.setFontColor(params.user_id, params.color))

@SocketRoute.on_message(target="SetBackColor", private = True)
async def setbackcolor(token: str, params: SetBackColor) -> str:
    return dispatcher.generate_answer(result = await Router.setBackgroundColor(params.user_id, params.color))

@SocketRoute.on_message(target="SetName", private = True)
async def setname(token: str, params: SetName) -> str:
    return dispatcher.generate_answer(result = await Router.setName(params.user_id, params.name))

@SocketRoute.on_message(target="SetAlign", private = True)
async def setalign(token: str, params: SetAlign) -> str:
    return dispatcher.generate_answer(result = await Router.setAlign(params.user_id, params.align))

@SocketRoute.on_message(target="SetFont", private = True)
async def setalign(token: str, params: SetFont) -> str:
    return dispatcher.generate_answer(result = await Router.setFont(params.user_id, params.font))

@SocketRoute.on_message(target="SetTimeTimetable", private = True)
async def settimeintimetable(token: str, params: SetTimeTimetable) -> str:
    return dispatcher.generate_answer(result = await Router.setTimeInTimetables(params.user_id, params.enable))

@SocketRoute.on_message(target="SetMailingChat", private = True)
async def setmailingchat(token: str, params: SetMailingChat) -> str:
    return dispatcher.generate_answer(result = await Router.setMailingChat(params.chat_id, params.mailing))

@SocketRoute.on_message(target="SetStatusChat", private = True)
async def setstatyschat(token: str, params: SetStatusChat) -> str:
    return dispatcher.generate_answer(result = await Router.setStatusChat(params.chat_id, params.opened))

@SocketRoute.on_message(target="SetLinkChat", private = True)
async def setlinkchat(token: str, params: SetLinkChat) -> str:
    return dispatcher.generate_answer(result = await Router.setLinkChat(params.chat_id, params.link))

@SocketRoute.on_message(target="SetGroupChat", private = True)
async def setgroupchat(token: str, params: SetGroupChat) -> str:
    return dispatcher.generate_answer(result = await Router.setGroupChat(params.chat_id, params.group))

@SocketRoute.on_message(target="CreateChat", private = True)
async def createchat(token: str, params: CreateChat) -> str:
    return dispatcher.generate_answer(result = await Router.NewChat(
        params.creator_id, params.chat_id, params.group
    ))

@SocketRoute.on_message(target="DeleteChat", private = True)
async def deletechat(token: str, params: DeleteChat) -> str:
    return dispatcher.generate_answer(result = await Router.deleteChat(params.chat_id))