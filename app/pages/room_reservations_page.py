import streamlit as st
import pandas as pd
import sys
from datetime import date
import sys
import numpy as np
from pathlib import Path
from datetime import date, datetime, timedelta

from app.backend.table_function_classes.db_roomreservation_functions import DBRRFunctions
from app.backend.table_function_classes.db_room_functions import DBRoomFunctions
from app.backend.table_object_classes.room_reservation import RoomReservation
from app.backend.table_object_classes.room import Room
from app.backend.db import DB
from app.components.navbar import render_navbar

if not "db" in st.session_state:
    st.session_state["db"] = DB()
if not "rr_functions" in st.session_state:
    st.session_state["rr_functions"] = DBRRFunctions(st.session_state["db"])
rr_functions = st.session_state["rr_functions"]
if not "room_functions" in st.session_state:
    st.session_state["room_functions"] = DBRoomFunctions(st.session_state["db"])
room_functions = st.session_state["room_functions"]

def get_utilization_by_hour(room_: Room, reservations: list[RoomReservation], start_date: date, end_date: date):
    util_list = []
    filtered_reservations = [reservation for reservation in reservations
                            if (reservation.room_id == room_.id or room == "All")
                            and start_date <= reservation.date <= end_date]
    first_hour = min(room_.wd_availability_start, room_.sat_availability_start, room_.sun_availability_start)
    curr_hour = first_hour
    last_hour = max(room_.wd_availability_end, room_.sat_availability_end, room_.sun_availability_end)
    it = 0
    while curr_hour <= last_hour and it < 24:
        total_hours_across_dates = 0
        total_hours_across_dates += np.busday_count(start_date, end_date) * (room_.wd_availability_start <= curr_hour < room_.wd_availability_end)
        total_hours_across_dates += np.busday_count(start_date, end_date, weekmask='0000010') * (room_.sat_availability_start <= curr_hour < room_.sat_availability_end)
        total_hours_across_dates += np.busday_count(start_date, end_date, weekmask='0000001') * (room_.sun_availability_start <= curr_hour < room_.sun_availability_end)
        if total_hours_across_dates > 0:
            total_reservation_hours = len([r for r in filtered_reservations if r.start_time <= curr_hour < r.end_time])
            util_list.append((curr_hour, total_reservation_hours, total_hours_across_dates))
        else:
            pass

        curr_hour = (datetime.combine(date.today(), curr_hour) + timedelta(hours=1)).time()
        it += 1

    return util_list

if not (hasattr(st.user, "is_logged_in") and st.user.is_logged_in):
    st.warning("You must be signed in to access this page.")
    if st.button("Go to Login"):
        st.switch_page("pages/login_page.py")
    if st.button("Back to Home", key="security"):
        st.switch_page("pages/home_page.py")
    st.stop()

render_navbar()

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(PROJECT_ROOT))

st.set_page_config(
    page_title="Room Reservations",
    page_icon="x",
    layout="wide"
)

#home button
if st.button("Back to Home"):
    st.switch_page("pages/home_page.py")

st.title("Room Reservations")
st.caption("Monitor past, current, and upcoming reservations across library rooms.")

# -----------------------------
# Data loading

rr_functions.refresh_data()
rows = rr_functions.get_reservations()

df = pd.DataFrame([rr.to_row() for rr in rows])
df["is_canceled"] = df["is_canceled"].map({False: "No", True: "Yes"})
df["room_id"] = df["room_id"].map(room_functions.get_room_mapping())
df.columns = ["ID", "Student Name", "Room Name", "Date", "Start Time", "End Time", "Request Timestamp", "Is Cancelled"]

if df.empty:
    st.info("No reservation data available yet.")
    st.stop()

# -----------------------------
# Cleanup / formatting
df["Room Name"] = df["Room Name"].astype("category")
df["Start Time"] = df["Start Time"].astype(str).str[:5]
df["End Time"] = df["End Time"].astype(str).str[:5]

today = date.today()

def classify_period(reservation_date):
    """
    :param reservation_date:
    :return:
    """
    if reservation_date < today:
        return "Past"
    elif reservation_date == today:
        return "Today"
    return "Future"

df["Period"] = df["Date"].apply(classify_period)

total_reservations = len(df)
past_count = len(df[df["Period"] == "Past"])
today_count = len(df[df["Period"] == "Today"])
future_count = len(df[df["Period"] == "Future"])
cancellation_count = len(df[df["Is Cancelled"] == "Yes"])

m1, m2, m3, m4, m5 = st.columns(5)
m1.metric("Total", total_reservations)
m2.metric("Past", past_count)
m3.metric("Today", today_count)
m4.metric("Upcoming", future_count)
m5.metric("Cancelled", cancellation_count)

st.markdown("---")
st.subheader("Filters")

c1, c2, c3 = st.columns(3)

with c1:
    period_filter = st.selectbox(
        "Timeframe",
        ["All", "Past", "Today", "Future"]
    )

with c2:
    room_options = ["All"] + sorted(df["Room Name"].dropna().unique().tolist())
    room_filter = st.selectbox("Room Name", room_options)

with c3:
    student_name_filter = st.text_input("Student Name", value="")

filtered_df = df.copy()

if student_name_filter != "":
    filtered_df = filtered_df[filtered_df["Student Name"] == student_name_filter]

if period_filter != "All":
    filtered_df = filtered_df[filtered_df["Period"] == period_filter]

if room_filter != "All":
    filtered_df = filtered_df[filtered_df["Room Name"] == room_filter]

filtered_df = filtered_df.sort_values(by=["Date", "Start Time", "Room Name"], ascending=[True, True, True])

# -----------------------------
# Main reservation table
st.subheader("Reservation Timeline")
st.dataframe(filtered_df,
             use_container_width=True,
             hide_index=True,
             column_config={"Request Timestamp": None})

# -----------------------------
# Sectioned views
st.markdown("---")
st.subheader("Grouped Views")

tab1, tab2, tab3 = st.tabs(["Today", "Upcoming", "Past"])

with tab1:
    today_df = df[df["Period"] == "Today"].sort_values(by=["Start Time", "Room Name"])
    if today_df.empty:
        st.info("No reservations scheduled for today.")
    else:
        st.dataframe(today_df, use_container_width=True, hide_index=True)

with tab2:
    future_df = df[df["Period"] == "Future"].sort_values(by=["Date", "Start Time"])
    if future_df.empty:
        st.info("No upcoming reservations.")
    else:
        st.dataframe(future_df, use_container_width=True, hide_index=True)

with tab3:
    past_df = df[df["Period"] == "Past"].sort_values(by=["Date", "Start Time"], ascending=[False, False])
    if past_df.empty:
        st.info("No past reservations found.")
    else:
        st.dataframe(past_df, use_container_width=True, hide_index=True)

st.subheader("Room Utilization")
c1, c2, c3 = st.columns(3)
with c1:
    room_options = ["All"] + sorted(df["Room Name"].dropna().unique().tolist())
    room_filter = st.selectbox("Room Name", room_options)
if room_filter != "All":
    room = room_functions.get_room_by_room_number(room_filter)
    utilization_df = pd.DataFrame(
    get_utilization_by_hour(room, rows, datetime.now().date(), datetime.now().date() + timedelta(days=10)))
else:
    room = "All"
utilization_df.columns = ["Hour", "Utilization"]
utilization_df.set_index("Hour", inplace=True)
st.dataframe(utilization_df, use_container_width=True)