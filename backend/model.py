from dataclasses import dataclass, field
from typing import List
from dataclasses_json import DataClassJsonMixin
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.schema import Column
from sqlalchemy.sql.sqltypes import Integer, String


Base = declarative_base()


@dataclass
class User(DataClassJsonMixin):
    id: int
    username: str


@dataclass
class Users(DataClassJsonMixin):
    _users: List[User]


class Post(Base):
    __tablename__ = "post"
    id = Column(Integer, primary_key=True)
    text = Column(String(255))


@dataclass
class Posts(DataClassJsonMixin):
    _posts: List[Post]
    _registered_id: int = field(default=1, init=False)

    def create_post(self, post: Post) -> None:
        self._registered_id += 1
        self._posts.append(post)
