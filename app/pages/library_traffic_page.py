import streamlit as st
import pandas as pd
import sys
from pathlib import Path
from app.backend.db import DB
from app.backend.table_function_classes.db_libraryentrylog_functions import DBLELFunctions
from app.components.navbar import render_navbar

PAGE_DIR = Path(__file__).resolve().parent
APP_DIR = PAGE_DIR.parent
PROJECT_ROOT = APP_DIR.parent
sys.path.append(str(PROJECT_ROOT))
sys.path.append(str(Path(__file__).resolve().parents[2]))

if not "db" in st.session_state:
    st.session_state["db"] = DB()

if not "lel_functions" in st.session_state:
    st.session_state["lel_functions"] = DBLELFunctions(st.session_state["db"])
lel_functions = st.session_state["lel_functions"]

st.set_page_config(page_title="Library Traffic", page_icon="🚶", layout="wide")

if not (hasattr(st.user, "is_logged_in") and st.user.is_logged_in):
    st.warning("You must be signed in to access this page.")
    if st.button("Go to Login"):
        st.switch_page("pages/login_page.py")
    if st.button("Back to Home", key="traffic_security"):
        st.switch_page("pages/home_page.py")
    st.stop()

render_navbar()

if st.button("Back to Home"):
    st.switch_page("pages/home_page.py")

st.title("Library Traffic")
st.caption("Gate counter analytics for library entrance volume and peak usage patterns.")


rows = lel_functions.get_library_entry_log()

df = pd.DataFrame(rows, columns=["Entry ID", "Entry Time", "Entry Count"])

if df.empty:
    st.info("No library traffic data available yet.")
    st.stop()

df["Entry Time"] = pd.to_datetime(df["Entry Time"])
df["Date"] = df["Entry Time"].dt.date
df["Hour"] = df["Entry Time"].dt.strftime("%I:%M %p")
df["Weekday"] = df["Entry Time"].dt.day_name()

st.subheader("Hourly Traffic by Selected Day")
available_dates = sorted(df["Date"].unique())
selected_date = st.selectbox("Select a day", available_dates)
selected_day_df = df[df["Date"] == selected_date].copy()
selected_day_df = selected_day_df.sort_values("Entry Time")
line_df = selected_day_df[["Hour", "Entry Count"]].set_index("Hour")
st.line_chart(line_df)

today_df = df[df["Date"] == pd.Timestamp.today().date()]
entries_today = int(today_df["Entry Count"].sum()) if not today_df.empty else 0
avg_hourly = round(df["Entry Count"].mean(), 1)

if not today_df.empty:
    peak_row = today_df.loc[today_df["Entry Count"].idxmax()]
    peak_entries_today = int(peak_row["Entry Count"])
else:
    peak_entries_today = 0

m1, m2, m3 = st.columns(3)
m1.metric("Entries Today", entries_today)
m3.metric("Average Hourly Entries", avg_hourly)

st.subheader("Daily Totals")
daily_totals = df.groupby(["Date", "Weekday"], as_index=False)["Entry Count"].sum()
st.dataframe(daily_totals, use_container_width=True, hide_index=True)

st.subheader("Hourly Traffic Log This Week")
log_selected_date = st.selectbox(
    "Select a day for hourly log",
    available_dates,
    index=available_dates.index(selected_date),
    format_func=lambda d: d.strftime("%A, %B %d, %Y")
)
log_day_df = df[df["Date"] == log_selected_date].copy()
log_day_df = log_day_df.sort_values("Entry Time")
st.dataframe(
    log_day_df[["Hour", "Entry Count"]],
    use_container_width=True,
    hide_index=True
)
