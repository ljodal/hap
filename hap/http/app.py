"""
This module implements a simple ASGI application that handles incoming requests
from the home controller.
"""

from typing import Awaitable

from .api import HANDLERS
from .request import Request
from .response import Response

RESPONSE_404 = Response(status=404, body=b"", content_type="text/plain")


class App:
    async def __call__(self, request: Request) -> Response:

        response = self.handle(request)
        if not isinstance(response, Response):
            response = await response

        return response

    def handle(self, request: Request) -> Awaitable[Response] | Response:

        method = "GET" if request.method == "HEAD" else request.method

        # Find the handler for this request and call it
        if handler := HANDLERS.get((method, request.path), None):
            return handler(request)

        return RESPONSE_404
