from typing import List
from libbbs.router import Handler, Router
from libbbs.misc import BadRequest, InternalServerError, Method, StatusCode
from libbbs.middleware import Middleware, Next
from libbbs.parse_request import RequestParser
from libbbs.response import Response
import socket
import threading


class Server:
    BUFSIZE = 4096

    def __init__(self, port: int) -> None:
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
        self.router = Router()
        self.middlewares: List[Middleware] = []

    def use(self, middleware: Middleware):
        self.middlewares.append(middleware)

    def route(self, uri: str, method: Method, handler: Handler):
        self.router.route(uri, method, handler)

    def run(self) -> None:
        self.sock.bind(("0.0.0.0", self.port))
        self.sock.listen(128)
        print("Listening to on port {}".format(self.port))

        while True:
            client_sock, _ = self.sock.accept()
            thread = threading.Thread(
                target=Server.handle_sock, args=(client_sock, self.router, self.middlewares))
            thread.daemon = True
            thread.start()

    @staticmethod
    def handle_sock(client_sock: socket.socket, router: Router, middlewares: List[Middleware]) -> None:
        parser = RequestParser()
        while True:
            message = client_sock.recv(Server.BUFSIZE)
            is_parse_complete = parser.try_parse(message)
            if is_parse_complete:
                break

        try:
            req = parser.complete()
            next = Next(router.dispatch(req.uri, req.method), middlewares)
            res = next.run(req)
            print(req)
        except BadRequest:
            res = Response(status_code=StatusCode.BAD_REQUEST)
        except InternalServerError:
            res = Response(status_code=StatusCode.INTERNAL_SERVER_ERROR)

        res.send(client_sock)
        client_sock.close()
