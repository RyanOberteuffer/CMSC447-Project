import sys
import os
import smtplib
from email.message import EmailMessage
from app.backend.table_object_classes.user import User
from app.backend.table_object_classes.feedback import Feedback
from app.backend.table_function_classes.db_feedback_functions import DBFeedbackFunctions
from app.backend.table_function_classes.db_user_functions import DBUserFunctions
from app.backend.constants import NOT_FETCHED
from app.backend.db import DB
from datetime import datetime, timezone
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[2]))

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

if not "db" in st.session_state:
    st.session_state["db"] = DB()
db = st.session_state["db"]
from app.components.navbar import render_navbar
from app.backend.get_db import get_db
import streamlit as st

st.set_page_config(page_title="Feedback", page_icon="📝", layout="wide")

if not "feedback_functions" in st.session_state:
    st.session_state["feedback_functions"] = DBFeedbackFunctions(st.session_state["db"])
feedback_functions = st.session_state["feedback_functions"]

if not "user_functions" in st.session_state:
    st.session_state["user_functions"] = DBUserFunctions(st.session_state["db"])
user_functions = st.session_state["user_functions"]

if not "user" in st.session_state:
    if st.user.is_logged_in:
        user = User(-1, "", st.user.email, "user")
        st.session_state["user"] = user_functions.get_user(user)
    else:
        st.session_state["user"] = User()

def email_feedback(feedback_:Feedback):
    dev_emails = [user.email for user in user_functions.get_users_by_role("developer")]
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    sender_email = "librarydashboard39@gmail.com"
    sender_password = st.secrets["EMAIL_PASSWORD"]

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            for recipient in dev_emails:
                msg = EmailMessage()
                msg.set_content(f"New {feedback_.type} submitted:\n\n{feedback_.content}")
                msg["Subject"] = "Alert: New System Feedback"
                msg["From"] = sender_email
                msg["To"] = recipient
                server.send_message(msg)
    except Exception as e:
        print(f"SMTP Error: {e}")
if not (hasattr(st.user, "is_logged_in") and st.user.is_logged_in):
    st.warning("You must be signed in to access this page.")
    if st.button("Go to Login"):
        st.switch_page("pages/login_page.py")
    st.stop()

render_navbar()
db = get_db()

if st.button("Back to Home"):
    st.switch_page("pages/home_page.py")

#title
st.title("Feedback")
st.caption("Having issues; Recommendations?")

option = st.selectbox("Select an option", Feedback.TYPES, format_func=lambda o: o.title())
content = st.text_area("Enter your feedback", max_chars=Feedback.MAX_LENGTH)

submit = st.button("Submit")
if submit:
    most_recent_feedback = feedback_functions.get_last_feedback(st.session_state["user"])
    minutes_since_last_submission = sys.maxsize
    if most_recent_feedback is NOT_FETCHED:
        st.error("Failed to try to fetch user feedback")
    else:
        if most_recent_feedback is not None:
            minutes_since_last_submission = (datetime.now(timezone.utc) - most_recent_feedback.submission_time).total_seconds() / 60

    if content == "":
        st.error("Please enter a description before submitting!")
    elif minutes_since_last_submission < 5:
        st.error("Can't submit feedback less than 5 minutes apart. Please wait {:.0f} minutes before submitting.".format(5 - minutes_since_last_submission))
    else:
        feedback = Feedback(type=option, content=content, user_id=st.session_state["user"].id)
        feedback_functions.add_feedback(feedback)
        email_feedback(feedback)
        st.success("Feedback submitted successfully!")
        st.write("Time since last feedback submission: ", minutes_since_last_submission)