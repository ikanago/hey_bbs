from __future__ import annotations
from enum import Enum, auto


class Method(Enum):
    GET = b"GET"

    def __str__(self) -> str:
        self.value

    @staticmethod
    def from_bytes(method: bytes) -> Method:
        if method == b"GET":
            return Method.GET


class StatusCode(Enum):
    OK = 200
    NOT_FOUND = 404

    def to_bytes(self) -> bytes:
        if self == StatusCode.OK:
            return b"OK"
        elif self == StatusCode.NOT_FOUND:
            return b"Not Found"


class HttpError(Exception):
    pass


class BadRequest(HttpError):
    pass
