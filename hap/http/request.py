from dataclasses import dataclass


@dataclass
class Request:
    method: str
    path: str
    query: dict[str, list[str]]
    body: str
