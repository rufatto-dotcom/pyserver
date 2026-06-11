from server.core.server import Server
import server.routes

server = Server()

async def main():
    await server.start()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())