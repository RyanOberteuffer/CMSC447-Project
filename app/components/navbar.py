import streamlit as st

def render_navbar():
    st.markdown("""
        <style>
        .navbar {
            background-color: #f0a500;
            padding: 10px 24px;
            display: flex;
            gap: 28px;
            font-weight: bold;
            font-size: 15px;
            margin-bottom: 20px;
        }
        .navbar a {
            color: white;
            text-decoration: none;
        }
        .navbar a:hover {
            text-decoration: underline;
        }
        </style>
        <div class="navbar">
            <a href="/home_page" target="_self">Home</a>
            <a href="/books_page" target="_self">Books</a>
            <a href="/room_reservations_page" target="_self">Room Reservations</a>
            <a href="/printer_page" target="_self">Printer Management</a>
            <a href="/library_traffic_page" target="_self">Library Traffic</a>
            <a href="/feedback_page" target="_self">Feedback</a>
        </div>
    """, unsafe_allow_html=True)