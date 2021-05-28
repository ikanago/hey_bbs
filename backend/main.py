from json import dumps
import sqlalchemy
from libbbs.body import Body
from libbbs.cors import Cors
from libbbs.response import Response
from libbbs.request import Request
from libbbs.misc import Method, StatusCode
from libbbs.server import Server
from model import Base, Post, PostEncoder
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


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


def get_posts_inner() -> Response:
    posts = session.query(Post).order_by(Post.id.desc()).limit(5).all()
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
    server.use(Cors(allow_origin="http://localhost:3000"))
    server.route("/posts", Method.GET, get_posts)
    server.route("/posts", Method.POST, create_post)
    server.run(8080)


if __name__ == "__main__":
    main()
