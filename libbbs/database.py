from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Generic, List, TypeVar, Protocol
from enum import Enum, auto


class Comparison(Enum):
    EQ = auto()
    NE = auto()
    LT = auto()
    GT = auto()
    LE = auto()
    GE = auto()


C = TypeVar("C", bound="Comparable")


class Comparable(Protocol):
    @abstractmethod
    def __eq__(self, other: Any) -> bool:
        pass

    def __ne__(self, other: C) -> bool:
        return not self == other

    @abstractmethod
    def __lt__(self: C, other: C) -> bool:
        pass

    def __gt__(self: C, other: C) -> bool:
        return (not self < other) and self != other

    def __le__(self: C, other: C) -> bool:
        return self < other or self == other

    def __ge__(self: C, other: C) -> bool:
        return (not self < other)


VT = TypeVar("VT", bound=Comparable)


class QueryableBy(ABC, Generic[VT]):
    @abstractmethod
    def get(self) -> VT: ...


T = TypeVar("T", bound=Comparable)


@dataclass
class Db(Generic[T]):
    __inner: List[QueryableBy[T]]

    def query(self, target: T, comp: Comparison = Comparison.EQ) -> List[QueryableBy[T]]:
        if comp == Comparison.EQ:
            return [x for x in self.__inner if x.get() == target]
        elif comp == Comparison.NE:
            return [x for x in self.__inner if x.get() != target]
        elif comp == Comparison.LT:
            return [x for x in self.__inner if x.get() < target]
        elif comp == Comparison.GT:
            return [x for x in self.__inner if x.get() > target]
        elif comp == Comparison.LE:
            return [x for x in self.__inner if x.get() <= target]
        elif comp == Comparison.GE:
            return [x for x in self.__inner if x.get() >= target]
        else:
            return []

    def delete(self, target: T):
        inner = []
        for data in self.__inner:
            if data.get() != target:
                inner.append(data)
        self.__inner = inner


@dataclass
class Model(QueryableBy[int]):
    name: int

    def get(self) -> int:
        return self.name
