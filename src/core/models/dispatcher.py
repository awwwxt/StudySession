from core.database import Router
from config import logger, SimmetricHashFunc, APITOKEN
from core.tools import check_on_symbols
from core import models

from typing import Callable, Dict, Any
from asyncio import Future
from re import compile, match
from json import dumps

class Dispatcher:
    def __init__(self):
        self.handlers = {}

    def register_handler(self, target: str, private: bool, handler: Callable[[Dict[str, str]], Future]):
        self.handlers[target] = {"private": private, "func": handler}

    async def dispatch(self, message: str) -> str:
        response = self.generate_answer(False, reason = "Bad request", message = message)
        target = message.pop("target")
        token = message.pop("token")
        if target and token:
            if check_on_symbols(token) and (token == APITOKEN or \
                                                await Router.getUserByToken(token)):
                if target in self.handlers.keys():
                    logger.info(f"handler for {target} founded")
                    handler = self.handlers[target]
                    if not handler["private"] or APITOKEN == token:
                        obj = getattr(models, target)                            
                        response = await handler['func'](token, obj(**message))
                    else:
                        response = self.generate_answer(False, reason = "Private method")
                else:
                    logger.info(f"handler for {target} not founded")
                    response = self.generate_answer(False, reason = "Unknown method")
            else:
                response = self.generate_answer(False, reason = "Bad access token")
        return response
    
    @staticmethod
    def generate_answer(success: bool = True, **kwargs: str) -> str:
        return dumps({
            "status": "success" if success else "error",
            **kwargs
        })