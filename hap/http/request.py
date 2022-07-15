import json
from dataclasses import dataclass, field
from functools import cached_property
from typing import Any

from .. import tlv
from ..crypto import srp


@dataclass
class Request:
    method: str
    path: str
    body: bytes
    query: dict[str, list[str]] = field(default_factory=dict)
    headers: tuple[tuple[bytes, bytes], ...] = ()

    # TODO: Extract to a separate Session class
    srp_session: srp.Server | None = None

    @cached_property
    def content_type(self) -> bytes | None:
        return next(
            (value for key, value in self.headers if key == b"content-type"),
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
