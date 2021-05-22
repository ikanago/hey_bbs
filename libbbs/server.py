from libbbs.parse_request import parse_request
import socket
import threading


class Server:
    BUFSIZE = 4096

    def __init__(self, port: int) -> None:
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)

    def run(self) -> None:
        self.sock.bind(("0.0.0.0", self.port))
        self.sock.listen(128)

        while True:
            client_sock, _ = self.sock.accept()
            thread = threading.Thread(
                target=Server.handle_sock, args=(client_sock,))
            thread.daemon = True
            thread.start()

    def handle_sock(client_sock: socket.socket) -> None:
        buffer = b""
        # Parse request line and header
        while True:
            message = client_sock.recv(Server.BUFSIZE)
            print(message)
            buffer += message
            end_of_header = buffer.find(b"\r\n\r\n")
            if end_of_header >= 0:
                request_message = buffer[:end_of_header]
                # Skip CRLF to parse request body
                buffer = buffer[(end_of_header + 4):]
                break

        req = parse_request(request_message)
        print(req.method, req.uri)
        # Parse request body
        # if req.content_length() > 0:
        #     while True:
        #         message = client_sock.recv(Server.BUFSIZE)
        #         buffer += message
        #         if len(buffer) == req.content_length():
        #             break

        client_sock.send(b"HTTP/1.1 200 OK\r\n\r\n")
        client_sock.close()
