import pytest

from libbbs.parse_request import parse_request
from libbbs.request import Request


@pytest.fixture()
def new_request() -> Request:
    return parse_request()


def test_get_request(new_request):
    assert 42 == new_request.get_x()
