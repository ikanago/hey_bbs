from __future__ import annotations
from typing import Optional
from libbbs.body import Body
from libbbs.header_map import HeaderMap
from libbbs.misc import Method
import dataclasses


@dataclasses.dataclass
class Request:
    method: Method = Method.GET
    uri: str = "/"
    version: bytes = b"HTTP/1.1"
    headers: HeaderMap = dataclasses.field(init=False)
    body: Optional[Body] = dataclasses.field(default=None)

    def __post_init__(self):
        self.headers = HeaderMap()

    def get(self, key: str) -> Optional[str]:
        if not isinstance(key, str):
            raise KeyError
        return self.headers.get(key)

    def set(self, key: str, value: str):
        if not isinstance(key, str):
            raise KeyError
        self.headers.set(key, value)

    def content_length(self) -> Optional[int]:
        try:
            value = self.get("content-length")
            if value is None:
                return None
            else:
                return int(value)
        except (KeyError, ValueError):
            return None