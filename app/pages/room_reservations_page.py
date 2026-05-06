import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[2]))

from app.components.navbar import render_navbar
from app.backend.get_db import get_db
import streamlit as st
import pandas as pd
from datetime import date

st.set_page_config(
    page_title="Room Reservations",
    page_icon="🚪",
    layout="wide"
)

if not (hasattr(st.user, "is_logged_in") and st.user.is_logged_in):
    st.warning("You must be signed in to access this page.")
    if st.button("Go to Login"):
        st.switch_page("pages/login_page.py")
    if st.button("Back to Home", key="security"):
        st.switch_page("pages/home_page.py")
    st.stop()

render_navbar()
db = get_db()

if st.button("Back to Home"):
    st.switch_page("pages/home_page.py")

st.title("Room Reservations")
st.caption("Monitor past, current, and upcoming reservations across library rooms.")

rows = db.get_room_reservations()

columns = [
    "Reservation ID", "Room", "Location", "Capacity",
    "Reserved By", "Purpose", "Date", "Start Time",
    "End Time", "Status", "Notes", "Created At"
]

df = pd.DataFrame(rows, columns=columns)

if df.empty:
    st.info("No reservation data available yet.")
    st.stop()

df["Date"] = pd.to_datetime(df["Date"]).dt.date
df["Start Time"] = df["Start Time"].astype(str).str[:5]
df["End Time"] = df["End Time"].astype(str).str[:5]
df["Created At"] = pd.to_datetime(df["Created At"], errors="coerce")

today = date.today()

def classify_period(reservation_date):
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
pending_count = len(df[df["Status"].str.lower() == "pending"])

m1, m2, m3, m4, m5 = st.columns(5)
m1.metric("Total", total_reservations)
m2.metric("Past", past_count)
m3.metric("Today", today_count)
m4.metric("Upcoming", future_count)
m5.metric("Pending", pending_count)

st.markdown("---")
st.subheader("Filters")

c1, c2, c3, c4 = st.columns(4)

with c1:
    search_text = st.text_input(
        "Search by person or purpose",
        placeholder="e.g. study group, Ava Johnson"
    )
with c2:
    period_filter = st.selectbox("Timeframe", ["All", "Past", "Today", "Future"])
with c3:
    room_options = ["All"] + sorted(df["Room"].dropna().unique().tolist())
    room_filter = st.selectbox("Room", room_options)
with c4:
    status_options = ["All"] + sorted(df["Status"].dropna().unique().tolist())
    status_filter = st.selectbox("Status", status_options)

filtered_df = df.copy()

if search_text:
    q = search_text.strip().lower()
    filtered_df = filtered_df[
        filtered_df["Reserved By"].str.lower().str.contains(q, na=False) |
        filtered_df["Purpose"].str.lower().str.contains(q, na=False)
    ]

if period_filter != "All":
    filtered_df = filtered_df[filtered_df["Period"] == period_filter]
if room_filter != "All":
    filtered_df = filtered_df[filtered_df["Room"] == room_filter]
if status_filter != "All":
    filtered_df = filtered_df[filtered_df["Status"] == status_filter]

filtered_df = filtered_df.sort_values(
    by=["Date", "Start Time", "Room"],
    ascending=[True, True, True]
)

st.subheader("Reservation Timeline")
display_df = filtered_df[[
    "Date", "Start Time", "End Time", "Room", "Location",
    "Reserved By", "Purpose", "Status", "Notes"
]]
st.dataframe(display_df, use_container_width=True, hide_index=True)

st.markdown("---")
st.subheader("Grouped Views")

tab1, tab2, tab3 = st.tabs(["Today", "Upcoming", "Past"])

with tab1:
    today_df = df[df["Period"] == "Today"].sort_values(by=["Start Time", "Room"])
    if today_df.empty:
        st.info("No reservations scheduled for today.")
    else:
        st.dataframe(
            today_df[["Start Time", "End Time", "Room", "Reserved By", "Purpose", "Status"]],
            use_container_width=True, hide_index=True
        )

with tab2:
    future_df = df[df["Period"] == "Future"].sort_values(by=["Date", "Start Time"])
    if future_df.empty:
        st.info("No upcoming reservations.")
    else:
        st.dataframe(
            future_df[["Date", "Start Time", "End Time", "Room", "Reserved By", "Purpose", "Status"]],
            use_container_width=True, hide_index=True
        )

with tab3:
    past_df = df[df["Period"] == "Past"].sort_values(by=["Date", "Start Time"], ascending=[False, False])
    if past_df.empty:
        st.info("No past reservations found.")
    else:
        st.dataframe(
            past_df[["Date", "Start Time", "End Time", "Room", "Reserved By", "Purpose", "Status"]],
            use_container_width=True, hide_index=True
        )