from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass
from libbbs.response import Response
from typing import List
from libbbs.request import Request
from libbbs.router import Handler


class Middleware(ABC):
    r""" Middleware performs some processes to a requests before a handler and
    a response after a handler.
    """

    @abstractmethod
    def call(self, req: Request, next: Next) -> Response:
        r""" Mutate request before handler and response after handler.

        Parameters
        ----------
        req: Request
            Incoming request.
        next: Next
            Middlewares to be called next.

        Returns
        -------
        Response
            Outgoing response.
        """
        ...


@dataclass
class Next:
    __handler: Handler
    __middlewares: List[Middleware]

    def run(self, req: Request) -> Response:
        if len(self.__middlewares) > 0:
            first, remaining = self.__middlewares[0], self.__middlewares[1:]
            self.__middlewares = remaining
            return first.call(req, self)
        else:
            # mypy might not be able to distinguish calling function of class
            # member and method.
            return self.__handler(req)  # type: ignore
