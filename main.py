from dataclasses import dataclass
from dataclasses_json import DataClassJsonMixin
from libbbs.body import Body
from libbbs.cors import Cors
from libbbs.response import Response
from libbbs.request import Request
from libbbs.middleware import Middleware, Next
from libbbs.misc import Method, StatusCode
from libbbs.server import Server

VALUE = "test"


class TestMiddleware(Middleware):
    def call(self, req: Request, next: Next) -> Response:
        req.set("A", VALUE)
        res = next.run(req)
        res.set("A", VALUE)
        return res


@dataclass
class User(DataClassJsonMixin):
    username: str
    text: str


def hello(_: Request) -> Response:
    return Response()


def echo(req: Request) -> Response:
    res = Response()
    if req.body is not None:
        user = req.body.from_json(User)
        print(user)
        res.set_body(Body.to_json(user))
    return res


server = Server()
server.use(Cors(allow_origin="localhost:3000"))
server.route("/", Method.GET, hello)
server.route("/", Method.POST, echo)
server.run(8080)
