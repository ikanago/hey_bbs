from __future__ import annotations
from libbbs.misc import BadRequest, Method
from libbbs.request import Request
from urllib.parse import unquote


def parse_request(request_message: bytes) -> Request:
    """
    Parse request line and headers.
    """
    lines = request_message.split(b"\r\n")
    method, uri, version = _parse_request_line(lines[0])
    req = Request(method, uri, version)

    headers = lines[1:]
    for header in headers:
        if len(header) == 0:
            # Empty line indicating the end of headers.
            break
        key, value = _parse_header(header)
        req[key] = value
    return req


def _parse_request_line(request_line: bytes) -> tuple[Method, str, str]:
    method, uri, version = request_line.split(b" ")
    if version != b"HTTP/1.0" and version != b"HTTP/1.1":
        raise BadRequest
    return Method.from_bytes(method), unquote(uri.decode()), version.decode()


def _parse_header(header_line: bytes) -> tuple[str, str]:
    key, value = header_line.split(b": ")
    return key.decode(), value.decode()
