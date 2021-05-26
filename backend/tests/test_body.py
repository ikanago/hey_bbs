from typing import List
from libbbs.misc import BadRequest
import pytest
from dataclasses_json import DataClassJsonMixin
from dataclasses import dataclass
from libbbs.body import Body


@dataclass
class User(DataClassJsonMixin):
    username: str
    group: List[str]


@pytest.fixture
def user() -> User:
    return User("John", ["a", "b"])


@pytest.fixture
def user_valid_json() -> Body:
    return Body(b'{"username": "John", "group": ["a", "b"]}')


@pytest.fixture
def user_invalid_json() -> Body:
    return Body(b'{"username": "John"}')


def test_decode_valid_json(user: User, user_valid_json: Body):
    assert user == user_valid_json.from_json(User)


def test_decode_invalid_json(user_invalid_json: Body):
    with pytest.raises(BadRequest):
        user_invalid_json.from_json(User)
