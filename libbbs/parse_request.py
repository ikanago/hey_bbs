from __future__ import annotations
from libbbs.misc import BadRequest, Method
from libbbs.request import Request
from urllib.parse import unquote
from typing import Optional
import dataclasses


@dataclasses.dataclass
class RequestParser:
    """`RequestParser` is a state machine which can accept valid HTTP message.

    Give lines read from TCP socket to `RequestParser.try_parse()`.
    It returns `Request` if whole lines of HTTP request is parsed.
    """
    buffer: bytes = dataclasses.field(default=b"", init=False)
    request: Request = dataclasses.field(init=False)
    is_parsing_header: bool = dataclasses.field(default=True, init=False)

    def try_parse(self, line: bytes) -> Optional[Request]:
        self.buffer += line
        if self.is_parsing_header:
            # Parsing request line and headers is not completed.
            end_of_header = self.buffer.find(b"\r\n\r\n")
            if end_of_header == -1:
                # Not enough to parse request line and headers.
                return None
            else:
                request_message = self.buffer[:end_of_header]
                # Skip CRLF to parse request body
                self.buffer = self.buffer[(end_of_header + 4):]
                self._parse_request(request_message)
                self.is_parsing_header = False
        return self.request

    def _parse_request(self, request_message: bytes) -> Request:
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
        # Parse request body
        # if req.content_length() > 0:
        #     while True:
        #         message = client_sock.recv(Server.BUFSIZE)
        #         buffer += message
        #         if len(buffer) == req.content_length():
        #             break
        self.request = req


def _parse_request_line(request_line: bytes) -> tuple[Method, str, str]:
    method, uri, version = request_line.split(b" ")
    if version != b"HTTP/1.0" and version != b"HTTP/1.1":
        raise BadRequest
    return Method.from_bytes(method), unquote(uri.decode()), version


def _parse_header(header_line: bytes) -> tuple[str, str]:
    key, value = header_line.split(b": ")
    return key.decode(), value.decode()
