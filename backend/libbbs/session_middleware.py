from dataclasses import dataclass, field
from libbbs.cookie import CookieData
from libbbs.response import Response
from libbbs.middleware import Middleware, Next
from libbbs.request import Request
from libbbs.session import Session, SessionStore


@dataclass
class SessionMiddleware(Middleware):
    session_id: str
    path: str = "/"
    __store: SessionStore = field(default_factory=SessionStore)

    def call(self, req: Request, next: Next) -> Response:
        if not req.uri.startswith(self.path):
            return next.run(req)
        session_id = req.extract_session_id(self.session_id)
        if session_id is None:
            session = Session()
            self.__store.set(session.id, session)
            req.session = session
        else:
            session = self.__store.get(session_id)
            if session is None:
                session = Session()
                self.__store.set(session.id, session)
                req.session = session
            else:
                # The request has cookie and it contains valid session ID.
                req.session = session

        res = next.run(req)

        if req.session is not None and req.session.has_changed:
            cookie = f"{self.session_id}={req.session.id}"
            res.set("Set-Cookie", cookie)
        return res
