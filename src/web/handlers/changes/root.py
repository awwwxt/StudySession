from web.web import SocketRoute, dispatcher
from core.models import NewUser, DeleteUser, ActivateKey, RemoveRole, \
                             CreateInviteKey, DeleteKey, RequestUpdate, RemoveInvited
from core.database import Router

from os import execv
from core.akvt.update import Updater
from sys import argv, executable

@SocketRoute.on_message(target="NewUser", private = True)
async def newuser(token: str, params: NewUser) -> str:
    return dispatcher.generate_answer(result = await Router.NewUser(params.user_id, params.invited_by))

@SocketRoute.on_message(target="DeleteUser", private = True)
async def deleteuser(token: str, params: DeleteUser) -> str:
    return dispatcher.generate_answer(result = await Router.deleteUser(params.user_id))

@SocketRoute.on_message(target="ActivateKey", private = True)
async def activatekey(token: str, params: ActivateKey) -> str:
    return dispatcher.generate_answer(result = await Router.activateKey(params.user_id, params.key))

@SocketRoute.on_message(target="RemoveRole", private = True)
async def removerole(token: str, params: RemoveRole) -> str:
    return dispatcher.generate_answer(result = await Router.removeRole(params.user_id))

@SocketRoute.on_message(target="CreateInviteKey", private = True)
async def createinvitekey(token: str, params: CreateInviteKey) -> str:
    return dispatcher.generate_answer(result = await Router.createInviteKey(params.uid, params.role))

@SocketRoute.on_message(target="DeleteKey", private = True)
async def deletekey(token: str, params: DeleteKey) -> str:
    return dispatcher.generate_answer(result = await Router.deleteKey(params.uid, params.key))

@SocketRoute.on_message(target="RequestUpdate", private = True)
async def requestupdate(token: str, params: RequestUpdate) -> str:
        updater = Updater()
        if await updater.start():
            execv(executable, [executable, argv[0]] + argv[1:])  
        else:
            return dispatcher.generate_answer(False, reason = "Unknown error")
        
@SocketRoute.on_message(target="RemoveInvited", private = True)
async def removeinvited(token: str, params: RemoveInvited) -> str:
    return dispatcher.generate_answer(result = await Router.deleteInvited(params.user_id, params.role))