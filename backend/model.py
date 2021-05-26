from dataclasses import dataclass, field
from typing import List
from dataclasses_json import DataClassJsonMixin


@dataclass
class User(DataClassJsonMixin):
    id: int
    username: str


@dataclass
class Users(DataClassJsonMixin):
    _users: List[User]


@dataclass
class Post(DataClassJsonMixin):
    id: int
    user_id: int
    text: str


@dataclass
class Posts(DataClassJsonMixin):
    _posts: List[Post]
    _registered_id: int = field(default=1, init=False)

    def create_post(self, post: Post) -> None:
        self._registered_id += 1
        self._posts.append(post)
