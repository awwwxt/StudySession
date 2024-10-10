from config import logger, MAX_BUFFER_LENGHT
from core.models import BaseTCPServer, dispatcher
from core.errors import BadParams

from asyncio import Future, StreamReader, StreamWriter
from typing import Callable, Dict
from json import loads

class WebServer(BaseTCPServer):
    def __init__(self):
        super().__init__()

    def on_message(self, target: str, private: bool = False) -> Callable[[Callable[[Dict[str, str]], Future]], Callable[[Dict[str, str]], Future]]:
        def decorator(func: Callable[[Dict[str, str]], Future]):
            dispatcher.register_handler(target, private, func)
            return func
        return decorator

    async def handle_client(self, reader: StreamReader, writer: StreamWriter):
        addr = writer.get_extra_info('peername')
        logger.warning(f"Accepted connection from {addr}")
        try:
            while True:
                data = await reader.read(MAX_BUFFER_LENGHT)
                if not data:
                    break
                logger.info(f"Received {len(data)} bytes from {addr}")
                try:
                  response = await dispatcher.dispatch(loads(data.decode()))
                except BadParams:
                    response = dispatcher.generate_answer(False, reason="Invalid params")
                except:
                    response = dispatcher.generate_answer(False, reason="Server or method error")
                response_data = response.encode()
                writer.write(response_data)
                await writer.drain()
                logger.success(f"Sent {len(response_data)} bytes to {addr}")

        except Exception as e:
            logger.error(f"{e} from {addr}")
        finally:
            logger.info(f"Closing connection {addr}")
            writer.close()
            await writer.wait_closed()
