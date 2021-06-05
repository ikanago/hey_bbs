import pytest
from json import loads
from libbbs.body import Body
from libbbs.login import LoginMiddleware
from libbbs.middleware import Middleware, Next
from libbbs.misc import Method, StatusCode
from libbbs.request import Request
from libbbs.response import Response, see_other
from libbbs.server import Server
from libbbs.session_middleware import SessionMiddleware


SESSION_ID = "SID"
CREDENTIAL = "credential"


@pytest.fixture
def login_server() -> Server:
    server = Server()
    server.use(SessionMiddleware(SESSION_ID))
    server.use(LoginMiddleware(["/login"], "/", CREDENTIAL))
    server.route("/hello", Method.GET, hello)
    server.route("/login", Method.POST, login)
    return server


def login(req: Request) -> Response:
    body = req.body
    if body is None:
        return Response(status_code=StatusCode.UNAUTHORIZED)
    body = loads(str(body))
    username = body["username"]
    password = body["password"]

    if req.session is None:
        return Response(status_code=StatusCode.INTERNAL_SERVER_ERROR)
    req.session.set(CREDENTIAL, f"{username};{password}")
    return see_other("/hello")


def hello(_req: Request) -> Response:
    res = Response()
    res.body = Body(b"hello")
    return res


def test_login(login_server: Server):
    req = Request(Method.POST, "/login")
    req.body = Body(
        bytes(r"""{"username": "John", "password": "qwerty"}""", "utf-8"))
    res = login_server.respond(req)
    assert StatusCode.SeeOther == res.status_code

    session_id = res.extract_session_id(SESSION_ID)
    if session_id is None:
        assert False

    req = Request(uri="/hello")
    req.set("Cookie", f"{SESSION_ID}={session_id}")
    res = login_server.respond(req)
    assert StatusCode.OK == res.status_code
    assert "hello" == str(res.body)


def test_fail_login(login_server: Server):
    req = Request(Method.POST, "/login")
    req.body = Body(
        bytes(r"""{"username": "John", "password": "qwerty"}""", "utf-8"))
    res = login_server.respond(req)
    assert StatusCode.SeeOther == res.status_code

    # "/hello" needs login session. So a request without session fails.
    req = Request(uri="/hello")
    res = login_server.respond(req)
    assert StatusCode.UNAUTHORIZED == res.status_code
