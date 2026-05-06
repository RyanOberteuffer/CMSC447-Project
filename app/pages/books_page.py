import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[2]))

from app.components.navbar import render_navbar
from app.backend.get_db import get_db
import streamlit as st
import pandas as pd

st.set_page_config(page_title="Book Management", page_icon="📚", layout="wide")

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

st.title("Book Management")
st.caption("Search, filter, and review the library catalog.")

rows = db.get_printable_table("BookLocator")
df = pd.DataFrame(
    rows,
    columns=["Book ID", "Title", "Author", "ISBN", "Shelf Location", "Availability"]
)

search = st.text_input("Search by title, author, ISBN, or shelf location")

col1, col2 = st.columns([1, 1])
with col1:
    status_filter = st.selectbox(
        "Availability Status",
        ["All", "Available", "Checked Out"]
    )
with col2:
    sort_by = st.selectbox(
        "Sort By",
        ["Title", "Author", "Shelf Location"]
    )

filtered_df = df.copy()
if search:
    q = search.strip().lower()
    filtered_df = filtered_df[
        filtered_df["Title"].str.lower().str.contains(q, na=False) |
        filtered_df["Author"].str.lower().str.contains(q, na=False) |
        filtered_df["ISBN"].astype(str).str.lower().str.contains(q, na=False) |
        filtered_df["Shelf Location"].str.lower().str.contains(q, na=False)
    ]

if status_filter != "All":
    filtered_df = filtered_df[filtered_df["Availability"] == status_filter]

filtered_df = filtered_df.sort_values(by=sort_by)

total_books = len(df)
available_books = len(df[df["Availability"] == "Available"])
checked_out_books = len(df[df["Availability"] == "Checked Out"])

m1, m2, m3 = st.columns(3)
m1.metric("Total Books", total_books)
m2.metric("Available", available_books)
m3.metric("Checked Out", checked_out_books)

st.markdown("### Catalog")
st.dataframe(
    filtered_df,
    use_container_width=True,
    hide_index=True
)