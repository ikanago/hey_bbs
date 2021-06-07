import pytest
from libbbs.body import Body
from libbbs.misc import Method, StatusCode
from libbbs.request import Request
from libbbs.response import Response
from libbbs.server import Server


server = Server()


@server.route("/")
def ok(_req: Request) -> Response:
    return Response()


@server.route("/", Method.POST)
def post(req: Request) -> Response:
    body = req.body
    if body is None:
        return Response(status_code=StatusCode.BAD_REQUEST)
    return Response(body=body)


def test_ok():
    res = server.respond(Request())
    assert res.is_success()


def test_post():
    req = Request(method=Method.POST, body=Body.from_str("Hello"))
    res = server.respond(req)
    assert res.is_success()
    assert "Hello" == str(res.body)
