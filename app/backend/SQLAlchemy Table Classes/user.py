import enum
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Null

db = SQLAlchemy()
class UserRoles(enum.Enum):
    ADMIN = "admin"
    USER = "user"
    DEVELOPER = "developer"
    NONE = Null

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    role = db.Column(db.Enum(UserRoles))