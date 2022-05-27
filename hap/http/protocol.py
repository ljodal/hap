import asyncio
from urllib.parse import unquote

import h11

from ..crypto.srp import SRP
from .asgi import (
    ASGIApplication,
    ASGIReceiveEvent,
    ASGISendEvent,
    HTTPRequestEvent,
    HTTPScope,
)


class HTTPProtocol(asyncio.Protocol):
    transport: asyncio.WriteTransport
    connection: h11.Connection

    def __init__(self, asgi_app: ASGIApplication) -> None:
        self.app = asgi_app
        self.to_app: asyncio.Queue[ASGIReceiveEvent] | None = None
        self.app_task: asyncio.Task[None] | None = None
        self.srp: SRP | None = None

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
        try:
            while True:
                event = self.connection.next_event()
                if event in (h11.NEED_DATA, h11.PAUSED):
                    break
                if isinstance(event, h11.Request):
                    self.request_received(event)
                elif isinstance(event, h11.Data):
                    assert self.to_app
                    self.to_app.put_nowait(
                        HTTPRequestEvent(
                            type="http.request", body=event.data, more_body=True
                        )
                    )
                elif isinstance(event, (h11.ConnectionClosed, h11.EndOfMessage)):
                    if self.to_app:
                        self.to_app.put_nowait(
                            HTTPRequestEvent(
                                type="http.request", body=b"", more_body=False
                            )
                        )
                    break
                else:
                    print(f"Unsupported event: {event}")
                    break
        except h11.RemoteProtocolError:
            print("Remote protocol error, closing connection")
            self.transport.close()

    def request_received(self, request: h11.Request) -> None:
        self.to_app = asyncio.Queue()
        path, _, query_string = request.target.partition(b"?")
        scope = HTTPScope(
            type="http",
            asgi={"version": "3.0", "spec_version": "2.3"},
            http_version=request.http_version.decode(),
            method=request.method.decode(),
            scheme="http",
            path=unquote(path.decode("ascii")),
            raw_path=request.target,
            query_string=query_string,
            root_path="",
            headers=request.headers,
            client=None,
            server=None,
            extensions={
                "hap": {"is_secure": False, "srp": self.srp},
            },
        )
        self.app_task = asyncio.ensure_future(
            self.app(scope, self.to_app.get, self.app_send)
        )

    async def app_send(self, event: ASGISendEvent) -> None:
        if self.transport.is_closing():
            print(f"Received event {event} after transport was closed")
            return

        if event["type"] == "http.response.start":
            self.transport.write(
                self.connection.send(
                    h11.Response(
                        status_code=event["status"],
                        headers=[
                            (key.decode(), value.decode())
                            for key, value in event["headers"]
                        ],
                    )
                )
            )
        elif event["type"] == "http.response.body":
            self.transport.write(self.connection.send(h11.Data(event["body"])))
            if not event["more_body"]:
                print("No more body, resetting connection")
                self.connection.start_next_cycle()
        elif event["type"] == "hap.srp":
            self.srp = event["srp"]
        else:
            raise ValueError(f"Unsupported ASGI event: {event['type']}")
