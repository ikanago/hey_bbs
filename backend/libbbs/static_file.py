from dataclasses import dataclass
from libbbs.body import Body
from libbbs.handler import HandlerMixin
from libbbs.misc import Mime, StatusCode
from libbbs.request import Request
from libbbs.response import Response
import os


@dataclass
class StaticFile(HandlerMixin):
    """
    Parameters
    ----------
    serve_file: str
        Filename to serve.
    """

    serve_file: str

    def call(self, _req: Request) -> Response:
        if not os.path.exists(self.serve_file):
            print(self.serve_file)
            return Response(status_code=StatusCode.NOT_FOUND)

        with open(self.serve_file, "r") as f:
            mime = Mime.from_filename(self.serve_file)
            body = Body.from_str(f.read())
            print(body)
            res = Response()
            res.set_body(body, mime)
            return res
