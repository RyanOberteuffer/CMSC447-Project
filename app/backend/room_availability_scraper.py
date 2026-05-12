import requests
from datetime import datetime
from app.backend.db import DB
from app.backend.table_function_classes.db_room_functions import DBRoomFunctions
from app.backend.table_object_classes.room_reservation import RoomReservation

class RoomAvailabilityScraper:
    URL = "https://umbc.libcal.com/spaces/bookings/search"
    HEADERS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Language": "en-US,en;q=0.9",
        "referer": "https://umbc.libcal.com/spaces/bookings?lid=662&gid=0",
        "X-Requested-With": "XMLHttpRequest",
    }
    PARAMS = {
        "lid": 662,
        "gid": 0,
        "draw": 1,
        "start": 0,
        "length": 100,
        "d": "90",  # "Next 90 days" is usually more reliable than "all"
        "customDate": "",
        "search[value]": "",  # The API expects the search object keys
        "search[regex]": "false"
    }

    def scrape_room_bookings(self):
        """
        :return: A list of dictionaries returned by the API call representing bookings. An example returned dictionary looks like:
        {'from': '2026-05-11 14:00:00',
        'to': '2026-05-11 15:00:00',
        'nickname': '',
        'itemId': 134146,
        'itemName': '204',
        'itemHasMoreInfo': False,
        'categoryName': 'Individual Study Rooms',
        'categoryUrl': '/spaces?lid=662&gid=7691',
        'locationName': 'AOK Library',
        'seatName': ''}
        """
        self.PARAMS["start"] = 0
        full_res = []
        result = requests.get(self.URL, headers=self.HEADERS, params=self.PARAMS).json()["data"]
        full_res.extend(result)
        it = 0
        while result and it < 20:
            self.PARAMS["start"] += self.PARAMS["length"]
            result = requests.get(self.URL, headers=self.HEADERS, params=self.PARAMS).json()["data"]
            full_res.extend(result)
            it += 1
        return full_res

    @staticmethod
    def format_booking_data(booking_data):
        """
        Note, all dictionaries without the "className" key (which is how the UMBC library tags timeslots that are reserved) are tossed.
        :param booking_data: A list of dictionaries representing bookings. Probably taken from get_current_bookings().
        :return: A list of RoomReservation objects.
        """
        room_db = DBRoomFunctions(DB())
        bookings = []
        for reservation in booking_data:
            student_name = reservation["nickname"]
            room_id = room_db.get_room_by_room_number(reservation["itemName"]).id
            start_dt = datetime.fromisoformat(reservation["from"])
            end_dt = datetime.fromisoformat(reservation["to"])
            request_timestamp = datetime.now()
            reservation = RoomReservation(-1, student_name, room_id, start_dt, end_dt, request_timestamp)
            bookings.append(reservation)

        return bookings

ra_scraper = RoomAvailabilityScraper()
data = ra_scraper.scrape_room_bookings()
reservations = ra_scraper.format_booking_data(data)
"""
#@st.cache_data(ttl=3600)
def scrape_hourly():
    # 5/23/26 is a week out from start of finals, the calendar stops showing slots on this day
    days_until_semester_end = get_days_until_semester_end()
    ra_scraper = RoomAvailabilityScraper()
    availability_data = ra_scraper.scrape_room_availability(10)
    ra_scraper.send_to_db(availability_data)

# Gotta see what the library availability is like for summer and winter semesters
def get_days_until_semester_end():
    return_val = None
    today = date.today()
    curr_year = today.year

    spring_sem_start = date(curr_year, 1, 19)
    spring_sem_end = date(curr_year, 5, 30)

    fall_sem_start = date(curr_year, 8, 25)
    fall_sem_end = date(curr_year, 12, 27)

    if spring_sem_start <= today <= spring_sem_end: # Spring Semester
        return_val = (spring_sem_end - today).days
    elif fall_sem_start <= today <= fall_sem_end: # Fall Semester
        return_val = (fall_sem_end - today).days
    else:
        return_val = 0

    return return_val

ra_scraper = RoomAvailabilityScraper()
availability_data = ra_scraper.scrape_room_availability(3)
current_bookings = ra_scraper.get_current_bookings(availability_data)
print(availability_data)
"""