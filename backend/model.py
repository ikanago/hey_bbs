from __future__ import annotations
from json import loads, JSONEncoder
from typing import Any, Dict
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import null
from sqlalchemy.sql.schema import Column, ForeignKey
from sqlalchemy.sql.sqltypes import Integer, String
from sqlalchemy.dialects.mysql.types import LONGBLOB

Base = declarative_base()


class Post(Base):
    __tablename__ = "post"
    post_id = Column(Integer, primary_key=True, autoincrement=True,
                     nullable=False, unique=True)
    text = Column(String(255), nullable=False)
    user_id = Column(Integer, ForeignKey("user.user_id"))
    thread_id = Column(Integer, ForeignKey("thread.thread_id"))
    image_id = Column(Integer, ForeignKey("image.image_id"), nullable=True)

    def from_json(json: str, user_id: str, thread_id: str) -> Post:
        data = loads(json)
        return Post(text=data.get("text"), user_id=user_id, thread_id=thread_id, image_id=data.get("image_id"))


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
    posts = relationship("Post")

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


class Thread(Base):
    __tablename__ = "thread"
    thread_id = Column(Integer, primary_key=True, autoincrement=True,
                       nullable=False, unique=True)
    thread_name = Column(String(255), nullable=False, unique=True)
    posts = relationship("Post")

    def from_json(json: str) -> Thread:
        data = loads(json)
        return Thread(thread_name=data["thread_name"])


class ThreadEncoder(JSONEncoder):
    def default(self, obj: Any) -> Dict[str, str]:
        if isinstance(obj, Thread):
            return {
                "thread_id": str(obj.thread_id),
                "thread_name": obj.thread_name,
            }
        else:
            return JSONEncoder.default(self, obj)


class Image(Base):
    __tablename__ = "image"
    image_id = Column(Integer, primary_key=True, autoincrement=True,
                      nullable=False, unique=True)
    image_type = Column(String(255), nullable=False)
    entity = Column(LONGBLOB)
    posts = relationship("Post")
