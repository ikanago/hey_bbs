import pytest
from libbbs.middleware import Middleware, Next
from libbbs.misc import Method, StatusCode
from libbbs.request import Request
from libbbs.response import Response
from libbbs.server import Server
from libbbs.session_middleware import SessionMiddleware


SESSION_ID = "SID"
VISITS = "visits"
CREDENTIAL = "credential"


class Visits(Middleware):
    def call(self, req: Request, next: Next) -> Response:
        visits = req.session.get(VISITS)
        if visits is None:
            visits = "0"
        req.session.set(VISITS, str(int(visits) + 1))
        return next.run(req)


def visit(req: Request) -> Response:
    visits = req.session.get(VISITS)
    if visits is None:
        return Response()
    res = Response()
    res.body = visits
    return res


@pytest.fixture
def session_server() -> Server:
    server = Server()
    server.use(SessionMiddleware(SESSION_ID))
    server.use(Visits())
    server.add_route("/", Method.GET, visit)
    return server


def test_new_client(session_server: Server):
    req = Request()
    res = session_server.respond(req)
    assert "1" == str(res.body)


def test_revisit_client(session_server: Server):
    req = Request()
    res = session_server.respond(req)
    assert StatusCode.OK == res.status_code
    assert "1" == str(res.body)

    session_id = res.extract_session_id(SESSION_ID)
    if session_id is None:
        assert False

    req = Request()
    req.set("Cookie", f"{SESSION_ID}={session_id}")
    res = session_server.respond(req)
    assert StatusCode.OK == res.status_code
    assert "2" == str(res.body)
