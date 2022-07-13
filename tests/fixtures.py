import asyncio
import json as _json
from dataclasses import dataclass
from typing import Any, Iterable

from hap import tlv as _tlv
from hap.crypto.srp import SRP
from hap.http.app import App
from hap.http.asgi import ASGIReceiveEvent, ASGISendEvent, HTTPScope


class Client:
    """
    Client for the HTTP server.
    """

    @dataclass
    class Response:
        """
        A simple wrapper around ASGI responses.
        """

        status: int
        headers: dict[str, str]
        body: bytes

        def tlv(self) -> list[_tlv.TLV[Any]]:
            return _tlv.decode(self.body)

    def __init__(self) -> None:
        self.app = App()
        self.srp_session: SRP | None = None

    def request(
        self,
        method: str,
        path: str,
        *,
        headers: dict[str, str] | None = None,
        json: Any = None,
        tlv: Iterable[_tlv.TLV[Any]] | None = None,
    ) -> Response:

        headers = headers.copy() if headers else {}

        body = b""
        if json is not None:
            body = _json.dumps(json).encode("utf-8")
            headers["content-type"] = "application/json"
        elif tlv is not None:
            body = _tlv.encode(*tlv)
            headers["content-type"] = "application/pairing+tlv8"

        scope = HTTPScope(
            type="http",
            asgi={"spec_version": "2.3", "version": "3.0"},
            http_version="1.1",
            method=method,
            scheme="http",
            path=path,
            raw_path=path.encode(),
            query_string=b"",
            root_path="",
            headers=(
                (key.encode(), value.encode()) for key, value in (headers or {}).items()
            ),
            client=None,
            server=None,
            extensions={"hap": {"srp": self.srp_session}},
        )

        async def receive() -> ASGIReceiveEvent:
            return {"type": "http.request", "body": body, "more_body": False}

        send_events: list[ASGISendEvent] = []

        async def send(event: ASGISendEvent) -> None:
            send_events.append(event)

        # Run the app until it exits and assume it'd one all it's work by then
        asyncio.run(self.app(scope, receive, send))

        # We should have received some send events, and the first one should be
        # an http.response.start event
        assert send_events
        start = send_events.pop(0)
        assert start["type"] == "http.response.start"

        body = b""
        while send_events:
            event = send_events.pop(0)
            if event["type"] == "http.response.body":
                body += event["body"]
            elif event["type"] == "hap.srp":
                assert self.srp_session is None
                self.srp_session = event["srp"]
            else:
                raise ValueError(f"Unsupported event: {event}")

        return self.Response(
            status=start["status"],
            headers={key.decode(): value.decode() for key, value in start["headers"]},
            body=body,
        )

    def get(
        self,
        path: str,
        *,
        headers: dict[str, str] | None = None,
        json: Any = None,
        tlv: Iterable[_tlv.TLV[Any]] | None = None,
    ) -> Response:
        return self.request("GET", path, headers=headers, json=json, tlv=tlv)

    def post(
        self,
        path: str,
        *,
        headers: dict[str, str] | None = None,
        json: Any = None,
        tlv: Iterable[_tlv.TLV[Any]] | None = None,
    ) -> Response:
        return self.request("POST", path, headers=headers, json=json, tlv=tlv)
