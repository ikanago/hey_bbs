from abc import ABC, abstractmethod
from typing import Callable, Union
from libbbs.request import Request
from libbbs.response import Response


class HandlerMixin(ABC):
    @abstractmethod
    def call(self, req: Request) -> Response:
        pass


Handler = Union[Callable[[Request], Response], HandlerMixin]
