from libbbs.misc import Mime
from libbbs.body import Body
from libbbs.response import Response


def test_set_body():
    res = Response()
    res.set_body(Body(b"Hello"), Mime.APPLICATION_JSON)
    assert Body(b"Hello") == res.body
    assert "5" == res["content-length"]
    assert "application/json" == res["content-type"]
