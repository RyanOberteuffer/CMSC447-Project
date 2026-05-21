import streamlit as st
from backend.database import SessionLocal, Base, Engine
from backend.sqlalchemy_table_classes import *

@st.cache_resource
def get_db_session():
    return SessionLocal()

db = get_db_session()
Base.metadata.create_all(Engine)

#st.switch_page("pages/home_page.py")