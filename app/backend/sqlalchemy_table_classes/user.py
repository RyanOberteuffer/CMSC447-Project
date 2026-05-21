import enum
from sqlalchemy import Null, Column, Integer, String, Enum
from ..database import Base

class UserRoles(enum.Enum):
    ADMIN = "admin"
    USER = "user"
    DEVELOPER = "developer"
    NONE = Null

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False)
    role = Column(Enum(UserRoles))