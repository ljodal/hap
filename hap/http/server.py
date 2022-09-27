import asyncio
import contextlib
import logging
from asyncio import ALL_COMPLETED, StreamReader, StreamWriter
from typing import AsyncIterator
from urllib.parse import parse_qs, unquote

import h11

from .app import App
from .request import Request, Session
from .response import Response

logger = logging.getLogger("hap.http")


async def handle_connection(
    reader: StreamReader, writer: StreamWriter, *, app: App
) -> None:
    """
    Handle an incoming connection. This coroutine will run for as long as the
    connection is alive.
    """

    # Every new connection starts out with a clean connection and session state
    connection = h11.Connection(h11.SERVER)
    session = Session()

    async def next_event() -> h11.Event | type[h11._util.Sentinel]:
        """Get the next event, potentially reading more data"""
        while True:
            event = connection.next_event()
            if event is h11.NEED_DATA:
                data = await asyncio.wait_for(reader.read(1024), timeout=1000)
                connection.receive_data(data)
                continue

            return event

    async def read_body() -> bytes:
        """Read data until we've received the full http request"""
        body = b""

        while True:
            event = await next_event()
            if isinstance(event, h11.EndOfMessage):
                break
            assert isinstance(event, h11.Data)
            body += event.data

        return body

    async def send(response: Response) -> None:
        events = [
            h11.Response(
                status_code=response.status,
                headers=(
                    response.headers + [("content-length", str(len(response.body)))]
                ),
            ),
            h11.Data(response.body),
            h11.EndOfMessage(),
        ]

        try:
            for event in events:
                if data := connection.send(event):
                    writer.write(data)
            await writer.drain()
        except Exception:
            connection.send_failed()
            raise

    async def maybe_send_error(status: int, body: bytes) -> None:
        if connection.our_state is not h11.SEND_RESPONSE:
            logger.error(
                "Not in a state where we can send an error message: %s",
                connection.our_state,
            )
            return

        try:
            response = Response(
                body=body,
                status=status,
                content_type="text/plain",
                connection="close",
            )
            await send(response)
        except Exception:
            logger.exception("Failed to send error response")

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
            response = Response(body=b"", status=500, content_type="text/html")

        # Send the response
        await send(response)

        connection.start_next_cycle()

    try:
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

            if connection.our_state is h11.MUST_CLOSE:
                break
    except h11.RemoteProtocolError as e:
        logger.exception("Remote protocol error")
        await maybe_send_error(
            status=e.error_status_hint, body=b"Unexpected data received"
        )
    except asyncio.TimeoutError:
        logger.info("Timeout error, closing connection")
        await maybe_send_error(status=408, body=b"Timeout")
    except Exception:
        logger.exception("An error occured")
        await maybe_send_error(status=500, body=b"An error occured")
    finally:
        if writer.can_write_eof():
            writer.write_eof()
            await writer.drain()


@contextlib.asynccontextmanager
async def serve(
    *, host: str = "127.0.0.1", port: int = 8080
) -> AsyncIterator[asyncio.Server]:

    app = App()
    tasks = []

    async def connection_made(reader: StreamReader, writer: StreamWriter) -> None:
        if task := asyncio.current_task():
            tasks.append(task)
            task.set_name(f"Request handler {len(tasks)}")
        try:
            await handle_connection(reader, writer, app=app)
        except Exception:
            logger.exception("An error occured while handling a request")

        # Remove task again when we're done
        if task:
            tasks.remove(task)

    server = await asyncio.start_server(connection_made, host, port)

    try:
        async with server:
            await server.start_serving()
            yield server
    except asyncio.CancelledError:
        pass
    finally:
        for task in tasks:
            task.cancel()
        if tasks:
            await asyncio.wait(tasks, return_when=ALL_COMPLETED)


async def main() -> None:
    async with serve() as server:
        await server.serve_forever()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
