from typing import List
from json import load

import sqlalchemy
from libbbs.body import Body
from libbbs.cors import Cors
from libbbs.response import Response
from libbbs.request import Request
from libbbs.middleware import Middleware, Next
from libbbs.misc import Method, StatusCode
from libbbs.server import Server
from model import Base, Post, Posts
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


# posts: Posts = Posts([Post(1, 1, "hoge"), Post(2, 1, "fuga")])

engine = create_engine("mysql+pymysql://root:test@db:3306/testdb", pool_pre_ping=True)
while True:
    # Wait until database is ready.
    try:
        Base.metadata.create_all(engine)
    except sqlalchemy.exc.OperationalError:
        continue
    break
SessionClass = sessionmaker(engine)
session = SessionClass()

def get_posts(req: Request) -> Response:
    res = Response()
    body = Body.to_json(posts)
    res.set_body(body)
    return res


def create_post(req: Request) -> Response:
    if req.body is None:
        return Response(status_code=StatusCode.BAD_REQUEST)

    post = load(str(req.body))
    post = Post(id=int(post["id"]), text=post["text"])
    print(post)
    session.add(post)
    session.commit()

    posts = session.query(Post).all()
    print(posts)
    res = Response()
    # body = Body.to_json(posts)
    # res.set_body(body)
    return res


def main():
    server = Server()
    server.use(Cors(allow_origin="localhost:3000"))
    server.route("/posts", Method.GET, get_posts)
    server.route("/posts", Method.POST, create_post)
    server.run(8080)


if __name__ == "__main__":
    main()
