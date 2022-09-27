import json
from typing import Any

from .. import tlv


class Response:
    def __init__(
        self,
        body: bytes,
        status: int,
        content_type: str,
        **headers: str,
    ) -> None:
        self.body = body
        self.status = status
        self.headers = [("content-type", content_type)]
        if headers:
            self.headers += headers.items()


class BadRequest(Response):
    def __init__(self, body: bytes) -> None:
        super().__init__(body, status=400, content_type="text/plain")


class UnprocessableEntity(Response):
    def __init__(self, body: bytes) -> None:
        super().__init__(body, status=422, content_type="text/plain")


class JSONResponse(Response):
    def __init__(self, data: Any, status: int = 200) -> None:
        super().__init__(
            json.dumps(data).encode(), status=status, content_type="application/json"
        )


class TLVResponse(Response):
    def __init__(self, *values: tlv.TLV[Any], status: int = 200) -> None:
        super().__init__(
            tlv.encode(*values), status=status, content_type="application/pairing+tlv8"
        )
