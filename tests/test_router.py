from libbbs.misc import Method, StatusCode
from libbbs.request import Request
from libbbs.response import Response
from libbbs.router import Router


def ok(_: Request) -> Response:
    return Response(status_code=StatusCode.OK)


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
