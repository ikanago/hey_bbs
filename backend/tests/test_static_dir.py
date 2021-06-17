import pytest
from libbbs.body import Body
from libbbs.misc import Method, StatusCode
from libbbs.request import Request
from libbbs.response import Response
from libbbs.server import Server


@pytest.fixture
def server() -> Server:
    server = Server()
    server.serve_directory("/test", "tests/static")
    return server


def test_get_static_file1(server: Server):
    req = Request(uri="/test/index.html")
    res = server.respond(req)
    assert res.is_success()
    assert "<p>Hello</p>" == str(res.body)


def test_get_static_file2(server: Server):
    req = Request(uri="/test/index.js")
    res = server.respond(req)
    assert res.is_success()
    assert "console.log('Hello');" == str(res.body)
