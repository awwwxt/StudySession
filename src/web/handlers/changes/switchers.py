from web.web import SocketRoute, dispatcher
from core.models import SwitchAccess, SwitchBan    
from core.tools import GetFonts, colors, sync_to_async
from core.database import Router

from typing import Dict

@SocketRoute.on_message(target="SwitchBan", private = True)
async def switchban(token: str, params: SwitchBan) -> str:
    return dispatcher.generate_answer(result = await Router.setBan(params.user_id, params.ban))

@SocketRoute.on_message(target="SwitchAccess", private = True)
async def switchaccess(token: str, params: SwitchAccess) -> str:
    return dispatcher.generate_answer(result = await Router.setAccess(params.user_id, params.access))
    