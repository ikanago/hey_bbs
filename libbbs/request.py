from __future__ import annotations
from libbbs.header_map import HeaderMap
from libbbs.misc import Method
import dataclasses


@dataclasses.dataclass
class Request:
    method: Method = Method.GET
    uri: str = "/"
    version: bytes = b"HTTP/1.1"
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
