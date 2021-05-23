from dataclasses import dataclass
import pytest
from libbbs.database import Comparison, Db, QueryableBy
from typing import List


@dataclass
class User(QueryableBy[str]):
    name: str

    def get(self) -> str:
        return self.name


@pytest.fixture
def users() -> Db[str]:
    return Db([User("Alex"), User("Jonathan"), User("Takashi"), User("Joseph"), User("Linus")])

def test_query(users: Db[str]):
    assert "Jonathan" == users.query("Jonathan")[0].name

def test_query_ord(users: Db[str]):
    actual: List[User] = users.query("Ken", Comparison.LE)
    assert "Alex" == actual[0].name
    assert "Jonathan" == actual[1].name
    assert "Joseph" == actual[2].name
