import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[2]))

from app.components.navbar import render_navbar
import streamlit as st
from pathlib import Path
import sys
from app.backend.db import DB
from app.backend.table_function_classes.db_roomreservation_functions import DBRRFunctions
from app.backend.table_function_classes.db_printer_functions import DBPrinterFunctions
from app.backend.table_function_classes.db_user_functions import DBUserFunctions
from app.backend.table_object_classes.user import User

st.set_page_config(
    page_title="UMBC Library Dashboard",
    page_icon="📚",
    layout="wide"
)

PAGE_DIR = Path(__file__).resolve().parent
APP_DIR = PAGE_DIR.parent
PROJECT_ROOT = APP_DIR.parent
ASSETS_DIR = APP_DIR / "assets"
LOGO_PATH = ASSETS_DIR / "umbclogo.png"

if not "db" in st.session_state:
    st.session_state["db"] = DB()

if not "rr_functions" in st.session_state:
    st.session_state["rr_functions"] = DBRRFunctions(st.session_state["db"])
rr_functions = st.session_state["rr_functions"]

if not "printer_functions" in st.session_state:
    st.session_state["printer_functions"] = DBPrinterFunctions(st.session_state["db"])
printer_functions = st.session_state["printer_functions"]

if not "user_functions" in st.session_state:
    st.session_state["user_functions"] = DBUserFunctions(st.session_state["db"])
user_functions = st.session_state["user_functions"]

#sys overview
pending_reservations_count = rr_functions.get_reservations_count()
printers_attention_count = printer_functions.get_printers_needing_attention_count()

#user login flag
if not "user" in st.session_state:
    if st.user.is_logged_in:
        partial_user_obj = User(email=st.user.email)
        st.session_state["user"] = user_functions.get_user(partial_user_obj)
    else:
        st.session_state["user"] = User()
st.set_page_config(
    page_title="UMBC Library Dashboard",
    page_icon="📚",
    layout="wide"
)

is_logged_in = hasattr(st.user, "is_logged_in") and st.user.is_logged_in
name = getattr(st.user, "name", None) or "Guest"
email = getattr(st.user, "email", None) or "Not signed in"

render_navbar()

st.markdown(
    """
    <style>
    .stApp {
        background-color: #f7f7f5;
    }
    .top-banner {
        background: linear-gradient(90deg, #1f1f1f 0%, #2a2a2a 100%);
        padding: 1.2rem 1.5rem;
        border-radius: 16px;
        border-left: 8px solid #fdb515;
        box-shadow: 0 4px 14px rgba(0,0,0,0.10);
        margin-bottom: 1rem;
    }
    .banner-title {
        color: white;
        font-size: 2rem;
        font-weight: 800;
        margin: 0;
    }
    .banner-subtitle {
        color: #e7e7e7;
        margin-top: 0.35rem;
        font-size: 1rem;
    }
    .section-card {
        background: white;
        padding: 1.1rem 1.2rem;
        border-radius: 16px;
        border: 1px solid #ece8df;
        box-shadow: 0 3px 12px rgba(0,0,0,0.05);
        margin-bottom: 1rem;
    }
    .card-title {
        font-size: 1.05rem;
        font-weight: 800;
        color: #1f1f1f;
        margin-bottom: 0.4rem;
    }
    .muted {
        color: #5f6368;
        font-size: 0.95rem;
    }
    .account-box {
        background: #fffaf0;
        border: 1px solid #f2d58a;
        border-left: 6px solid #fdb515;
        padding: 0.9rem 1rem;
        border-radius: 12px;
        margin-top: 0.8rem;
    }
    div.stButton > button {
        border-radius: 12px;
        border: 1px solid #1f1f1f;
        background-color: #1f1f1f;
        color: white;
        font-weight: 700;
        padding: 0.55rem 0.8rem;
    }
    div.stButton > button:hover {
        border-color: #fdb515;
        color: #fdb515;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Top banner
banner_left, spacer, banner_right = st.columns([8, .5, 1])

with banner_left:
    st.markdown(
        """
        <div class="top-banner">
            <div class="banner-title">UMBC Library Dashboard</div>
            <div class="banner-subtitle">
                Operations portal for books, reservations, printers, and service monitoring
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with spacer:
    st.write("")

with banner_right:
    if LOGO_PATH.exists():
        st.image(LOGO_PATH, width=95)

# Account + System Overview
left, spacer, right = st.columns([1.2, .2, 1])

with left:
    st.markdown('<div class="card-title">Account</div>', unsafe_allow_html=True)

    if st.user.is_logged_in:
        st.markdown(
            f"""
            <div class="account-box">
                <div><strong>Name:</strong> {st.session_state["user"].name}</div>
                <div><strong>Email:</strong> {st.session_state["user"].email}</div>
                <div><strong>Status:</strong> Authenticated through Google</div>
            </div>
            """,
            unsafe_allow_html=True
        )
        st.markdown("<div style='height: 15px;'></div>", unsafe_allow_html=True)
        if st.button("Log out", use_container_width=True):
            st.logout()
    else:
        st.markdown(
            '<div class="muted">Sign in with your UMBC Google account to access protected dashboard tools.</div>',
            unsafe_allow_html=True
        )
        if st.button("Go to Login", use_container_width=True):
            st.switch_page("pages/login_page.py")

with spacer:
    st.write("")

with right:
    if st.user.is_logged_in:
        st.markdown('<div class="card-title">System Overview</div>', unsafe_allow_html=True)
        st.markdown(
            '<div class="muted">Use this dashboard to monitor library resources, room activity, printing demand, and user feedback in one place.</div>',
            unsafe_allow_html=True
        )
        if pending_reservations_count == 0:
            st.success("No pending reservation requests")
        elif pending_reservations_count == 1:
            st.info("1 pending reservation request")
        else:
            st.info(f"{pending_reservations_count} pending reservation requests")

        if printers_attention_count == 0:
            st.success("No printers currently need attention")
        elif printers_attention_count == 1:
            st.warning("1 printer may need attention")
        else:
            st.warning(f"{printers_attention_count} printers may need attention")

# Navigation cards
st.markdown("## Dashboard Navigation")

c1, c2 = st.columns(2)

with c1:
    st.markdown("### Books")
    st.markdown('<div class="muted">Browse catalog inventory, search titles, and filter by availability or location.</div>', unsafe_allow_html=True)
    if st.user.is_logged_in:
        if st.button("Open Books Page", use_container_width=True, key="books_btn"):
            st.switch_page("pages/books_page.py")
    else:
        st.button("Login required", use_container_width=True, disabled=True, key="books_disabled")

with c2:
    st.markdown("### Room Reservations")
    st.markdown('<div class="muted">Review past, current, and future reservations by room, requester, and purpose.</div>', unsafe_allow_html=True)
    if st.user.is_logged_in:
        if st.button("Open Reservations Page", use_container_width=True, key="rooms_btn"):
            st.switch_page("pages/room_reservations_page.py")
    else:
        st.button("Login required", use_container_width=True, disabled=True, key="rooms_disabled")

c3, c4 = st.columns(2)

with c3:
    st.markdown("### Printer Management")
    st.markdown('<div class="muted">Track printer status, usage activity, and operational demand across the library.</div>', unsafe_allow_html=True)
    if st.user.is_logged_in:
        if st.button("Open Printer Page", use_container_width=True, key="printer_btn"):
            st.switch_page("pages/printer_page.py")
    else:
        st.button("Login required", use_container_width=True, disabled=True, key="printer_disabled")

with c4:
    st.markdown("### Library Traffic")
    st.markdown('<div class="muted">View current occupancy, peak hours.</div>', unsafe_allow_html=True)
    if st.user.is_logged_in:
        if st.button("Open Library Traffic Page", use_container_width=True, key="library_traffic_btn"):
            st.switch_page("pages/library_traffic_page.py")
    else:
        st.button("Login required", use_container_width=True, disabled=True, key="traffic_disabled")

c5, c6 = st.columns(2)

with c5:
    st.markdown("### Feedback")
    st.markdown('<div class="muted">Submit bug reports, feature requests, and compliments.</div>', unsafe_allow_html=True)
    if st.button("Open Feedback Page", use_container_width=True, key="feedback_btn"):
        st.switch_page("pages/feedback_page.py")

if st.user.is_logged_in:
    user_role = st.session_state["user"].role
    if user_role == "admin" or user_role == "developer":
        with c6:
            with st.container():
                st.markdown("### Admin Controls")
                st.markdown(
                    '<div class="muted">Add and remove users, change permissions</div>',
                    unsafe_allow_html=True
                )
                st.markdown('</div>', unsafe_allow_html=True)
                if st.button("Open Admin Controls", use_container_width=True, key="admin_btn"):
                    st.switch_page("pages/admin_controls_page.py")