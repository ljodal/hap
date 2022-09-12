import asyncio
import logging
from urllib.parse import parse_qs, unquote

import h11

from .app import App
from .request import Request, Session

logger = logging.getLogger(__name__)


class HTTPProtocol(asyncio.Protocol):
    transport: asyncio.WriteTransport
    connection: h11.Connection

    def __init__(self, app: App) -> None:
        self.app = app
        self.app_task: asyncio.Task[None] | None = None
        self.request: h11.Request | None = None
        self.data: list[h11.Data] = []
        self.session = Session()

    # Protocol interface

    def connection_made(self, transport: asyncio.BaseTransport) -> None:
        print("Connection received")
        assert isinstance(transport, asyncio.WriteTransport)
        self.transport = transport
        self.connection = h11.Connection(h11.SERVER)

    def data_received(self, data: bytes) -> None:
        print("Data received")
        if data:
            self.connection.receive_data(data)
        self.process_events()

    def eof_received(self) -> None:
        print("Connection closed")
        self.connection.receive_data(b"")
        self.process_events()

    def connection_lost(self, exc: Exception | None) -> None:
        print("Connection lost")
        self.connection.receive_data(b"")
        self.process_events()

    # h11/asgi event processing

    def process_events(self) -> None:
        # Do not process incoming events if we're already processing a request
        if self.app_task:
            return

        try:
            while True:
                event = self.connection.next_event()
                if event in (h11.NEED_DATA, h11.PAUSED):
                    break
                if isinstance(event, h11.Request):
                    assert not self.request
                    assert not self.data
                    self.request = event
                elif isinstance(event, h11.Data):
                    self.data.append(event)
                elif isinstance(event, (h11.ConnectionClosed, h11.EndOfMessage)):
                    if self.request:
                        self.app_task = asyncio.ensure_future(self.process_request())
                    break
                else:
                    raise RuntimeError(f"Unsupported event: {event}")
        except h11.RemoteProtocolError:
            print("Remote protocol error, closing connection")
            self.transport.close()

    async def process_request(self) -> None:
        print("Process request")
        assert self.request
        path, _, query_string = self.request.target.partition(b"?")
        request = Request(
            method=self.request.method.decode(),
            path=unquote(path.decode()),
            query=parse_qs(query_string.decode(), keep_blank_values=True),
            headers=tuple(self.request.headers),
            body=b"".join(data.data for data in self.data),
            session=self.session,
        )

        print("Calling app")
        try:
            response = await self.app(request)
        except Exception:
            # TODO: Return 500 internal error
            logger.exception("Error while processing request")
            return

        print("Writing response")

        if data := self.connection.send(
            h11.Response(
                status_code=response.status,
                headers=[(b"content-type", response.content_type)],
            )
        ):
            self.transport.write(data)
        if data := self.connection.send(h11.Data(response.body)):
            self.transport.write(data)
        if data := self.connection.send(h11.EndOfMessage()):
            self.transport.write(data)
        self.connection.start_next_cycle()

        print("Wrote response")

        # Make sure we process any pending events
        asyncio.get_running_loop().call_soon(self.process_events)

        self.request = None
        self.data = []
        self.app_task = None
