from dataclasses import dataclass
from libbbs.misc import StatusCode
from libbbs.response import Response
from libbbs.middleware import Middleware, Next
from libbbs.request import Request


@dataclass
class Cors(Middleware):
    allow_origin: str = "*"
    allow_methods: str = "POST, GET, OPTIONS"
    allow_headers: str = "*"
    max_age: str = "86400"

    def is_valid_origin(self, origin: str) -> bool:
        if self.allow_origin == "*":
            return True
        else:
            return self.allow_origin == origin

    def call(self, req: Request, next: Next) -> Response:
        origin = req.get("Origin")
        if origin is None:
            return next.run(req)

        if not self.is_valid_origin(origin):
            return Response(status_code=StatusCode.UNAUTHORIZED)

        res = next.run(req)
        res.set("Access-Control-Allow-Origin", self.allow_origin)
        # print(res.get("Access-Control-Allow-Origin"))
        return res
