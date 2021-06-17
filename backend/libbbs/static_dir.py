from dataclasses import dataclass
from libbbs.body import Body
from libbbs.handler import HandlerMixin
from libbbs.misc import Mime, StatusCode
from libbbs.request import Request
from libbbs.response import Response
import os


@dataclass
class StaticDir(HandlerMixin):
    """
    Parameters
    ----------
    mount_uri: str
        URI to which static assets in the `serve_dir` are mount.
    serve_dir: str
        Directory name whose inner contents are served.
    """

    mount_uri: str
    serve_dir: str

    def call(self, req: Request) -> Response:
        filename_to_serve = req.uri.lstrip(self.mount_uri)
        path_to_serve = os.path.join(self.serve_dir, filename_to_serve)

        if not os.path.exists(path_to_serve):
            print(path_to_serve)
            return Response(status_code=StatusCode.NOT_FOUND)

        with open(path_to_serve, "r") as f:
            mime = Mime.from_filename(path_to_serve)
            body = Body.from_str(f.read())
            res = Response()
            res.set_body(body, mime)
            return res
