from dataclasses import dataclass
from datetime import datetime, time, date
from app.backend.table_object_classes.table_object import TableObject

@dataclass
class RoomReservation(TableObject):
    id: int
    student_name: str
    room_id: int
    date: date
    start_time: time
    end_time: time
    request_timestamp: datetime
    is_canceled: bool = False

    def __post_init__(self):
        if self.is_canceled != 0 and self.is_canceled != 1:
            raise AttributeError("Room Reservation is_canceled must be 0 or 1")
        if (self.start_time > self.end_time) and self.start_time != time.fromisoformat("23:00:00"):
            raise AttributeError("Room Reservation start_time must be before end_time")

    def __eq__(self, other):
        """
        Two RoomReservation objects are equal given they share the same room_id, date, and start_time
        """
        if not isinstance(other, RoomReservation):
            is_equal = False
        else:
            is_equal = (self.room_id == other.room_id) and (self.date == other.date) and (self.start_time == other.start_time)

        return is_equal

    def __hash__(self):
        return hash((self.room_id, self.date, self.start_time))

    @classmethod
    def from_row(cls, row):
        try:
            return cls(row["id"],
                       row["student_name"],
                       row["room_id"],
                       date.fromisoformat(row["reservation_date"]),
                       time.fromisoformat(row["start_time"]),
                       time.fromisoformat(row["end_time"]),
                       row["request_timestamp"],
                       bool(row["is_canceled"]))
        except (KeyError, IndexError) as e:
            raise AttributeError(f"Database Mapping Error: Column {e} not found in row passed to from_row") from e

    def to_row(self):
        return {"id": self.id,
                "student_name": self.student_name,
                "room_id": self.room_id,
                "reservation_date": self.date,
                "start_time": self.start_time,
                "end_time": self.end_time,
                "request_timestamp": self.request_timestamp,
                "is_canceled": self.is_canceled
        }