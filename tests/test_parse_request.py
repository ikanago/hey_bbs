import pytest

from libbbs.parse_request import parse_request
from libbbs.request import Request


def test_get_request():
    req = parse_request(b"GET /index.html HTTP/1.1\r\n")
    assert Request(uri="/index.html") == req


def test_url_encoded():
    req = parse_request(b"GET /index.html?key=%E8%9B%87 HTTP/1.1\r\n")
    assert Request(uri="/index.html?key=蛇") == req
