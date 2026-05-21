import enum
from ..database import Base
from sqlalchemy import Column, Integer, String, Enum

class BookAvailabilityStatuses(enum.Enum):
    AVAILABLE = "available"
    CHECKED_OUT = "checked out"

class Book(Base):
    __tablename__ = 'books'

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    author = Column(String)
    isbn = Column(String)
    shelf_location = Column(String)
    availability_status = Column(Enum(BookAvailabilityStatuses), default=BookAvailabilityStatuses.AVAILABLE)