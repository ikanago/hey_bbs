from __future__ import annotations
from libbbs.request import Request
from libbbs.response import Response
from libbbs.misc import Method, StatusCode
from typing import Callable
import dataclasses


Handler = Callable[[Request], Response]


@dataclasses.dataclass
class Router:
    routing: dict[tuple[str, Method], Handler] = dataclasses.field(init=False)

    def __post_init__(self):
        self.routing = {}

    def route(self, uri: str, method: Method, handler: Handler) -> None:
        self.routing[(uri, method)] = handler

    def dispatch(self, uri: str, method: Method) -> Handler:
        try:
            return self.routing[(uri, method)]
        except Exception:
            return not_found_handler


def not_found_handler(_: Request) -> Response:
    return Response(status_code=StatusCode.NOT_FOUND)
