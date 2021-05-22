from __future__ import annotations
from libbbs.misc import Method
import dataclasses


@dataclasses.dataclass
class Request:
    method: Method = Method.GET
    uri: str = "/"
    version: str = "HTTP/1.1"
    headers: dict[str, str] = dataclasses.field(init=False)

    def __post_init__(self):
        self.headers = {}

    def __getitem__(self, key: str) -> str:
        if not isinstance(key, str):
            raise KeyError
        return self.headers[key.lower()]

    def __setitem__(self, key: str, value: str):
        if not isinstance(key, str):
            raise KeyError
        self.headers[key.lower()] = value

    def __len__(self):
        return len(self.headers)

    # def __iter__(self):
    #     return [key for key, _ in self.headers]
