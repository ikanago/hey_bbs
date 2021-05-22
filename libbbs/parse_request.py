from __future__ import annotations
from libbbs.misc import BadRequest, Method
from libbbs.request import Request
from urllib.parse import unquote


def parse_request(request_message: bytes):
    lines = request_message.split(b"\r\n")
    try:
        method, uri, version = _parse_request_line(lines[0])
    except:
        raise
    print(uri)
    req = Request(method, uri, version)
    return req


def _parse_request_line(request_line: bytes) -> tuple[Method, str, str]:
    method, uri, version = request_line.split(b" ")
    version.strip(b"\r\n")
    if version != b"HTTP/1.0" and version != b"HTTP/1.1":
        raise BadRequest
    return Method.from_bytes(method), unquote(uri.decode()), version.decode()
