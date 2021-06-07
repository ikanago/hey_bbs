from dataclasses import dataclass
from typing import Optional

from libbbs.header_map import CaseInsensitiveMap


@dataclass
class CookieData:
    r""" Parse header value of a "Cookie" header and store it.

    Stored data are case insensitive; a key or value "Hoge" is treaded the
    same as "hoge".

    Example
    -------
    let cookie header be `Cookie: SID=Hoge;lang=meow`.
    ```python
    data = CookieData("SID=Hoge;lang=meow")
    assert "hoge" == data.get("SID")
    assert "meow" == data.get("lang")
    ```
    """

    __cookies: CaseInsensitiveMap

    def __init__(self, cookie_value: str) -> None:
        self.__cookies = CaseInsensitiveMap()
        self._parse_cookie_value(cookie_value)

    def _parse_cookie_value(self, cookie_value: str) -> None:
        cookie_pairs = cookie_value.split(";")
        for pair in cookie_pairs:
            pair = pair.strip()
            pair = pair.split("=")
            if len(pair) == 2:
                self.__cookies.set(pair[0], pair[1])

    def get(self, key: str) -> Optional[str]:
        return self.__cookies.get(key)

    def set(self, key: str, value: str) -> None:
        self.__cookies.set(key, value)
