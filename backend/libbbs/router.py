from __future__ import annotations
from libbbs.handler import Handler
from libbbs.request import Request
from libbbs.response import Response
from libbbs.misc import Method, StatusCode
import dataclasses


@dataclasses.dataclass
class Router:
    __exact_map: dict[tuple[str, Method],
                      Handler] = dataclasses.field(init=False)
    __wildcard_map: dict[tuple[str, Method],
                         Handler] = dataclasses.field(init=False)

    def __post_init__(self):
        self.__exact_map = {}
        self.__wildcard_map = {}

    def route(self, uri: str, method: Method, handler: Handler) -> None:
        assert uri.startswith("/")
        if uri.endswith("*"):
            uri = uri.strip("*")
            self.__wildcard_map[(uri, method)] = handler
        else:
            self.__exact_map[(uri, method)] = handler

    def dispatch(self, uri: str, method: Method) -> Handler:
        handler = self.__exact_map.get((uri, method))
        if handler is not None:
            return handler

        candidate_handler = None
        candidate_path = ""
        for ((wildcard_path, wildcard_method), wildcard_handler) in self.__wildcard_map.items():
            if uri.startswith(wildcard_path) and method == wildcard_method and candidate_path < wildcard_path:
                candidate_handler = wildcard_handler
                candidate_path = wildcard_path

        if candidate_handler is None:
            return not_found_handler
        return candidate_handler


def not_found_handler(_: Request) -> Response:
    return Response(status_code=StatusCode.NOT_FOUND)
