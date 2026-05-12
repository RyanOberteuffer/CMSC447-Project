from dataclasses import dataclass
from datetime import datetime
from app.backend.table_object_classes.table_object import TableObject

@dataclass
class RoomReservation(TableObject):
    id: int
    student_name: str
    room_id: int
    start_dt: datetime
    end_dt: datetime
    request_timestamp: datetime
    is_canceled: bool = False

    def __post_init__(self):
        if self.start_dt > self.end_dt:
            raise AttributeError(f"Room Reservation start_dt must be before end_dt. start_dt = {self.start_dt}, end_dt = {self.end_dt}")

    def __eq__(self, other):
        """
        Two RoomReservation objects are equal given they share the same room_id, start_dt, and end_dt.
        """
        if not isinstance(other, RoomReservation):
            is_equal = False
        else:
            is_equal = (self.room_id == other.room_id) and (self.start_dt == other.end_dt) and (self.end_dt == other.end_dt)

        return is_equal

    def __hash__(self):
        return hash((self.room_id, self.start_dt, self.end_dt))

    @classmethod
    def from_row(cls, row):
        try:
            return cls(row["id"],
                       row["student_name"],
                       row["room_id"],
                       datetime.fromisoformat(row["start_dt"]),
                       datetime.fromisoformat(row["end_dt"]),
                       row["request_timestamp"],
                       bool(row["is_canceled"]))
        except (KeyError, IndexError) as e:
            raise AttributeError(f"Database Mapping Error: Column {e} not found in row passed to from_row") from e

    def to_row(self):
        return {"id": self.id,
                "student_name": self.student_name,
                "room_id": self.room_id,
                "start_dt": self.start_dt,
                "end_dt": self.end_dt,
                "request_timestamp": self.request_timestamp,
                "is_canceled": self.is_canceled
        }