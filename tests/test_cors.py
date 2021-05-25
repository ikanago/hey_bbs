from libbbs.body import Body
from libbbs.response import Response
from libbbs.request import Request
from libbbs.misc import Method, StatusCode
from libbbs.server import Server
import pytest
from libbbs.cors import Cors


def hello(_: Request) -> Response:
    res = Response()
    res.set_body(Body(b"Hello"))
    return res


@pytest.fixture
def server_any_origin() -> Server:
    server = Server()
    server.route("/", Method.GET, hello)
    server.use(Cors())
    return server


ALLOW_ORIGIN: str = "localhost:3000"


@pytest.fixture
def server_specific_origin() -> Server:
    server = Server()
    server.route("/", Method.GET, hello)
    server.use(Cors(allow_origin=ALLOW_ORIGIN))
    return server


@pytest.fixture
def get_with_origin() -> Request:
    req = Request()
    req.set("Origin", ALLOW_ORIGIN)
    return req


def test_simple_req_any_origin(server_any_origin: Server, get_with_origin: Request):
    res = server_any_origin.respond(get_with_origin)
    assert res.is_success()
    assert "*" == res.get("Access-Control-Allow-Origin")


def test_simple_req_specific_origin(server_specific_origin: Server, get_with_origin: Request):
    res = server_specific_origin.respond(get_with_origin)
    assert res.is_success()
    assert ALLOW_ORIGIN == res.get("Access-Control-Allow-Origin")


def test_without_origin_header(server_specific_origin: Server):
    res = server_specific_origin.respond(Request())
    assert res.is_success()
    assert None is res.get("Access-Control-Allow-Origin")
