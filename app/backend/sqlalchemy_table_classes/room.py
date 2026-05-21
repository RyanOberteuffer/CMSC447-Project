from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from ..database import Base

class Room(Base):
    __tablename__ = 'rooms'

    id = Column(Integer, primary_key=True)
    type = Column(String(100), nullable=False)
    room_number = Column(String(100), nullable=False)
    capacity = Column(Integer, nullable=False)
    description = Column(String(250), nullable=False)
    weekday_availability_start = Column(DateTime, nullable=False)
    weekday_availability_end = Column(DateTime, nullable=False)
    saturday_availability_start = Column(DateTime, nullable=False)
    saturday_availability_end = Column(DateTime, nullable=False)
    sunday_availability_start = Column(DateTime, nullable=False)
    sunday_availability_end = Column(DateTime, nullable=False)

    reservations = relationship('RoomReservation', back_populates='reservations')