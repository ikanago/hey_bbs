from __future__ import annotations
from dataclasses import dataclass
from libbbs.misc import BadRequest
from typing import Type, TypeVar
from dataclasses_json import DataClassJsonMixin


@dataclass
class Body:
    __inner: str = ""

    def __init__(self, inner: bytes) -> None:
        self.__inner = inner.decode()

    def __len__(self) -> int:
        return len(self.__inner)

    def __str__(self) -> str:
        return self.__inner

    @staticmethod
    def from_str(inner: str) -> Body:
        body = Body(b"")
        body.__inner = inner
        return body

    T = TypeVar("T", bound=DataClassJsonMixin)

    def from_json(self, model: Type[T]) -> T:
        r"""Parse `Body` as JSON and return corresponding type.

        Parameter
        ---------
        model: Type[DataClassJsonMixin]
            Class name which is subclass of DataClassJsonMixin.

        Returns
        -------
        DataClassJsonMixin
            Instance parsed from JSON, which is subclass of DataClassJsonMixin.

        Raises
        ------
        BadRequest
            * If the JSON string contains some keys which are not
            one of the attributes of `model` class.
            * If `model` is not subclass of DataClassJsonMixin.
        """
        if issubclass(model, DataClassJsonMixin):
            try:
                return model.from_json(self.__inner)
            except KeyError:
                raise BadRequest
        raise BadRequest

    @staticmethod
    def to_json(data: DataClassJsonMixin) -> Body:
        r"""Encode `data` to a JSON string.

        Parameter
        ---------
        data: DataClassJsonMixin
            Instance to encode to JSON, which is subclass of DataClassJsonMixin.

        Returns
        -------
        Body
            Body whose data is a encoded JSON string.

        Raises
        ------
        BadRequest
            If `model` is not subclass of DataClassJsonMixin.
        """
        if isinstance(data, DataClassJsonMixin):
            return Body.from_str(data.to_json())
        raise BadRequest

    def to_bytes(self) -> bytes:
        return self.__inner.encode("utf-8")
