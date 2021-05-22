from libbbs.router import Handler, Router
from libbbs.misc import BadRequest, Method, StatusCode
from libbbs.response import Response
from libbbs.parse_request import parse_request
import socket
import threading


class Server:
    BUFSIZE = 4096

    def __init__(self, port: int) -> None:
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
        self.router = Router()

    def route(self, uri: str, method: Method, handler: Handler):
        self.router.route(uri, method, handler)

    def run(self) -> None:
        self.sock.bind(("0.0.0.0", self.port))
        self.sock.listen(128)
        print("Listening to on port {}".format(self.port))

        while True:
            client_sock, _ = self.sock.accept()
            thread = threading.Thread(
                target=Server.handle_sock, args=(client_sock,  self.router))
            thread.daemon = True
            thread.start()

    def handle_sock(client_sock: socket.socket, router: Router) -> None:
        buffer = b""
        # Parse request line and header
        while True:
            message = client_sock.recv(Server.BUFSIZE)
            buffer += message
            end_of_header = buffer.find(b"\r\n\r\n")
            if end_of_header >= 0:
                request_message = buffer[:end_of_header]
                # Skip CRLF to parse request body
                buffer = buffer[(end_of_header + 4):]
                break

        try:
            req = parse_request(request_message)
            res = router.dispatch(req.uri, req.method)(req)
            print(req)
        except BadRequest:
            res = Response.from_status_code(StatusCode.BAD_REQUEST)

        res.send(client_sock)
        client_sock.close()
