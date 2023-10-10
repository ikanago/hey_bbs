from json import dumps, loads
import os
import sqlalchemy
from libbbs.body import Body
from libbbs.login import LoginMiddleware
from libbbs.response import Response, see_other
from libbbs.request import Request
from libbbs.misc import Method, StatusCode
from libbbs.server import Server
from libbbs.session_middleware import SessionMiddleware
from libbbs.static_file import StaticFile
from model import Base, Image, Post, Thread, ThreadEncoder, User
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker


CREDENTIAL = "credential"
SESSION_ID = "SID"
USER_ID = "user_id"
USERNAME = "username"
CONTENT_TYPE = "Content-Type"
CONTENT_LENGTH = "Content-Length"
APPLICATION_JSON = "application/json"
IMAGE_PNG = "image/png"
IMAGE_JPG = "image/jpeg"

MYSQL_USER = os.environ.get("MYSQL_USER") or "root"
MYSQL_PASSWORD = os.environ.get("MYSQL_PASSWORD") or "test"
MYSQL_HOSTNAME = os.environ.get("MYSQL_HOSTNAME") or "db"
MYSQL_PORT = os.environ.get("MYSQL_PORT") or "3306"
MYSQL_DATABASE = os.environ.get("MYSQL_DATABASE") or "testdb"

engine = create_engine(
    f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOSTNAME}:{MYSQL_PORT}/{MYSQL_DATABASE}", pool_pre_ping=True)
while True:
    # Wait until database is ready.
    try:
        Base.metadata.create_all(engine)
    except sqlalchemy.exc.OperationalError:
        continue
    break
session_factory = sessionmaker(engine)
Session = scoped_session(session_factory)

server = Server()


@server.route("/verify_login")
def verify_login(req: Request) -> Response:
    if req.session is None:
        print("Session is not set")
        return Response(status_code=StatusCode.INTERNAL_SERVER_ERROR)

    if req.session.get(USER_ID) is None or req.session.get(USERNAME) is None:
        print("USER_ID or USERNAME is not set")
        return Response(status_code=StatusCode.UNAUTHORIZED)

    json = dumps({
        "username": req.session.get(USERNAME)
    })
    res = Response()
    res.set(CONTENT_TYPE, APPLICATION_JSON)
    res.body = Body.from_str(json)
    return res


@server.route("/signup", Method.POST)
def signup(req: Request) -> Response:
    body = req.body
    if body is None:
        return Response(status_code=StatusCode.UNAUTHORIZED)

    user = User.from_json(str(req.body))
    already_exist_users = Session.query(User).filter(
        User.username == user.username).all()
    if len(already_exist_users) != 0:
        return Response(status_code=StatusCode.BAD_REQUEST)
    Session.add(user)
    Session.commit()

    if req.session is None:
        return Response(status_code=StatusCode.INTERNAL_SERVER_ERROR)
    req.session.set(CREDENTIAL, user.credential())
    req.session.set(USER_ID, str(user.user_id))
    req.session.set(USERNAME, user.username)
    Session.remove()
    return Response()


@server.route("/login", Method.POST)
def login(req: Request) -> Response:
    body = req.body
    if body is None:
        return Response(status_code=StatusCode.UNAUTHORIZED)
    user = User.from_json(str(req.body))
    try:
        user_in_db = Session.query(User).filter(
            User.username == user.username).one()
        if user.username != user_in_db.username or user.password != user_in_db.password:
            print("Invalid credential.")
            raise Exception
        user = user_in_db
    except Exception:
        return Response(status_code=StatusCode.BAD_REQUEST)
    finally:
        Session.commit()

    if req.session is None:
        return Response(status_code=StatusCode.INTERNAL_SERVER_ERROR)
    req.session.set(CREDENTIAL, user.credential())
    req.session.set(USER_ID, user.user_id)
    req.session.set(USERNAME, user.username)
    Session.remove()
    return Response()


@server.route("/logout")
def logout(req: Request) -> Response:
    if req.session is None:
        print("Session is not set")
        return Response(status_code=StatusCode.INTERNAL_SERVER_ERROR)

    if req.session.get(USER_ID) is None or req.session.get(USERNAME) is None:
        print("USER_ID or USERNAME is not set")
        return Response(status_code=StatusCode.UNAUTHORIZED)

    req.session.delete()
    res = see_other("/login")
    cookie = f"{SESSION_ID}=deleted; expires=Thu, 01 Jan 1970 00:00:00 GMT"
    res.set("Set-Cookie", cookie)
    return res


def get_posts_inner(thread_name: str) -> Response:
    posts = Session.query(Post, User, Thread, Image) \
        .outerjoin(Image, Post.image_id == Image.image_id) \
        .filter(Thread.thread_name == thread_name) \
        .filter(Post.thread_id == Thread.thread_id) \
        .filter(User.user_id == Post.user_id) \
        .order_by(Post.post_id.desc()).limit(20).all()

    posts = [
        {
            "post_id": post.Post.post_id,
            "text": post.Post.text,
            "username": post.User.username,
            "image_id": post.Image.image_id if post.Image is not None else None,
        }
        for post in posts]
    json = dumps(posts)
    res = Response(body=Body.from_str(json))
    res.set(CONTENT_TYPE, APPLICATION_JSON)
    return res


@server.route("/posts/*")
def get_posts(req: Request) -> Response:
    thread_name = req.uri.split("/")[-1]
    return get_posts_inner(thread_name)


@server.route("/posts/*", Method.POST)
def create_post(req: Request) -> Response:
    if req.body is None:
        return Response(status_code=StatusCode.BAD_REQUEST)

    if req.session is None:
        return Response(status_code=StatusCode.INTERNAL_SERVER_ERROR)

    thread_name = req.uri.split("/")[-1]
    thread = Session.query(Thread).filter(
        Thread.thread_name == thread_name).one()
    post = Post.from_json(
        str(req.body), req.session.get(USER_ID), thread.thread_id)
    Session.add(post)
    Session.commit()
    Session.remove()

    return get_posts_inner(thread_name)


def get_threads_inner() -> Response:
    threads = Session.query(Thread).order_by(
        Thread.thread_id.desc()).limit(20).all()
    json = dumps(threads, cls=ThreadEncoder)
    res = Response(body=Body.from_str(json))
    res.set(CONTENT_TYPE, APPLICATION_JSON)
    return res


@server.route("/threads")
def get_threads(_req: Request) -> Response:
    return get_threads_inner()


@server.route("/threads", Method.POST)
def create_thread(req: Request) -> Response:
    if req.body is None:
        return Response(status_code=StatusCode.BAD_REQUEST)

    thread = Thread.from_json(str(req.body))
    already_exist_threads = Session.query(Thread).filter(
        Thread.thread_name == thread.thread_name).all()
    if len(already_exist_threads) != 0:
        return Response(status_code=StatusCode.BAD_REQUEST)
    Session.add(thread)
    Session.commit()
    Session.remove()
    return get_threads_inner()


@server.route("/image", Method.POST)
def get_image(req: Request) -> Response:
    if req.body is None:
        return Response(status_code=StatusCode.BAD_REQUEST)

    json = loads(str(req.body))
    print(json)
    try:
        image = Session.query(Image).filter(
            Image.image_id == json["image_id"]).one()
    except:
        # No corresponding images.
        print("Failed to get image:", json["image_id"])
        Session.commit()
        Session.remove()
        return Response()
    Session.commit()

    body = Body(image.entity)
    res = Response(body=body)
    res.set(CONTENT_TYPE, image.image_type)
    res.set(CONTENT_LENGTH, str(body.size()))
    Session.remove()
    return res


@server.route("/upload_image", Method.POST)
def upload_image(req: Request) -> Response:
    if req.body is None:
        return Response(status_code=StatusCode.BAD_REQUEST)

    mime = req.get(CONTENT_TYPE)
    if mime is None:
        return Response(status_code=StatusCode.BAD_REQUEST)

    if mime != IMAGE_PNG and mime != IMAGE_JPG:
        return Response(status_code=StatusCode.BAD_REQUEST)

    image = Image(image_type=mime, entity=req.body.to_bytes())
    Session.add(image)
    Session.commit()
    print("image id:", image.image_id)
    json = {
        "image_id": image.image_id,
    }
    body = Body.from_str(dumps(json))
    res = Response(body=body)
    res.set(CONTENT_TYPE, APPLICATION_JSON)
    res.set(CONTENT_LENGTH, str(body.size()))
    Session.remove()
    return res


def main():
    server.use(SessionMiddleware(SESSION_ID))
    server.use(LoginMiddleware(
        ["/verify_login", "/signup", "/login", "/static"], credential_key=CREDENTIAL))
    server.serve_directory("/static", "build/static")
    server.add_route("/*", Method.GET, StaticFile("build/index.html"))
    server.run(8080)


if __name__ == "__main__":
    main()
