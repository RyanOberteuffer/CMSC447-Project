from app.backend.db import DB
from app.backend.table_object_classes.room import Room

class DBRoomFunctions:
    def __init__(self, db_:DB):
        self.db = db_

    def get_rooms(self):
        query = """
        SELECT room_id, room_name, room_location, capacity, room_type
        FROM Room
        ORDER BY room_name ASC
        """
        params = ()
        return self.db.get_all(query, params)

    def get_room_by_room_number(self, room_number: str) -> Room:
        """
        :param room_number: A string representing the location of the room in the library.
        :return: A Room object
        """
        query = "SELECT * FROM Room WHERE number = ? LIMIT 1"
        params = (room_number,)
        result = self.db.get_one(query, params)
        return Room.from_row(result)

    def get_room_mapping(self):
        """
        :return: A dictionary with room IDs as keys and room names as values.
        """
        query = "SELECT id, number FROM Room"
        params = ()
        result = self.db.get_all(query, params)
        return {row["id"]: row["number"] for row in result}