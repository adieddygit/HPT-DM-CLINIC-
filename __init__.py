from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy import Integer, String, DateTime, func
from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped
import enum
from .models import *


class Base(DeclarativeBase):
    pass

class BaseModel:
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()