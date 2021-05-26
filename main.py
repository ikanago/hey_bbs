from typing import List
from libbbs.body import Body
from libbbs.cors import Cors
from libbbs.response import Response
from libbbs.request import Request
from libbbs.middleware import Middleware, Next
from libbbs.misc import Method, StatusCode
from libbbs.server import Server
from model import Post, Posts


posts: Posts = Posts([Post(1, 1, "hoge"), Post(2, 1, "fuga")])
# users: Users = Users([User(1, "John")])


def get_posts(req: Request) -> Response:
    res = Response()
    body = Body.to_json(posts)
    res.set_body(body)
    return res


def create_post(req: Request) -> Response:
    if req.body is None:
        return Response(status_code=StatusCode.BAD_REQUEST)

    post = req.body.from_json(Post)
    posts.create_post(post)

    res = Response()
    body = Body.to_json(posts)
    res.set_body(body)
    return res


def main():
    server = Server()
    server.use(Cors(allow_origin="localhost:3000"))
    server.route("/posts", Method.GET, get_posts)
    server.route("/posts", Method.POST, create_post)
    server.run(8080)


if __name__ == "__main__":
    main()
