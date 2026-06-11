import asyncio
from .handler import handle_client_connection

class Server:
    def __init__(self, host="127.0.0.1", port=8080, handler=handle_client_connection):
        self.host = host
        self.port = port
        self.handler = handler
        self.server = None
            
    async def start(self):
        self.server = await asyncio.start_server(
            self.handler,
            self.host,
            self.port
        )

        print(f"Servidor rodando em {self.host}:{self.port}")
        
        async with self.server:
            await self.server.serve_forever()