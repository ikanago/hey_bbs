from __future__ import annotations
from libbbs.body import Body
from typing import Optional
from libbbs.header_map import HeaderMap
from libbbs.misc import StatusCode, Mime
import dataclasses
import socket


@dataclasses.dataclass
class Response:
    version: bytes = b"HTTP/1.1"
    status_code: StatusCode = StatusCode.OK
    headers: HeaderMap = dataclasses.field(init=False)
    body: Optional[Body] = dataclasses.field(default=None)

    def __post_init__(self):
        self.headers = HeaderMap()

    def get(self, key: str) -> Optional[str]:
        r""" Get header value.

        Parameters
        ----------
        key: str
            Header name to get.

        Returns
        -------
        str
            Header value corresponding to the key.
        """
        if not isinstance(key, str):
            raise KeyError
        return self.headers.get(key)

    def set(self, key: str, value: str):
        r""" Set header value to the key.

        Parameters
        ----------
        key: str
            Header name to set.
        value: str
            Header value to set.
        """
        if not isinstance(key, str):
            raise KeyError
        self.headers.set(key, value)

    def send(self, socket: socket.socket):
        socket.send(b"%b %d %b\r\n" % (
            self.version, self.status_code.value, self.status_code.to_bytes()))
        for key, value in iter(self.headers):
            socket.send(b"%b: %b\r\n" %
                        (bytes(key, "utf-8"), bytes(value, "utf-8")))
        socket.send(b"\r\n")
        if self.body is not None:
            socket.send(self.body.to_bytes())

    def is_success(self) -> bool:
        return self.status_code.is_success()

    def is_failure(self) -> bool:
        return self.status_code.is_failure()

    def set_body(self, to_body: Body, mime_type: Optional[str] = None):
        self.body = to_body
        self.set("Content-Length", str(len(self.body)))
        if mime_type is None:
            self.set("Content-Type", Mime.TEXT_PLAIN)
        else:
            self.set("Content-Type", mime_type)


def moved_permanently(uri: str) -> Response:
    res = Response(status_code=StatusCode.MovedPermanently)
    res.set("Location", uri)
    return res


def found(uri: str) -> Response:
    res = Response(status_code=StatusCode.Found)
    res.set("Location", uri)
    return res


def see_other(uri: str) -> Response:
    res = Response(status_code=StatusCode.SeeOther)
    res.set("Location", uri)
    return res
