from __future__ import annotations
from enum import Enum


class Method(Enum):
    GET = b"GET"
    POST = b"POST"
    OPTIONS = b"OPTIONS"

    def __str__(self) -> str:
        return self.value.decode()

    @staticmethod
    def from_bytes(method: bytes) -> Method:
        if method == b"GET":
            return Method.GET
        elif method == b"POST":
            return Method.POST
        elif method == b"OPTIONS":
            return Method.OPTIONS
        else:
            raise BadRequest


class StatusCode(Enum):
    OK = 200
    MovedPermanently = 301
    Found = 302
    SeeOther = 303
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    NOT_FOUND = 404
    INTERNAL_SERVER_ERROR = 500

    def to_bytes(self) -> bytes:
        if self == StatusCode.OK:
            return b"OK"
        elif self == StatusCode.MovedPermanently:
            return b"Moved Permanently"
        elif self == StatusCode.Found:
            return b"Found"
        elif self == StatusCode.SeeOther:
            return b"See Other"
        elif self == StatusCode.BAD_REQUEST:
            return b"Bad Request"
        elif self == StatusCode.UNAUTHORIZED:
            return b"Unauthorized"
        elif self == StatusCode.NOT_FOUND:
            return b"Not Found"
        else:
            # Unreachable, though
            return b"Unknown"

    def is_success(self) -> bool:
        return 200 <= self.value < 400

    def is_redirect(self) -> bool:
        return 300 <= self.value < 400

    def is_failure(self) -> bool:
        return 400 <= self.value < 600


class Mime:
    APPLICATION_JSON = "application/json"
    IMAGE_JPG = "image/jpeg"
    IMAGE_PNG = "image/png"
    TEXT_CSS = "text/css"
    TEXT_HTML = "text/html"
    TEXT_JAVASCRIPT = "text/javascript"
    TEXT_PLAIN = "text/plain"

    def from_filename(filename: str) -> Mime:
        extension = filename.split(".")[-1]
        if extension == "json":
            return Mime.APPLICATION_JSON
        elif extension == "png":
            return Mime.IMAGE_PNG
        elif extension == "jpg" or extension == "jpeg":
            return Mime.IMAGE_JPG
        elif extension == "css":
            return Mime.TEXT_CSS
        elif extension == "htm" or extension == "html":
            return Mime.TEXT_HTML
        elif extension == "js":
            return Mime.TEXT_JAVASCRIPT
        else:
            return Mime.TEXT_PLAIN


class HttpError(Exception):
    pass


class BadRequest(HttpError):
    pass


class InternalServerError(HttpError):
    pass
