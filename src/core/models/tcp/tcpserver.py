from config import TCP_IP, TCP_PORT, logger, KEYS

from asyncio import start_server, StreamReader, StreamWriter
from ssl import SSLContext, PROTOCOL_TLS_SERVER
from typing import Any
from abc import ABC, abstractmethod

class BaseTCPServer(ABC):
    
    @staticmethod
    def load_context(keys):
        context = SSLContext(PROTOCOL_TLS_SERVER)
        context.load_cert_chain(keys[0], keys[1])
        return context
        
    @abstractmethod
    async def handle_client(self, reader: StreamReader, writer: StreamWriter) -> Any:
        ...
        
    async def start(self) -> None:
        server = await start_server(
            self.handle_client, TCP_IP, TCP_PORT,
            ssl = self.load_context((f'{KEYS}cert.pem', f'{KEYS}key.pem'))
        )
        ip = server.sockets[0].getsockname()
        logger.success(f"Starting TCP at {ip[0]}:{ip[1]}")

        async with server:
            await server.serve_forever()