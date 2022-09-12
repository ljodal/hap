import asyncio
import functools
import logging
from asyncio import StreamReader, StreamWriter
from urllib.parse import parse_qs, unquote

import h11

from .app import App
from .request import Request, Session
from .response import Response

logger = logging.getLogger("hap.http")


async def handle_connection(
    reader: StreamReader, writer: StreamWriter, *, app: App
) -> None:

    # Every new connection starts out with a clean connection and session state
    connection = h11.Connection(h11.SERVER)
    session = Session()

    async def next_event() -> h11.Event | type[h11._util.Sentinel]:
        """Helper to get the next event, potentially reading more data"""
        while True:
            event = connection.next_event()
            if event is h11.NEED_DATA:
                connection.receive_data(await reader.read(1024))
                continue

            return event

    async def read_body() -> bytes:
        """Read data until we've received the full request body"""
        body = b""

        while True:
            event = await next_event()
            if isinstance(event, h11.EndOfMessage):
                break
            assert isinstance(event, h11.Data)
            body += event.data

        return body

    async def handle_request(event: h11.Request) -> None:
        """Handle a received request"""
        body = await read_body()

        path, _, query_string = event.target.partition(b"?")
        request = Request(
            method=event.method.decode(),
            path=unquote(path.decode()),
            query=parse_qs(query_string.decode(), keep_blank_values=True),
            headers=tuple(event.headers),
            body=body,
            session=session,
        )

        # Call the application to handle the request
        try:
            response = await app(request)
        except Exception:
            logger.exception("Error while processing request")
            response = Response(body=b"", status=500, content_type=b"text/html")

        # Send the response
        if data := connection.send(
            h11.Response(
                status_code=response.status,
                headers=[(b"content-type", response.content_type)],
            )
        ):
            writer.write(data)
        if data := connection.send(h11.Data(response.body)):
            writer.write(data)
        if data := connection.send(h11.EndOfMessage()):
            writer.write(data)

        await writer.drain()

        connection.start_next_cycle()

    while True:
        event = await next_event()
        if isinstance(event, h11.Request):
            logger.info("Request received: %s", event)
            await handle_request(event)
        elif isinstance(event, h11.ConnectionClosed):
            logger.info("Connection closed")
            break
        else:
            logger.warning("Unexpected event received: %s", event)


async def serve(*, host: str = "127.0.0.1", port: int = 8080) -> None:
    app = App()
    server = await asyncio.start_server(
        functools.partial(handle_connection, app=app), host, port
    )
    async with server:
        await server.serve_forever()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(serve())
