from __future__ import annotations
from libbbs.misc import BadRequest, Method
from libbbs.request import Request
from urllib.parse import unquote
from typing import Literal, Optional
import dataclasses


@dataclasses.dataclass
class RequestParser:
    """`RequestParser` is a state machine which can accept valid HTTP message.

    Give lines read from TCP socket to `RequestParser.try_parse()`.
    It returns `Request` if whole lines of HTTP request is parsed.
    """
    __buffer: bytes = dataclasses.field(default=b"", init=False)
    __request: Request = dataclasses.field(init=False)
    __state: Literal["headers", "body"] = dataclasses.field(
        default="headers", init=False)

    def complete(self) -> Request:
        return self.__request

    def try_parse(self, line: bytes) -> bool:
        """Try to parse request message with incoming `line`.

        Returns
        -------
        is_parse_complete: bool
            Whether parse is completed.
        """
        self.__buffer += line
        # Roop here because request message can contains headers and body
        # if the message is small enough.
        while True:
            if self.__state == "headers":
                # Parsing request line and headers is not completed.
                is_header_complete = self._try_parse_until_headers()
                if not is_header_complete:
                    return False
                if self.__request.content_length() is None:
                    # No need to parse request body, so tell that parsing is finished.
                    return True
                self.__state = "body"
            elif self.__state == "body":
                is_body_complete = self._try_parse_body()
                if not is_body_complete:
                    return False
                break
        return True

    def _try_parse_until_headers(self) -> Optional[Request]:
        """Try to parse request message in the buffer until whole headers complete.

        Returns
        -------
        is_header_complete: bool
            Whether request line and headers are all parsed.
        """
        end_of_header = self.__buffer.find(b"\r\n\r\n")
        if end_of_header == -1:
            # Not enough to parse request line and headers.
            return False

        request_message = self.__buffer[:end_of_header]
        # Skip CRLF to parse request body
        self.__buffer = self.__buffer[(end_of_header + 4):]
        self.__request = self._parse_request(request_message)
        return True

    def _try_parse_body(self) -> Optional[Request]:
        """Try to parse request message in the buffer until whole headers complete.

        Returns
        -------
        is_body_complete: bool
            Whether request body is all parsed.
        """
        content_length = self.__request.content_length()
        if content_length is None:
            return False
        if len(self.__buffer) < content_length:
            # Not enough to parse request body
            return False
        self.__request.body = self.__buffer[:content_length]
        return True

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
        return req


def _parse_request_line(request_line: bytes) -> tuple[Method, str, str]:
    method, uri, version = request_line.split(b" ")
    if version != b"HTTP/1.0" and version != b"HTTP/1.1":
        raise BadRequest
    return Method.from_bytes(method), unquote(uri.decode()), version


def _parse_header(header_line: bytes) -> tuple[str, str]:
    key, value = header_line.split(b": ")
    return key.decode(), value.decode()
