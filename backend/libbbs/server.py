from dataclasses import dataclass, field
from typing import Callable, List
from libbbs.router import Handler, Router
from libbbs.misc import InternalServerError, Method, StatusCode
from libbbs.middleware import Middleware, Next
from libbbs.parse_request import RequestParser
from libbbs.request import Request
from libbbs.response import Response
import socket
import threading


@dataclass
class Server:
    BUFSIZE = 4096
    router: Router = field(default_factory=Router)
    middlewares: List[Middleware] = field(default_factory=list)

    def use(self, middleware: Middleware):
        self.middlewares.append(middleware)

    def route(self, uri: str, method: Method = Method.GET) -> Callable[[Handler], None]:
        def wrapper(handler: Handler):
            self.router.route(uri, method, handler)
        return wrapper

    def add_route(self, uri: str, method: Method, handler: Handler):
        self.router.route(uri, method, handler)

    def run(self, port: int) -> None:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
        sock.bind(("0.0.0.0", port))
        sock.listen(128)
        print("Listening to on port {}".format(port))

        while True:
            client_sock, _ = sock.accept()
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

        req = parser.complete()
        print(req)
        server = Server(router=router, middlewares=middlewares)
        res = server.respond(req)
        res.send(client_sock)
        client_sock.close()

    def respond(self, req: Request):
        try:
            next = Next(self.router.dispatch(
                req.uri, req.method), self.middlewares)
            return next.run(req)
        except InternalServerError:
            return Response(status_code=StatusCode.INTERNAL_SERVER_ERROR)
        except Exception:
            return Response(status_code=StatusCode.BAD_REQUEST)
