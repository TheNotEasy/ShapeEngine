import socket
import asyncio
from typing import Optional, Coroutine


class Server:
    def __init__(self):
        self.loop = asyncio.get_event_loop()
        self.socket: Optional[Coroutine] = None

    def parse_response(self, response):
        pass

    async def accept_client(self, reader, writer):
        pass

    async def _run(self):
        self.socket = await asyncio.start_server(self.accept_client, '0.0.0.0', 9999)
        async with self.socket:
            await self.socket.serve_forever()

    def run(self):
        self.loop.run_in_executor(None, self._run)
