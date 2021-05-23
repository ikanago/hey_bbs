from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Generic, List, TypeVar, Protocol
from enum import Enum, auto


class Comparison(Enum):
    r""" This class is used to specify search condition in `Db`.
    """
    EQ = auto()
    NE = auto()
    LT = auto()
    GT = auto()
    LE = auto()
    GE = auto()


C = TypeVar("C", bound="Comparable")


class Comparable(Protocol):
    r""" Protocol class to indicate total order.

    This class is used for lower bound of type variable.
    Without this class, mypy cannot infer a type variable can be compared to
    other object.
    """

    @abstractmethod
    def __eq__(self, other: Any) -> bool:
        pass

    def __ne__(self, other: Any) -> bool:
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
    r""" Abstract class which is stored to `Db`.

    This class provides an interface to specific instance variable to use in
    `Db.query()`.
    """

    @abstractmethod
    def get(self) -> VT:
        r""" Interface to access instance variable. A class implementing this
        abstract class is queried by the variable.

        Returns
        -------
        VT
            Instance variable.

        Example
        -------
        In the following example, `Model` class is queried by its `name` in a
        `Db`.

        ```
        @dataclass
        class Model(QueryableBy[int]):
        name: int

        def get(self) -> int:
            return self.name
        ```
        """
        ...


T = TypeVar("T", bound=Comparable)


@dataclass
class Db(Generic[T]):
    r""" Simple database class.

    This just holds data in a list. Not performant and useful.
    """

    __inner: List[QueryableBy[T]]

    def query(self, target: T, comp: Comparison = Comparison.EQ) -> List[QueryableBy[T]]:
        r""" Find data matching a condition.

        Parameters
        ----------
        target: T
            Right hand side of comparison.
        comp: Comparison
            Specify comparison operator to match data.

        Returns
        -------
        List[Queryable[T]]
            List of data matching a condition.
        """
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
