from __future__ import annotations
from enum import Enum


class Method(Enum):
    GET = b"GET"
    POST = b"POST"

    def __str__(self) -> str:
        self.value

    @staticmethod
    def from_bytes(method: bytes) -> Method:
        if method == b"GET":
            return Method.GET
        elif method == b"POST":
            return Method.POST
        else:
            raise BadRequest


class StatusCode(Enum):
    OK = 200
    BAD_REQUEST = 400
    NOT_FOUND = 404

    def to_bytes(self) -> bytes:
        if self == StatusCode.OK:
            return b"OK"
        elif self == StatusCode.BAD_REQUEST:
            return b"Bad Request"
        elif self == StatusCode.NOT_FOUND:
            return b"Not Found"

    def is_success(self) -> bool:
        return 200 <= self.value < 400

    def is_failure(self) -> bool:
        return 400 <= self.value < 600


class HttpError(Exception):
    pass


class BadRequest(HttpError):
    pass
