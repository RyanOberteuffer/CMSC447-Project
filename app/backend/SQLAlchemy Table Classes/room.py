from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
class Room(db.Model):
    __tablename__ = 'rooms'

    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(100), nullable=False)
    room_number = db.Column(db.String(100), nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(250), nullable=False)
    weekday_availability_start = db.Column(db.DateTime, nullable=False)
    weekday_availability_end = db.Column(db.DateTime, nullable=False)
    saturday_availability_start = db.Column(db.DateTime, nullable=False)
    saturday_availability_end = db.Column(db.DateTime, nullable=False)
    sunday_availability_start = db.Column(db.DateTime, nullable=False)
    sunday_availability_end = db.Column(db.DateTime, nullable=False)

    reservations = db.relationship('RoomReservation', back_populates='reservations')