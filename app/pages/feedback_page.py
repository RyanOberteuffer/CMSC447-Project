import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[2]))

from app.components.navbar import render_navbar
from app.backend.get_db import get_db
import streamlit as st

st.set_page_config(page_title="Feedback", page_icon="📝", layout="wide")

if not (hasattr(st.user, "is_logged_in") and st.user.is_logged_in):
    st.warning("You must be signed in to access this page.")
    if st.button("Go to Login"):
        st.switch_page("pages/login_page.py")
    st.stop()

render_navbar()
db = get_db()

if st.button("Back to Home"):
    st.switch_page("pages/home_page.py")

st.title("Feedback")
st.caption("Having issues? Recommendations?")

option = st.selectbox(
    "Select an option",
    ["Bug Report", "Feature Request", "Compliment"]
)

max_chars = 1000
content = st.text_area("Enter your feedback", max_chars=max_chars)

submit = st.button("Submit")
if submit:
    db.add_feedback(option, content)
    st.success("Thank you for your feedback!")
    st.write(db.get_printable_table("FeedbackForms"))