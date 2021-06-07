from json import dumps
import sqlalchemy
from libbbs.body import Body
from libbbs.cors import CorsMiddleware
from libbbs.login import LoginMiddleware
from libbbs.response import Response, see_other
from libbbs.request import Request
from libbbs.misc import Method, StatusCode
from libbbs.server import Server
from libbbs.session_middleware import SessionMiddleware
from model import Base, Post, PostEncoder, User
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


SESSION_ID = "SID"
CREDENTIAL = "credential"
USERNAME = "username"


engine = create_engine(
    "mysql+pymysql://root:test@db:3306/testdb", pool_pre_ping=True)
while True:
    # Wait until database is ready.
    try:
        Base.metadata.create_all(engine)
    except sqlalchemy.exc.OperationalError:
        continue
    break
SessionClass = sessionmaker(engine)
session = SessionClass()


def verify_login(req: Request) -> Response:
    if req.session is None:
        print("Session is not set")
        return Response(status_code=StatusCode.INTERNAL_SERVER_ERROR)
    username = req.session.get(USERNAME)
    if username is None:
        return Response(status_code=StatusCode.UNAUTHORIZED)
    json = dumps({
        "username": username
    })
    res = Response()
    res.body = Body.from_str(json)
    return res


def signup(req: Request) -> Response:
    body = req.body
    if body is None:
        return Response(status_code=StatusCode.UNAUTHORIZED)
    user = User.from_json(str(req.body))
    already_exist_users = session.query(User).filter(
        User.username == user.username).all()
    print(already_exist_users)
    if len(already_exist_users) != 0:
        return Response(status_code=StatusCode.BAD_REQUEST)
    session.add(user)
    session.commit()

    if req.session is None:
        return Response(status_code=StatusCode.INTERNAL_SERVER_ERROR)
    req.session.set(CREDENTIAL, user.credential())
    req.session.set(USERNAME, user.username)
    return see_other("/posts")


def login(req: Request) -> Response:
    body = req.body
    if body is None:
        return Response(status_code=StatusCode.UNAUTHORIZED)
    user = User.from_json(str(req.body))
    try:
        user_in_db = session.query(User).filter(
            User.username == user.username).one()
        if user.username != user_in_db.username or user.password != user_in_db.password:
            raise Exception
    except Exception:
        return Response(status_code=StatusCode.BAD_REQUEST)
    finally:
        session.commit()

    if req.session is None:
        return Response(status_code=StatusCode.INTERNAL_SERVER_ERROR)
    req.session.set(CREDENTIAL, user.credential())
    return see_other("/posts")


def get_posts_inner() -> Response:
    posts = session.query(Post).order_by(Post.post_id.desc()).limit(5).all()
    res = Response()
    body = dumps(posts, cls=PostEncoder)
    res.set_body(Body.from_str(body))
    return res


def get_posts(_req: Request) -> Response:
    return get_posts_inner()


def create_post(req: Request) -> Response:
    if req.body is None:
        return Response(status_code=StatusCode.BAD_REQUEST)

    post = Post.from_json(str(req.body))
    session.add(post)
    session.commit()

    return get_posts_inner()


def main():
    server = Server()
    # server.use(CorsMiddleware(allow_origin="http://localhost:3000", allow_credentials="true"))
    server.use(SessionMiddleware(SESSION_ID))
    server.use(LoginMiddleware(
        ["/verify_login", "/signup", "/login"], credential_key=CREDENTIAL))
    server.route("/verify_login", Method.GET, verify_login)
    server.route("/signup", Method.POST, signup)
    server.route("/login", Method.POST, login)
    server.route("/posts", Method.GET, get_posts)
    server.route("/posts", Method.POST, create_post)
    server.run(8080)


if __name__ == "__main__":
    main()
