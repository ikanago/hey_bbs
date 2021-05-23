from __future__ import annotations
import dataclasses
from libbbs.misc import BadRequest, InternalServerError
from typing import Type
from dataclasses_json import DataClassJsonMixin


@dataclasses.dataclass
class Body:
    __inner: str = ""

    def __init__(self, inner: bytes) -> None:
        self.__inner = inner.decode()

    def __len__(self) -> int:
        return len(self.__inner)

    @staticmethod
    def from_str(inner: str) -> Body:
        body = Body(b"")
        body.__inner = inner
        return body

    def from_json(self, model: Type[DataClassJsonMixin]) -> DataClassJsonMixin:
        if issubclass(model, DataClassJsonMixin):
            try:
                return model.from_json(self.__inner)
            except KeyError:
                raise BadRequest
        raise BadRequest

    @staticmethod
    def to_json(data: DataClassJsonMixin) -> Body:
        if not isinstance(data, DataClassJsonMixin):
            return Body.from_str(data.to_json())
        raise BadRequest

    def to_bytes(self) -> bytes:
        return self.__inner.encode("utf-8")
