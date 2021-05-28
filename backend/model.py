from __future__ import annotations
from json import dumps, loads, JSONEncoder
from typing import Any, Dict
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.schema import Column
from sqlalchemy.sql.sqltypes import Integer, String

Base = declarative_base()


class Post(Base):
    __tablename__ = "post"
    id = Column(Integer, primary_key=True, autoincrement=True,
                nullable=False, unique=True)
    text = Column(String(255))

    def from_json(json: str) -> Post:
        data = loads(json)
        return Post(text=data["text"])

    def to_json(self) -> str:
        data = {
            "id": str(self.id),
            "text": self.text,
        }
        return dumps(data)


class PostEncoder(JSONEncoder):
    def default(self, obj: Any) -> Dict[str, str]:
        if isinstance(obj, Post):
            return {
                "id": str(obj.id),
                "text": obj.text,
            }
        else:
            return JSONEncoder.default(self, obj)
