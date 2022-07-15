import asyncio
import json as _json
from typing import Any, Iterable

from hap.http.app import App
from hap.http.request import Request, Session
from hap.http.response import Response
from hap.tlv import TLV
from hap.tlv import encode as encode_tlv


class Client:
    """
    Client for the HTTP server.
    """

    def __init__(self) -> None:
        self.app = App()
        self.session = Session()

    def request(
        self,
        method: str,
        path: str,
        *,
        headers: dict[str, str] | None = None,
        json: Any = None,
        tlv: Iterable[TLV[Any]] | None = None,
    ) -> Response:

        headers = headers.copy() if headers else {}

        body = b""
        if json is not None:
            body = _json.dumps(json).encode("utf-8")
            headers["content-type"] = "application/json"
        elif tlv is not None:
            body = encode_tlv(*tlv)
            headers["content-type"] = "application/pairing+tlv8"

        request = Request(
            method=method,
            path=path,
            headers=tuple(
                (key.encode(), value.encode()) for key, value in headers.items()
            ),
            body=body,
            session=self.session,
        )

        # Run the app until it exits and assume it's done all its work by then
        return asyncio.run(self.app(request))

    def get(self, path: str, *, headers: dict[str, str] | None = None) -> Response:
        return self.request("GET", path, headers=headers)

    def post(
        self,
        path: str,
        *,
        headers: dict[str, str] | None = None,
        json: Any = None,
        tlv: Iterable[TLV[Any]] | None = None,
    ) -> Response:
        return self.request("POST", path, headers=headers, json=json, tlv=tlv)
