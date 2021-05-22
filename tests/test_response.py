from libbbs.misc import StatusCode
from libbbs.response import Response


def test_response_from_status_code():
    assert Response(status_code=StatusCode.NOT_FOUND) == Response.from_status_code(
        StatusCode.NOT_FOUND)
