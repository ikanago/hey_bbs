import pytest
from libbbs.misc import Method
from libbbs.request import Request
from libbbs.response import Response
from libbbs.router import Router


def ok(_: Request) -> Response:
    return Response()


def test_router():
    router = Router()
    routes = [("/hello", Method.GET), ("/", Method.POST)]
    for route in routes:
        router.route(*route, ok)

    for route in routes:
        res = router.dispatch(*route)(Request())
        assert res.is_success()


def test_absent_route():
    router = Router()
    res = router.dispatch("/", Method.GET)(Request())
    assert res.is_failure()


@pytest.fixture
def wildcard_router() -> Router:
    router = Router()
    routes = [("/*", Method.GET), ("/", Method.GET),
              ("/api/posts", Method.GET), ("/api/posts", Method.POST)]
    for route in routes:
        router.route(*route, ok)
    return router


def test_match_wildcard(wildcard_router: Router):
    assert wildcard_router.dispatch(
        "/index.html", Method.GET)(Request()).is_success()
    assert wildcard_router.dispatch(
        "/index.css", Method.GET)(Request()).is_success()


def test_concrete_path_does_not_match_wildcard(wildcard_router: Router):
    assert wildcard_router.dispatch(
        "/api/posts", Method.GET)(Request()).is_success()
    assert wildcard_router.dispatch(
        "/api/posts", Method.POST)(Request()).is_success()
    assert wildcard_router.dispatch(
        "/", Method.GET)(Request()).is_success()


def test_not_match_wildcard(wildcard_router: Router):
    assert wildcard_router.dispatch(
        "/index.html", Method.POST)(Request()).is_failure()
