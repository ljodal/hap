import json
from dataclasses import dataclass
from functools import cached_property
from typing import Any
from urllib.parse import parse_qs

from hap.http.asgi import HTTPScope

from .. import tlv


@dataclass
class Request:
    body: bytes
    scope: HTTPScope

    @property
    def method(self) -> str:
        return self.scope["method"]

    @property
    def path(self) -> str:
        return self.scope["path"]

    @cached_property
    def query(self) -> dict[str, list[str]]:
        return parse_qs(self.scope["query_string"].decode(), keep_blank_values=True)

    @cached_property
    def content_type(self) -> bytes | None:
        return next(
            (value for key, value in self.scope["headers"] if key == b"content-type"),
            None,
        )

    def tlv(self) -> list[tuple[tlv.TLVType, bytes]]:
        if self.content_type != b"application/pairing+tlv8":
            raise ValueError("Request does not contain TLV data")

        return tlv.decode(self.body)

    def json(self) -> Any:
        if self.content_type != b"application/json":
            raise ValueError("Request does not contain JSON data")

        return json.loads(self.body)
