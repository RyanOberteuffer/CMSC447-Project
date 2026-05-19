from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone

db = SQLAlchemy()
class RoomReservation(db.Model):
    __tablename__ = 'room_reservations'

    id = db.Column(db.Integer, primary_key=True)
    student_name = db.Column(db.String, nullable=False)
    start_dt = db.Column(db.DateTime, nullable=False)
    end_dt = db.Column(db.DateTime, nullable=False)
    request_timestamp = db.Column(db.DateTime, default=datetime.now(tz=timezone.utc), nullable=False)
    deleted_at = db.Column(db.DateTime, nullable=False, default=None)

    room_id = db.Column(db.Integer, db.ForeignKey('rooms.id'), nullable=False)
    room = db.relationship('Room', back_populates='room')
