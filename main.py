from libbbs.response import Response
from libbbs.request import Request
from libbbs.misc import Method, StatusCode
from libbbs.server import Server


def hello(_: Request) -> Response:
    return Response(status_code=StatusCode.OK)


def echo(req: Request) -> Response:
    res = Response()
    res.set_body(req.body)
    return res


server = Server(8080)
server.route("/", Method.GET, hello)
server.route("/", Method.POST, echo)
server.run()
