import json
from dataclasses import InitVar, dataclass
from typing import Any


@dataclass
class Response:
    body: bytes
    status: int = 200
    content_type: bytes = b"text/plain"


@dataclass
class BadRequest(Response):
    status: int = 400


@dataclass
class JSONResponse(Response):
    body: bytes = b""
    content_type: bytes = b"application/json"
    data: InitVar[Any] = None

    def __post_init__(self, data: Any) -> None:
        self.body = json.dumps(data).encode()
