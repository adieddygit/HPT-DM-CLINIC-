from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy import Integer, String, DateTime, func
from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped
import enum
# from models import Base, BaseModel

class Base(DeclarativeBase):
    pass

class BaseModel:
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()
    
class Role(enum.Enum):
    ADMIN = 'admin'
    CLIENT = 'client'
    CLINICAL = 'clinical'

class Users(Base, BaseModel):
    __tablename__ = 'users'
    id:Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name:Mapped[str] = mapped_column(String(200))
    email:Mapped[str] = mapped_column(String(100), unique=True)
    password:Mapped[str] = mapped_column(String(200))
    role:Mapped[Role]
    patient_id:Mapped[str] = mapped_column(Integer, ForeignKey('patient_reg.patient_id', ondelete='CASCADE', onupdate='CASCADE'))
    created_at:Mapped[str] = mapped_column(DateTime, default=func.now())






