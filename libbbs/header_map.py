from __future__ import annotations
import dataclasses
from typing import Iterator, Optional


@dataclasses.dataclass
class HeaderMap:
    __headers: dict[str, str] = dataclasses.field(init=False)

    def __post_init__(self):
        self.__headers = {}

    def get(self, key: str) -> Optional[str]:
        if not isinstance(key, str):
            raise KeyError
        return self.__headers.get(key.lower())

    def set(self, key: str, value: str):
        if not isinstance(key, str):
            raise KeyError
        self.__headers[key.lower()] = value

    def __len__(self):
        return len(self.__headers)

    def __iter__(self) -> Iterator[tuple[str, str]]:
        return iter([(key, value) for key, value in self.__headers.items()])
