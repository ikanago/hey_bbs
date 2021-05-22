from __future__ import annotations
from libbbs.header_map import HeaderMap
from libbbs.misc import StatusCode
import dataclasses
import socket


@dataclasses.dataclass
class Response:
    version: bytes = b"HTTP/1.1"
    status_code: StatusCode = StatusCode.OK
    headers: HeaderMap = dataclasses.field(init=False)

    def __post_init__(self):
        self.headers = HeaderMap()

    def __getitem__(self, key: str) -> str:
        if not isinstance(key, str):
            raise KeyError
        return self.headers[key]

    def __setitem__(self, key: str, value: str):
        if not isinstance(key, str):
            raise KeyError
        self.headers[key] = value

    def send(self, socket: socket.socket) -> str:
        socket.send(b"%b %d %b\r\n" % (
            self.version, self.status_code.value, self.status_code.to_bytes()))

    def is_success(self) -> bool:
        return self.status_code.is_success()

    def is_failure(self) -> bool:
        return self.status_code.is_failure()
