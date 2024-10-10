from web import SocketRoute

import asyncio
import uvloop; uvloop.install()

logo = """\033[31m
01010011 01110100 01110101 01100100 01111001 01010011 01100101 01110011 01110011 01101001 01101111 01101110
\033[32m\n\tby awwwxt                                                               
"""

async def main() -> None:
    await SocketRoute.start()

if __name__ == "__main__":
    print(logo)
    asyncio.run(main())