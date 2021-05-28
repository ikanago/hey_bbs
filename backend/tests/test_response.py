from libbbs.misc import Mime, StatusCode
from libbbs.body import Body
from libbbs.response import Response, found, moved_permanently, see_other


def test_set_body():
    res = Response()
    res.set_body(Body(b"Hello"), Mime.APPLICATION_JSON)
    assert Body(b"Hello") == res.body
    assert "5" == res.get("content-length")
    assert "application/json" == res.get("content-type")


LOCATION = "example.com"


def test_moved_permanently():
    res = moved_permanently(LOCATION)
    assert StatusCode.MovedPermanently == res.status_code
    assert LOCATION == res.get("Location")


def test_found():
    res = found(LOCATION)
    assert StatusCode.Found == res.status_code
    assert LOCATION == res.get("Location")


def test_see_other():
    res = see_other(LOCATION)
    assert StatusCode.SeeOther == res.status_code
    assert LOCATION == res.get("Location")
