from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional
from libbbs.body import Body
from libbbs.header_map import CaseInsensitiveMap
from libbbs.misc import Method
from libbbs.session import Session, extract_session_id_inner


@dataclass
class Request:
    method: Method = Method.GET
    uri: str = "/"
    version: bytes = b"HTTP/1.1"
    __headers: CaseInsensitiveMap = field(init=False)
    body: Optional[Body] = field(default=None)
    session: Optional[Session] = field(default=None, init=False)

    def __post_init__(self):
        self.__headers = CaseInsensitiveMap()

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
        return self.__headers.get(key)

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
        self.__headers.set(key, value)

    def content_length(self) -> Optional[int]:
        try:
            value = self.get("content-length")
            if value is None:
                return None
            else:
                return int(value)
        except (KeyError, ValueError):
            return None

    def extract_session_id(self, session_id: str) -> Optional[str]:
        return extract_session_id_inner(self.get("Cookie"), session_id)
