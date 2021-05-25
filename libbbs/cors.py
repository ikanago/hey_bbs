from dataclasses import dataclass
from libbbs.misc import Method, StatusCode
from libbbs.response import Response
from libbbs.middleware import Middleware, Next
from libbbs.request import Request


@dataclass
class Cors(Middleware):
    r""" This middleware handles a CORS request.
    """

    allow_origin: str = "*"
    allow_methods: str = "POST, GET, OPTIONS"
    allow_headers: str = "*"
    max_age: str = "86400"

    def _is_valid_origin(self, origin: str) -> bool:
        if self.allow_origin == "*":
            return True
        else:
            return self.allow_origin == origin

    def _handle_preflight(self) -> Response:
        res = Response()
        res.set("Access-Control-Allow-Origin", self.allow_origin)
        res.set("Access-Control-Allow-Methods", self.allow_methods)
        res.set("Access-Control-Allow-Headers", self.allow_headers)
        res.set("Access-Control-Allow-Max-Age", self.max_age)
        return res

    def call(self, req: Request, next: Next) -> Response:
        origin = req.get("Origin")
        if origin is None:
            return next.run(req)

        if not self._is_valid_origin(origin):
            return Response(status_code=StatusCode.UNAUTHORIZED)

        if req.method == Method.OPTIONS:
            return self._handle_preflight()

        res = next.run(req)
        res.set("Access-Control-Allow-Origin", self.allow_origin)
        return res
