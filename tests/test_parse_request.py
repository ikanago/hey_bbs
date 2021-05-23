from libbbs.body import Body
from urllib import parse
from libbbs.parse_request import RequestParser
from libbbs.request import Request


def test_get_request():
    parser = RequestParser()
    assert parser.try_parse(b"GET /index.html HTTP/1.1\r\n\r\n")
    assert Request(uri="/index.html") == parser.complete()


def test_url_encoded():
    parser = RequestParser()
    assert parser.try_parse(b"GET /index.html?key=%E8%9B%87 HTTP/1.1\r\n\r\n")
    assert Request(uri="/index.html?key=蛇") == parser.complete()


def test_headers():
    expected = Request(uri="/index.html")
    expected["host"] = "localhost"
    expected["accept"] = "*/*"
    parser = RequestParser()
    assert parser.try_parse(
        b"GET /index.html HTTP/1.1\r\nHost: localhost\r\nAccept: */*\r\n\r\n")
    assert expected == parser.complete()


def test_headers_separated_input():
    expected = Request(uri="/index.html")
    expected["host"] = "localhost"
    expected["accept"] = "*/*"
    parser = RequestParser()
    parser.try_parse(b"GET /index.html H")
    parser.try_parse(b"TTP/1.1\r\nHost: loc")
    parser.try_parse(b"alhost\r\nAccept: */")
    assert parser.try_parse(b"*\r\n\r\n")
    assert expected == parser.complete()


def test_header_is_case_insensitive():
    expected = Request(uri="/index.html")
    expected["accept"] = "*/*"
    parser = RequestParser()
    assert parser.try_parse(
        b"GET /index.html HTTP/1.1\r\nAccEpT: */*\r\n\r\n")
    assert expected == parser.complete()


def test_body_separated_input():
    expected = Request(uri="/index.html")
    expected["content-length"] = "13"
    expected.body = b"Hello, World!"
    parser = RequestParser()
    assert parser.try_parse(
        b"GET /index.html HTTP/1.1\r\nContent-Length: 13\r\n\r\nHello, World!")
    assert expected == parser.complete()


def test_body_separated_input():
    expected = Request(uri="/index.html")
    expected["content-length"] = "13"
    expected.body = Body(b"Hello, World!")
    parser = RequestParser()
    parser.try_parse(b"GET /index.html HT")
    parser.try_parse(b"TP/1.1\r\nContent-Le")
    parser.try_parse(b"ngth: 13\r\n\r\nHello")
    assert parser.try_parse(b", World!")
    assert expected == parser.complete()
