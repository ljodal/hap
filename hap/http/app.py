"""
This module implements a simple ASGI application that handles incoming requests
from the home controller.
"""

from typing import Awaitable, Callable

from .asgi import ASGIReceiveEvent, ASGISendEvent, HTTPScope
from .request import Request
from .response import Response

Handler = Callable[[Request], Awaitable[Response] | Response]

RESPONSE_404 = Response(status=404, body=b"", content_type=b"text/plain")


class App:
    def __init__(self, handlers: dict[tuple[str, str], Handler]) -> None:
        self.handlers = handlers

    async def __call__(
        self,
        scope: HTTPScope,
        receive: Callable[[], Awaitable[ASGIReceiveEvent]],
        send: Callable[[ASGISendEvent], Awaitable[None]],
    ) -> None:

        # Consume the entire body of the request
        body = bytearray()
        while True:
            event = await receive()
            if event["type"] == "http.request":
                body += event["body"]
                if not event["more_body"]:
                    break

        request = Request(scope=scope, body=body)

        print(f"Received request: {request}")

        response = self.handle(request)
        if not isinstance(response, Response):
            response = await response

        await send(
            {
                "type": "http.response.start",
                "status": response.status,
                "headers": [
                    (b"content-type", response.content_type),
                    (b"content-length", str(len(response.body)).encode()),
                ],
            }
        )
        await send(
            {
                "type": "http.response.body",
                "body": response.body if request.method != "HEAD" else b"",
                "more_body": False,
            }
        )

    def handle(self, request: Request) -> Awaitable[Response] | Response:

        method = "GET" if request.method == "HEAD" else request.method

        # Find the handler for this request and call it
        handler = self.handlers.get((method, request.path), None)
        if not handler:
            return RESPONSE_404

        return handler(request)
