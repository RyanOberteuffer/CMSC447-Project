import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[2]))

from app.components.navbar import render_navbar
from app.backend.get_db import get_db
import streamlit as st
import pandas as pd

st.set_page_config(page_title="Printer Management", page_icon="🖨️", layout="wide")

if not (hasattr(st.user, "is_logged_in") and st.user.is_logged_in):
    st.warning("You must be signed in to access this page.")
    if st.button("Go to Login"):
        st.switch_page("pages/login_page.py")
    st.stop()

render_navbar()
db = get_db()

st.markdown(
    """
    <style>
    .stApp {
        background-color: #f7f7f5;
    }
    .page-card {
        background: white;
        border: 1px solid #ece8df;
        border-radius: 16px;
        padding: 1rem 1.1rem;
        box-shadow: 0 3px 12px rgba(0,0,0,0.05);
        margin-bottom: 1rem;
    }
    .muted {
        color: #5f6368;
    }
    </style>
    """,
    unsafe_allow_html=True
)

if st.button("Back to Home"):
    st.switch_page("pages/home_page.py")

st.title("Printer Management")
st.caption("Monitor printer availability, maintenance, supply levels, and recent usage.")

printer_rows = db.get_printers()
usage_rows = db.get_printer_usage()
summary_rows = db.get_printer_usage_summary()

printer_df = pd.DataFrame(
    printer_rows,
    columns=[
        "Printer ID", "Printer Name", "Location", "Model",
        "Status", "Toner Level %", "Paper Level %", "Last Maintenance"
    ]
)

warning_df = printer_df[
    (printer_df["Toner Level %"] <= 20) | (printer_df["Paper Level %"] <= 20)
]
if not warning_df.empty:
    st.warning("⚠️ One or more printers need attention. (Warning: low resources)")

usage_df = pd.DataFrame(
    usage_rows,
    columns=[
        "Usage ID", "Printer Name", "Location",
        "Pages Printed", "Job Status", "Print Time"
    ]
)
summary_df = pd.DataFrame(
    summary_rows,
    columns=["Printer Name", "Total Jobs", "Total Pages"]
)

total_printers = len(printer_df)
available_count = len(printer_df[printer_df["Status"] == "Available"])
issue_count = len(printer_df[printer_df["Status"].isin(["Offline", "Maintenance"])])
total_pages = int(summary_df["Total Pages"].sum()) if not summary_df.empty else 0

m1, m2, m3, m4 = st.columns(4)
m1.metric("Total Printers", total_printers)
m2.metric("Available", available_count)
m3.metric("Needs Attention", issue_count)
m4.metric("Pages Printed", total_pages)

st.subheader("Printer Status")
status_filter = st.selectbox(
    "Filter by status",
    ["All"] + sorted(printer_df["Status"].dropna().unique().tolist())
)

filtered_printer_df = printer_df.copy()
if status_filter != "All":
    filtered_printer_df = filtered_printer_df[filtered_printer_df["Status"] == status_filter]

def highlight_low_resources(row):
    if row["Toner Level %"] <= 20 or row["Paper Level %"] <= 20:
        return ['background-color: #fff3cd'] * len(row)
    return [''] * len(row)

# ✅ Fixed the corrupted line
styled_printer_df = filtered_printer_df.style.apply(highlight_low_resources, axis=1)
st.dataframe(
    styled_printer_df,
    use_container_width=True,
    hide_index=True
)

st.subheader("Usage Summary by Printer")
st.dataframe(
    summary_df,
    use_container_width=True,
    hide_index=True
)
