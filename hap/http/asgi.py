from typing import Awaitable, Callable, Iterable, Literal, TypedDict


class ASGIVersions(TypedDict):
    spec_version: str
    version: Literal["2.0", "3.0"]


class HTTPScope(TypedDict):
    type: Literal["http"]
    asgi: ASGIVersions
    http_version: str
    method: str
    scheme: str
    path: str
    raw_path: bytes
    query_string: bytes
    root_path: str
    headers: Iterable[tuple[bytes, bytes]]
    client: tuple[str, int] | None
    server: tuple[str, int | None] | None
    extensions: dict[str, dict[object, object]] | None


class HTTPRequestEvent(TypedDict):
    type: Literal["http.request"]
    body: bytes
    more_body: bool


class HTTPResponseStartEvent(TypedDict):
    type: Literal["http.response.start"]
    status: int
    headers: Iterable[tuple[bytes, bytes]]


class HTTPResponseBodyEvent(TypedDict):
    type: Literal["http.response.body"]
    body: bytes
    more_body: bool


class HTTPDisconnectEvent(TypedDict):
    type: Literal["http.disconnect"]


ASGIReceiveEvent = HTTPRequestEvent | HTTPDisconnectEvent
ASGISendEvent = HTTPResponseStartEvent | HTTPResponseBodyEvent | HTTPDisconnectEvent

Scope = HTTPScope
ASGIReceiveCallable = Callable[[], Awaitable[ASGIReceiveEvent]]
ASGISendCallable = Callable[[ASGISendEvent], Awaitable[None]]


ASGIApplication = Callable[
    [Scope, ASGIReceiveCallable, ASGISendCallable],
    Awaitable[None],
]
