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
def server() -> Server:
    server = Server()
    server.route("/", Method.GET, hello)
    return server


ALLOW_ORIGIN: str = "localhost:3000"


def test_simple_req_any_origin(server: Server):
    req = Request()
    req.set("Origin", ALLOW_ORIGIN)
    server.use(Cors())
    res = server.responde(req)
    assert StatusCode.OK == res.status_code
    assert "*" == res.get("Access-Control-Allow-Origin")
