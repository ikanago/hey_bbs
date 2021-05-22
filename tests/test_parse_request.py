import pytest

from libbbs.parse_request import parse_request
from libbbs.request import Request


def test_get_request():
    req = parse_request(b"GET /index.html HTTP/1.1\r\n\r\n")
    assert Request(uri="/index.html") == req


def test_url_encoded():
    req = parse_request(b"GET /index.html?key=%E8%9B%87 HTTP/1.1\r\n\r\n")
    assert Request(uri="/index.html?key=蛇") == req


def test_headers():
    actual = parse_request(
        b"GET /index.html HTTP/1.1\r\nHost: localhost\r\nAccept: */*\r\n")
    expected = Request(uri="/index.html")
    expected["host"] = "localhost"
    expected["accept"] = "*/*"
    assert expected == actual


def test_header_is_case_insensitive():
    actual = parse_request(
        b"GET /index.html HTTP/1.1\r\nAccEpt: */*\r\n")
    expected = Request(uri="/index.html")
    expected["accept"] = "*/*"
    assert expected == actual
