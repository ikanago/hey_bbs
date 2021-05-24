from libbbs.misc import StatusCode
from libbbs.middleware import Middleware, Next
from libbbs.request import Request
from libbbs.response import Response


VALUE = "value"


class MiddlewareA(Middleware):
    def call(self, req: Request, next: Next) -> Response:
        req.set("A", VALUE)
        res = next.run(req)
        res.set("A", VALUE)
        return res


class MiddlewareB(Middleware):
    def call(self, req: Request, next: Next) -> Response:
        req.set("B", VALUE)
        res = next.run(req)
        res.set("B", VALUE)
        return res


def handler(req: Request) -> Response:
    # Request has passed through `MiddlewareA` and `MiddlewareB`, so header "A"
    # and "B" must be set.
    assert VALUE == req.get("A")
    assert VALUE == req.get("B")
    return Response(status_code=StatusCode.OK)


def test_middleware():
    next = Next(handler, [MiddlewareA(), MiddlewareB()])
    res = next.run(Request())
    assert VALUE == res.get("A")
    assert VALUE == res.get("B")
    assert 200 == res.status_code.value
