from __future__ import annotations
from libbbs.misc import Method


class Request:
    def __init__(self, m: Method = None, uri: str = None, version: str = None) -> None:
        self.__method = m if m is not None else Method.GET
        self.__uri = uri if uri is not None else ""
        self.__version = version if version is not None else "HTTP/1.1"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Request):
            raise NotImplemented
        return self.__method == other.__method and self.__uri == other.__uri

    @property
    def method(self) -> Method:
        return self.__method

    @property
    def uri(self) -> str:
        return self.__uri

    @property
    def version(self) -> str:
        return self.__version
