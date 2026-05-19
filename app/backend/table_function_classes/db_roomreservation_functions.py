import sqlite3
from collections.abc import Iterable

from app.backend.db import DB
from app.backend.constants import NOT_FETCHED
from app.backend.table_object_classes.room_reservation import RoomReservation
from app.backend.room_availability_scraper import RoomAvailabilityScraper

class DBRRFunctions:
    reservation_scraper: RoomAvailabilityScraper = RoomAvailabilityScraper()

    def __init__(self, db_:DB):
        self.db = db_

    def get_reservations_count(self):
        """
        Returns the number of non-canceled reservations in the DB.
        """
        query = """
        SELECT COUNT(*)
        FROM RoomReservations
        WHERE is_canceled = 0
        """
        params = ()
        result = self.db.get_one(query, params)
        return result[0] if result else 0

    def add_reservations(self, reservations: Iterable[RoomReservation]):
        """
        If the combination of the date, start time, and room are unknown to the DB, then just add it. Otherwise, check that the new data is fresher, and if it is, use that.
        Additionally, remove reservations from the DB if the fresher data shows that the reservation has been canceled.
        :param reservations: A list of RoomReservation objects
        :return: None
        """
        self.db.execute_command("DROP TABLE IF EXISTS TempRoomReservations", ())
        
        query = "CREATE TEMP TABLE TempRoomReservations AS SELECT * FROM RoomReservations WHERE 0"
        params = ()
        self.db.execute_command(query, params)

        query = """INSERT INTO TempRoomReservations (student_name, room_id, start_dt, end_dt, request_timestamp) VALUES
                                                    (:student_name, :room_id, :start_dt, :end_dt, :request_timestamp)"""
        paramslist = [reservation.to_row() for reservation in reservations]
        self.db.execute_batch(query, paramslist)

        query = """INSERT INTO RoomReservations (student_name, room_id, start_dt, end_dt, request_timestamp, is_canceled)
                SELECT student_name, room_id, start_dt, end_dt, request_timestamp, is_canceled FROM TempRoomReservations
                ON CONFLICT(room_id, start_dt) DO UPDATE
                SET request_timestamp = excluded.request_timestamp,
                is_canceled = excluded.is_canceled
                WHERE excluded.request_timestamp > request_timestamp"""
        self.db.execute_command(query, ())

    def delete_reservations(self, reservations: Iterable[RoomReservation]):
        query = ("UPDATE RoomReservations SET is_canceled = 1, request_timestamp = :request_timestamp WHERE"
                 "room_id = :room_id AND start_dt = :start_dt AND request_timestamp < :request_timestamp")
        param_list = [reservation.to_row() for reservation in reservations]
        self.db.execute_batch(query, param_list)

    def get_reservations(self):
        """
        Returns a list of all reservations as RoomReservation objects.
        """
        reservations = []
        query = "SELECT * FROM RoomReservations WHERE is_canceled = 0"
        params = ()
        result = self.db.get_all(query, params)
        if not result is NOT_FETCHED:
            for reservation_ in result:
                reservations.append(RoomReservation.from_row(reservation_))

        return reservations

    def refresh_data(self):
        new_data = self.reservation_scraper.scrape_room_bookings()

        old_reservations_set = set(self.get_reservations())
        new_reservations_set = set(new_data)
        reservations_to_delete = old_reservations_set - new_reservations_set
        reservations_to_add = new_reservations_set - old_reservations_set

        self.add_reservations(reservations_to_add)
        self.delete_reservations(reservations_to_delete)