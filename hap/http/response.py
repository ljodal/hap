import json
from typing import Any

from .. import tlv


class Response:
    def __init__(
        self,
        body: bytes,
        status: int,
        content_type: bytes,
    ) -> None:
        self.body = body
        self.status = status
        self.content_type = content_type


class BadRequest(Response):
    def __init__(self, body: bytes) -> None:
        super().__init__(body, status=400, content_type=b"text/plain")


class UnprocessableEntity(Response):
    def __init__(self, body: bytes) -> None:
        super().__init__(body, status=422, content_type=b"text/plain")


class JSONResponse(Response):
    def __init__(self, data: Any, status: int = 200) -> None:
        super().__init__(
            json.dumps(data).encode(), status=status, content_type=b"application/json"
        )


class PairingResponse(Response):
    def __init__(self, *values: tuple[tlv.TLVType, bytes], status: int = 200) -> None:
        super().__init__(
            tlv.encode(values), status=status, content_type=b"application/pairing+tlv8"
        )
