from libbbs.misc import StatusCode
from libbbs.middleware import Middleware, Next
from libbbs.request import Request
from libbbs.response import Response


VALUE = "value"


class MiddlewareA(Middleware):
    def call(self, req: Request, next: Next) -> Response:
        req["A"] = VALUE
        res = next.run(req)
        res["A"] = VALUE
        return res


class MiddlewareB(Middleware):
    def call(self, req: Request, next: Next) -> Response:
        req["B"] = VALUE
        res = next.run(req)
        res["B"] = VALUE
        return res


def handler(req: Request) -> Response:
    # Request has passed through `MiddlewareA` and `MiddlewareB`, so header "A"
    # and "B" must be set.
    assert VALUE == req["A"]
    assert VALUE == req["B"]
    return Response(status_code=StatusCode.OK)


def test_middleware():
    next = Next(handler, [MiddlewareA(), MiddlewareB()])
    res = next.run(Request())
    assert VALUE == res["A"]
    assert VALUE == res["B"]
    assert 200 == res.status_code.value
