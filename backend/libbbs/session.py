from dataclasses import dataclass, field
from typing import Dict, Optional
from libbbs.cookie import CookieData
import random
import string


def extract_session_id_inner(cookie_value: Optional[str], session_id: str) -> Optional[str]:
    if cookie_value is None:
        return None
    cookie_data = CookieData(cookie_value)
    return cookie_data.get(session_id)


@dataclass
class Session:
    __map: Dict[str, str] = field(init=False)
    __has_changed: bool = field(default=False, init=False)
    id: str = field(init=False)
    ID_LEN = 32

    def __post_init__(self) -> None:
        self.__map = {}
        id = [random.choice(
            string.ascii_lowercase + string.digits) for i in range(self.ID_LEN)]
        self.id = "".join(id)

    @property
    def has_changed(self) -> bool:
        return self.__has_changed

    def reset_changed(self):
        self.__has_changed = False

    def get(self, key: str) -> Optional[str]:
        return self.__map.get(key)

    def set(self, key: str, value: str):
        self.__has_changed = True
        self.__map[key] = value


@dataclass
class SessionStore:
    __map: Dict[str, Session] = field(default_factory=dict)

    def get(self, id: str) -> Optional[Session]:
        return self.__map.get(id)

    def set(self, id: str, session: Session):
        self.__map[id] = session

