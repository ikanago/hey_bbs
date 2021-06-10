from json import dumps
import sqlalchemy
from libbbs.body import Body
from libbbs.login import LoginMiddleware
from libbbs.response import Response, see_other
from libbbs.request import Request
from libbbs.misc import Method, StatusCode
from libbbs.server import Server
from libbbs.session_middleware import SessionMiddleware
from model import Base, Post, PostEncoder, User
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


CREDENTIAL = "credential"
SESSION_ID = "SID"
USER_ID = "user_id"
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

server = Server()


@server.route("/verify_login")
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


@server.route("/signup", Method.POST)
def signup(req: Request) -> Response:
    body = req.body
    if body is None:
        return Response(status_code=StatusCode.UNAUTHORIZED)

    user = User.from_json(str(req.body))
    already_exist_users = session.query(User).filter(
        User.username == user.username).all()
    if len(already_exist_users) != 0:
        return Response(status_code=StatusCode.BAD_REQUEST)
    session.add(user)
    session.commit()

    if req.session is None:
        return Response(status_code=StatusCode.INTERNAL_SERVER_ERROR)
    req.session.set(CREDENTIAL, user.credential())
    req.session.set(USER_ID, str(user.user_id))
    req.session.set(USERNAME, user.username)
    return see_other("/posts")


@server.route("/login", Method.POST)
def login(req: Request) -> Response:
    body = req.body
    if body is None:
        return Response(status_code=StatusCode.UNAUTHORIZED)
    user = User.from_json(str(req.body))
    try:
        user_in_db = session.query(User).filter(
            User.username == user.username).one()
        if user.username != user_in_db.username or user.password != user_in_db.password:
            print("Invalid credential.")
            raise Exception
        user = user_in_db
    except Exception:
        return Response(status_code=StatusCode.BAD_REQUEST)
    finally:
        session.commit()

    if req.session is None:
        return Response(status_code=StatusCode.INTERNAL_SERVER_ERROR)
    req.session.set(CREDENTIAL, user.credential())
    req.session.set(USER_ID, user.user_id)
    req.session.set(USERNAME, user.username)
    return see_other("/posts")


def get_posts_inner() -> Response:
    posts = session.query(Post, User).join(Post, Post.user_id == User.user_id).order_by(Post.post_id.desc()).limit(20).all()
    print(posts)
    posts = [
        {
            "post_id": post.Post.post_id,
            "text": post.Post.text,
            "username": post.User.username,
        }
        for post in posts]
    body = dumps(posts)
    res = Response()
    res.set_body(Body.from_str(body))
    return res


@server.route("/posts")
def get_posts(_req: Request) -> Response:
    return get_posts_inner()


@server.route("/posts", Method.POST)
def create_post(req: Request) -> Response:
    if req.body is None:
        return Response(status_code=StatusCode.BAD_REQUEST)

    if req.session is None:
        return Response(status_code=StatusCode.INTERNAL_SERVER_ERROR)

    print(req.session)
    post = Post.from_json(str(req.body), req.session.get(USER_ID))
    session.add(post)
    session.commit()

    return get_posts_inner()


def main():
    server.use(SessionMiddleware(SESSION_ID))
    server.use(LoginMiddleware(
        ["/verify_login", "/signup", "/login"], credential_key=CREDENTIAL))
    server.run(8080)


if __name__ == "__main__":
    main()
