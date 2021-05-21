import socket
import threading


class Server:
    def __init__(self, port: int) -> None:
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def run(self) -> None:
        self.sock.bind(("0.0.0.0", self.port))
        self.sock.listen(128)

        while True:
            client_sock, _ = self.sock.accept()
            thread = threading.Thread(
                target=Server.handle_sock, args=(client_sock,))
            thread.daemon = True
            thread.start()

    def handle_sock(client_sock) -> None:
        while True:
            message = client_sock.recv(1024)
            print(message)
            if len(message) == 0:
                break
            client_sock.send(message)
        client_sock.close()
