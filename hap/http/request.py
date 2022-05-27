import json
from dataclasses import dataclass
from functools import cached_property
from typing import Any
from urllib.parse import parse_qs

from .. import tlv
from ..crypto import srp
from .asgi import HTTPScope


@dataclass
class Request:
    scope: HTTPScope
    body: bytes

    @property
    def method(self) -> str:
        return self.scope["method"]

    @property
    def path(self) -> str:
        return self.scope["path"]

    @property
    def srp_session(self) -> srp.Server | None:
        # Extract the SRP session from the scope
        match self.scope["extensions"]:
            case {"hap": {"srp": srp.Server() as srp_session}}:
                return srp_session

        return None

    @cached_property
    def query(self) -> dict[str, list[str]]:
        return parse_qs(self.scope["query_string"].decode(), keep_blank_values=True)

    @cached_property
    def content_type(self) -> bytes | None:
        return next(
            (value for key, value in self.scope["headers"] if key == b"content-type"),
            None,
        )

    def tlv(self) -> list[tlv.TLV[Any]]:
        if self.content_type != b"application/pairing+tlv8":
            raise ValueError("Request does not contain TLV data")

        return tlv.decode(self.body)

    def json(self) -> Any:
        if self.content_type != b"application/json":
            raise ValueError("Request does not contain JSON data")

        return json.loads(self.body)
