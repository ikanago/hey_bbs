import dataclasses


@dataclasses.dataclass
class Body:
    __inner: str = ""

    def __init__(self, inner: bytes) -> None:
        self.__inner = inner.decode()

    def __len__(self) -> int:
        return len(self.__inner)

    def to_bytes(self) -> bytes:
        return self.__inner.encode("utf-8")
