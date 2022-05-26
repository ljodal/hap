import asyncio

from .api import index
from .app import App
from .protocol import HTTPProtocol


async def serve(*, host: str = "127.0.0.1", port: int = 8080) -> None:
    app = App({("GET", "/"): index})
    loop = asyncio.get_running_loop()
    server = await loop.create_server(lambda: HTTPProtocol(asgi_app=app), host, port)
    async with server:
        await server.serve_forever()


if __name__ == "__main__":
    asyncio.run(serve())
