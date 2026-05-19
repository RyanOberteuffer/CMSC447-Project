import enum
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
class BookAvailabilityStatuses(enum.Enum):
    AVAILABLE = "available"
    CHECKED_OUT = "checked out"

class Book(db.Model):
    __tablename__ = 'books'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    author = db.Column(db.String)
    isbn = db.Column(db.String)
    shelf_location = db.Column(db.String)
    availability_status = db.Column(db.Enum(BookAvailabilityStatuses), default=BookAvailabilityStatuses.AVAILABLE)