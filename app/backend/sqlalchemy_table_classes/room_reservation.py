from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from ..database import Base
from datetime import datetime, timezone

class RoomReservation(Base):
    __tablename__ = 'room_reservations'

    id = Column(Integer, primary_key=True)
    student_name = Column(String, nullable=False)
    start_dt = Column(DateTime, nullable=False)
    end_dt = Column(DateTime, nullable=False)
    request_timestamp = Column(DateTime, default=datetime.now(tz=timezone.utc), nullable=False)
    deleted_at = Column(DateTime, nullable=False, default=None)

    room_id = Column(Integer, ForeignKey('rooms.id'), nullable=False)
    room = relationship('Room', back_populates='room')
