from dataclasses import dataclass
from tests.test_middleware import VALUE
from dataclasses_json import DataClassJsonMixin
from libbbs.body import Body
from libbbs.response import Response
from libbbs.request import Request
from libbbs.middleware import Middleware, Next
from libbbs.misc import Method, StatusCode
from libbbs.server import Server

VALUE = "test"


class TestMiddleware(Middleware):
    def call(self, req: Request, next: Next) -> Response:
        req["A"] = VALUE
        res = next.run(req)
        res["A"] = VALUE
        return res


@dataclass
class User(DataClassJsonMixin):
    username: str
    text: str


def hello(_: Request) -> Response:
    return Response(status_code=StatusCode.OK)


def echo(req: Request) -> Response:
    res = Response()
    if req.body is not None:
        user = req.body.from_json(User)
        print(user)
        res.set_body(Body.to_json(user))
    return res


server = Server(8080)
server.use(TestMiddleware())
server.route("/", Method.GET, hello)
server.route("/", Method.POST, echo)
server.run()
