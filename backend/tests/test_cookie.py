from libbbs.cookie import CookieData


def test_parse_single_cookie_pair():
    data = CookieData("SID=blah")
    assert "blah" == data.get("SID")


def test_parse_multiple_cookie_pairs():
    data = CookieData("SID=blah;lang=meow")
    assert "blah" == data.get("SID")
    assert "meow" == data.get("lang")


def test_parse_multiple_cookie_pairs_with_whitespace():
    data = CookieData("SID=blah; lang=meow; hoge=cat")
    assert "blah" == data.get("SID")
    assert "meow" == data.get("lang")
    assert "cat" == data.get("hoge")


def test_parse_errornous_cookie_pairs():
    data = CookieData("SID=blah;lang=meow=hoge")
    assert "blah" == data.get("SID")
