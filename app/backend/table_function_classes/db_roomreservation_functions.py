import sqlite3

from app.backend.db import DB
from app.backend.constants import NOT_FETCHED
from app.backend.table_object_classes.room_reservation import RoomReservation
from app.backend.room_availability_scraper import RoomAvailabilityScraper
import datetime

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

    def add_reservations(self, reservations):
        """
        If the combination of the date, start time, and room are unknown to the DB, then just add it. Otherwise, check that the new data is fresher, and if it is, use that.
        Additionally, remove reservations from the DB if the fresher data shows that the reservation has been canceled.
        :param reservations: A list of RoomReservation objects
        :return: None
        """
        old_reservations_set = set(self.get_reservations())
        new_reservations_set = set(reservations)
        reservations_to_delete = old_reservations_set - new_reservations_set
        reservations_to_add = new_reservations_set - old_reservations_set
        query = None
        params = None

        for reservation in reservations_to_delete:
            query = "UPDATE RoomReservations SET is_canceled = 1 WHERE room_id = ? AND reservation_date = ? AND start_time = ?"
            params = (reservation.room_id, reservation.date.isoformat(), reservation.start_time.isoformat())
            self.db.execute_command(query, params)

        for reservation in reservations_to_add:
            if reservation.id != -1: # Already has an assigned ID
                query = "SELECT * FROM RoomReservations WHERE id = ?"
                params = (reservation.id,)
            else:
                # The three of these parameters will specify a row
                query = "SELECT * FROM RoomReservations WHERE room_id = ? AND reservation_date = ?, AND start_time = ?"
                params = (reservation.room_id, reservation.date.isoformat(), reservation.start_time.isoformat())

            result = self.db.get_one(query, params)
            if result is sqlite3.Row:
                if result["request_timestamp"] < reservation.request_timestamp:
                    query = "UPDATE RoomReservations SET created_at = ?, is_canceled = ?, WHERE room_id = ?"
                    params = (reservation.request_timestamp.isoformat(), 0, reservation.room_id)
            else:
                query = "INSERT INTO RoomReservations (student_name, room_id, reservation_date, start_time, end_time, request_timestamp) VALUES (?, ?, ?, ?, ?, ?)"
                params = (reservation.student_name, reservation.room_id, reservation.date.isoformat(), reservation.start_time.isoformat(), reservation.end_time.isoformat(), reservation.request_timestamp)

            self.db.execute_command(query, params)

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
        self.add_reservations(self.reservation_scraper.format_booking_data(new_data))