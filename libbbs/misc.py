from __future__ import annotations
from enum import Enum, auto


class Method(Enum):
    GET = auto()

    def __str__(self) -> str:
        if self == Method.GET:
            return "GET"

    @staticmethod
    def from_bytes(method: bytes) -> Method:
        if method == "GET":
            return Method.GET


class HttpError(Exception):
    pass


class BadRequest(HttpError):
    pass
