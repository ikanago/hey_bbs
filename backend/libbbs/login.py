from dataclasses import dataclass
from typing import List
from libbbs.middleware import Middleware, Next
from libbbs.misc import StatusCode
from libbbs.request import Request
from libbbs.response import Response


@dataclass
class Login(Middleware):
    r"""Middleware to check if a request has a valid session.

    Args:
        exclude_path: URIs which do not need to check a session.
        realm: This path and child paths need check.
        credential_key: Key of session to use login validation.
    """

    exclude_path: List[str]
    realm: str = "/"
    credential_key: str = "CREDENTIAL"

    def call(self, req: Request, next: Next) -> Response:
        if not req.uri.startswith(self.realm):
            return next.run(req)
        for path in self.exclude_path:
            if req.uri == path:
                return next.run(req)

        # All requests to `req.uri` need login credentials.
        session = req.session
        if session is None:
            print("SessionMiddleware is necessary to maintain login.")
            return Response(status_code=StatusCode.INTERNAL_SERVER_ERROR)

        credential = session.get(self.credential_key)
        if credential is None:
            return Response(status_code=StatusCode.UNAUTHORIZED)

        return next.run(req)
