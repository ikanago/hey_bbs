from __future__ import annotations
from json import loads, JSONEncoder
from typing import Any, Dict
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.schema import Column, ForeignKey
from sqlalchemy.sql.sqltypes import Integer, String

Base = declarative_base()


class Post(Base):
    __tablename__ = "post"
    post_id = Column(Integer, primary_key=True, autoincrement=True,
                     nullable=False, unique=True)
    user_id = Column(Integer, ForeignKey("user.user_id"))
    text = Column(String(255), nullable=False)

    def from_json(json: str, user_id: str) -> Post:
        data = loads(json)
        return Post(user_id=user_id, text=data["text"])


class PostEncoder(JSONEncoder):
    def default(self, obj: Any) -> Dict[str, str]:
        if isinstance(obj, Post):
            return {
                "post_id": str(obj.post_id),
                "text": obj.text,
            }
        else:
            return JSONEncoder.default(self, obj)


class User(Base):
    __tablename__ = "user"
    user_id = Column(Integer, primary_key=True, autoincrement=True,
                     nullable=False, unique=True)
    username = Column(String(255), nullable=False, unique=True)
    password = Column(String(256), nullable=False)

    def from_json(json: str) -> User:
        data = loads(json)
        return User(username=data["username"], password=data["password"])

    def credential(self) -> str:
        return f"{self.username}:{self.password}"


class UserEncoder(JSONEncoder):
    def default(self, obj: Any) -> Dict[str, str]:
        if isinstance(obj, User):
            return {
                "user_id": str(obj.user_id),
                "username": obj.username,
            }
        else:
            return JSONEncoder.default(self, obj)
